//! Dimensional analysis for unit-aware symbolic regression.
//!
//! Provides [`Units`] — a 7-element exponent vector representing SI base units —
//! and [`UnitError`] for dimensional consistency violations. Integrates with
//! [`crate::lower::LoweredOp::check_units`] to enable hard pruning of
//! dimensionally-inadmissible topologies during symbolic regression.
//!
//! # SI base dimensions
//!
//! Index | Symbol | Quantity
//! ------|--------|----------
//! 0     | m      | Length
//! 1     | kg     | Mass
//! 2     | s      | Time
//! 3     | A      | Electric current
//! 4     | K      | Thermodynamic temperature
//! 5     | mol    | Amount of substance
//! 6     | cd     | Luminous intensity
//!
//! # Example
//!
//! ```
//! use oxieml::units::Units;
//!
//! // velocity: m/s
//! let velocity = Units::METER.div(&Units::SECOND);
//! assert_eq!(velocity.0, [1, 0, -1, 0, 0, 0, 0]);
//!
//! // kinetic energy: kg·m²/s²  ≡ JOULE
//! let ke = Units::KILOGRAM.mul(&Units::METER).mul(&Units::METER).div(&Units::SECOND).div(&Units::SECOND);
//! assert_eq!(ke, Units::JOULE);
//! ```

use std::fmt;

/// SI unit represented as a 7-element exponent vector `[m, kg, s, A, K, mol, cd]`.
///
/// Positive exponents appear in the numerator, negative in the denominator.
/// The arithmetic follows the standard rules:
///
/// - Multiplication: element-wise addition of exponents (`m·s → [1,0,1,0,0,0,0]`).
/// - Division: element-wise subtraction of exponents (`m/s → [1,0,-1,0,0,0,0]`).
/// - Integer power: element-wise scaling (`m² → [2,0,0,0,0,0,0]`).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Units(pub [i8; 7]);

impl Units {
    // -----------------------------------------------------------------------
    // SI base units
    // -----------------------------------------------------------------------

    /// Dimensionless quantity (no physical unit).
    pub const DIMENSIONLESS: Self = Self([0, 0, 0, 0, 0, 0, 0]);
    /// Metre (length).
    pub const METER: Self = Self([1, 0, 0, 0, 0, 0, 0]);
    /// Kilogram (mass).
    pub const KILOGRAM: Self = Self([0, 1, 0, 0, 0, 0, 0]);
    /// Second (time).
    pub const SECOND: Self = Self([0, 0, 1, 0, 0, 0, 0]);
    /// Ampere (electric current).
    pub const AMPERE: Self = Self([0, 0, 0, 1, 0, 0, 0]);
    /// Kelvin (thermodynamic temperature).
    pub const KELVIN: Self = Self([0, 0, 0, 0, 1, 0, 0]);
    /// Mole (amount of substance).
    pub const MOL: Self = Self([0, 0, 0, 0, 0, 1, 0]);
    /// Candela (luminous intensity).
    pub const CANDELA: Self = Self([0, 0, 0, 0, 0, 0, 1]);

    // -----------------------------------------------------------------------
    // Derived units
    // -----------------------------------------------------------------------

    /// Newton (force): kg·m·s⁻².
    pub const NEWTON: Self = Self([1, 1, -2, 0, 0, 0, 0]);
    /// Joule (energy): kg·m²·s⁻².
    pub const JOULE: Self = Self([2, 1, -2, 0, 0, 0, 0]);
    /// Watt (power): kg·m²·s⁻³.
    pub const WATT: Self = Self([2, 1, -3, 0, 0, 0, 0]);
    /// Pascal (pressure): kg·m⁻¹·s⁻².
    pub const PASCAL: Self = Self([-1, 1, -2, 0, 0, 0, 0]);
    /// Hertz (frequency): s⁻¹.
    pub const HERTZ: Self = Self([0, 0, -1, 0, 0, 0, 0]);
    /// Coulomb (electric charge): A·s.
    pub const COULOMB: Self = Self([0, 0, 1, 1, 0, 0, 0]);
    /// Volt (electric potential): kg·m²·s⁻³·A⁻¹.
    pub const VOLT: Self = Self([2, 1, -3, -1, 0, 0, 0]);
    /// Ohm (electric resistance): kg·m²·s⁻³·A⁻².
    pub const OHM: Self = Self([2, 1, -3, -2, 0, 0, 0]);

    // -----------------------------------------------------------------------
    // Constructors
    // -----------------------------------------------------------------------

    /// Construct a `Units` value from a raw 7-element exponent array.
    #[inline]
    pub const fn new(exps: [i8; 7]) -> Self {
        Self(exps)
    }

    /// Return `true` when all exponents are zero (i.e. dimensionless).
    #[inline]
    pub fn is_dimensionless(&self) -> bool {
        self.0 == [0; 7]
    }

    // -----------------------------------------------------------------------
    // Arithmetic
    // -----------------------------------------------------------------------

    /// Multiply units: element-wise addition of exponents.
    ///
    /// Equivalent to multiplying two quantities with these units.
    #[inline]
    pub fn mul(&self, other: &Self) -> Self {
        let mut result = [0i8; 7];
        for (dst, (&a, &b)) in result.iter_mut().zip(self.0.iter().zip(other.0.iter())) {
            *dst = a.saturating_add(b);
        }
        Self(result)
    }

    /// Divide units: element-wise subtraction of exponents.
    ///
    /// Equivalent to dividing a quantity with `self` units by one with `other` units.
    #[inline]
    pub fn div(&self, other: &Self) -> Self {
        let mut result = [0i8; 7];
        for (dst, (&a, &b)) in result.iter_mut().zip(self.0.iter().zip(other.0.iter())) {
            *dst = a.saturating_sub(b);
        }
        Self(result)
    }

    /// Raise to an integer power: multiply each exponent by `n`.
    ///
    /// Returns `Err` when exponent overflow occurs (any dimension would exceed `i8` range).
    ///
    /// # Errors
    ///
    /// Returns [`UnitError::ExponentOverflow`] when any exponent would overflow `i8`.
    pub fn pow_int(&self, n: i32) -> Result<Self, UnitError> {
        let mut result = [0i8; 7];
        for (i, &exp) in self.0.iter().enumerate() {
            let scaled = i64::from(exp) * i64::from(n);
            if scaled < i64::from(i8::MIN) || scaled > i64::from(i8::MAX) {
                return Err(UnitError::ExponentOverflow {
                    dimension: i,
                    base_exp: exp,
                    power: n,
                });
            }
            result[i] = scaled as i8;
        }
        Ok(Self(result))
    }

    // -----------------------------------------------------------------------
    // Symbol helpers
    // -----------------------------------------------------------------------

    /// Symbol string for dimension `idx` (0 = m, 1 = kg, 2 = s, …).
    fn dim_symbol(idx: usize) -> &'static str {
        match idx {
            0 => "m",
            1 => "kg",
            2 => "s",
            3 => "A",
            4 => "K",
            5 => "mol",
            6 => "cd",
            _ => "?",
        }
    }
}

// -----------------------------------------------------------------------
// Display — produces strings like "m¹·kg²·s⁻²"
// -----------------------------------------------------------------------

impl fmt::Display for Units {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.is_dimensionless() {
            return write!(f, "1");
        }

        let superscripts = |n: i8| -> String {
            // Fast path for the common cases.
            match n {
                1 => String::new(),                   // exponent 1 is implicit
                -1 => "\u{207B}\u{00B9}".to_string(), // ⁻¹
                2 => "\u{00B2}".to_string(),
                3 => "\u{00B3}".to_string(),
                -2 => "\u{207B}\u{00B2}".to_string(),
                -3 => "\u{207B}\u{00B3}".to_string(),
                _ => {
                    let sign = if n < 0 { "\u{207B}" } else { "" };
                    let digits: String = n
                        .unsigned_abs()
                        .to_string()
                        .chars()
                        .map(|c| match c {
                            '0' => '\u{2070}',
                            '1' => '\u{00B9}',
                            '2' => '\u{00B2}',
                            '3' => '\u{00B3}',
                            '4' => '\u{2074}',
                            '5' => '\u{2075}',
                            '6' => '\u{2076}',
                            '7' => '\u{2077}',
                            '8' => '\u{2078}',
                            '9' => '\u{2079}',
                            other => other,
                        })
                        .collect();
                    format!("{sign}{digits}")
                }
            }
        };

        let mut first = true;
        for (i, &exp) in self.0.iter().enumerate() {
            if exp == 0 {
                continue;
            }
            if !first {
                write!(f, "\u{00B7}")?; // · middle dot
            }
            write!(f, "{}{}", Self::dim_symbol(i), superscripts(exp))?;
            first = false;
        }
        Ok(())
    }
}

// -----------------------------------------------------------------------
// Error type
// -----------------------------------------------------------------------

/// Errors that can occur during dimensional analysis.
#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub enum UnitError {
    /// `Add` or `Sub` applied to operands with incompatible units.
    IncompatibleAddSub {
        /// Units of the left operand.
        left: Units,
        /// Units of the right operand.
        right: Units,
    },
    /// Transcendental function (`exp`, `ln`, `sin`, …) applied to a
    /// non-dimensionless argument.
    NonDimensionlessArgument {
        /// Name of the offending operation.
        op: &'static str,
        /// Actual units of the argument.
        got: Units,
    },
    /// `Pow` with a non-dimensionless base and a non-integer-constant exponent.
    NonRationalPower {
        /// Units of the base expression.
        base_units: Units,
    },
    /// Variable index `index` was out of range for a `var_units` slice of
    /// length `n_vars`.
    VarIndexOutOfRange {
        /// The offending variable index.
        index: usize,
        /// Length of the `var_units` slice.
        n_vars: usize,
    },
    /// Integer exponent scaling would overflow `i8`.
    ExponentOverflow {
        /// Zero-based dimension index.
        dimension: usize,
        /// Base exponent value.
        base_exp: i8,
        /// Requested integer power.
        power: i32,
    },
}

impl fmt::Display for UnitError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::IncompatibleAddSub { left, right } => {
                write!(f, "add/sub unit mismatch: {left} ≠ {right}")
            }
            Self::NonDimensionlessArgument { op, got } => {
                write!(f, "{op} requires a dimensionless argument, got {got}")
            }
            Self::NonRationalPower { base_units } => {
                write!(
                    f,
                    "Pow with dimensioned base ({base_units}) requires an integer-constant exponent"
                )
            }
            Self::VarIndexOutOfRange { index, n_vars } => {
                write!(
                    f,
                    "variable index {index} out of range (var_units has {n_vars} entries)"
                )
            }
            Self::ExponentOverflow {
                dimension,
                base_exp,
                power,
            } => {
                write!(
                    f,
                    "exponent overflow for dimension {dimension}: {base_exp} × {power} exceeds i8"
                )
            }
        }
    }
}

impl std::error::Error for UnitError {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn dimensionless_is_zero_vector() {
        assert!(Units::DIMENSIONLESS.is_dimensionless());
        assert_eq!(Units::DIMENSIONLESS.0, [0; 7]);
    }

    #[test]
    fn named_units_correct() {
        assert_eq!(Units::METER.0, [1, 0, 0, 0, 0, 0, 0]);
        assert_eq!(Units::KILOGRAM.0, [0, 1, 0, 0, 0, 0, 0]);
        assert_eq!(Units::SECOND.0, [0, 0, 1, 0, 0, 0, 0]);
    }

    #[test]
    fn mul_adds_exponents() {
        let result = Units::METER.mul(&Units::SECOND);
        assert_eq!(result.0, [1, 0, 1, 0, 0, 0, 0]);
    }

    #[test]
    fn div_subtracts_exponents() {
        let result = Units::METER.div(&Units::SECOND);
        assert_eq!(result.0, [1, 0, -1, 0, 0, 0, 0]);
    }

    #[test]
    fn pow_int_scales_exponents() {
        let result = Units::METER.pow_int(3).expect("no overflow");
        assert_eq!(result.0, [3, 0, 0, 0, 0, 0, 0]);
    }

    #[test]
    fn pow_int_overflow_returns_err() {
        let result = Units::METER.pow_int(200);
        assert!(result.is_err());
    }

    #[test]
    fn display_meter_per_second() {
        let v = Units::METER.div(&Units::SECOND);
        let s = v.to_string();
        assert!(s.contains('m'), "expected 'm' in '{s}'");
        assert!(s.contains('s'), "expected 's' in '{s}'");
    }

    #[test]
    fn display_dimensionless() {
        assert_eq!(Units::DIMENSIONLESS.to_string(), "1");
    }

    #[test]
    fn derived_newton() {
        // F = kg·m·s⁻²
        let newton = Units::KILOGRAM.mul(&Units::METER).mul(
            &Units::SECOND
                .pow_int(-2)
                .expect("pow_int(-2) does not overflow"),
        );
        assert_eq!(newton, Units::NEWTON);
    }
}
