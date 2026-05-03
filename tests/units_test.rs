//! Integration tests for the dimensional-analysis / unit-aware regression feature.
//!
//! Covers:
//! - [`oxieml::units::Units`] algebra (mul, div, pow)
//! - [`oxieml::LoweredOp::check_units`] (all rule cases)
//! - [`oxieml::SymRegConfig::unit_filter`] integration with `discover_exhaustive`

use oxieml::units::{UnitError, Units};
use oxieml::{LoweredOp, SymRegConfig, SymRegEngine};

// ---------------------------------------------------------------------------
// Units algebra
// ---------------------------------------------------------------------------

#[test]
fn dimensionless_const_passes() {
    let result = LoweredOp::Const(2.0).check_units(&[]);
    assert_eq!(result, Ok(Units::DIMENSIONLESS));
}

#[test]
fn var_returns_its_units() {
    let result = LoweredOp::Var(0).check_units(&[Units::METER]);
    assert_eq!(result, Ok(Units::METER));
}

#[test]
fn add_compatible_units_ok() {
    // x0 [m] + x1 [m] → [m]
    let expr = LoweredOp::Add(Box::new(LoweredOp::Var(0)), Box::new(LoweredOp::Var(1)));
    let result = expr.check_units(&[Units::METER, Units::METER]);
    assert_eq!(result, Ok(Units::METER));
}

#[test]
fn add_incompatible_units_err() {
    // x0 [m] + x1 [s] → error
    let expr = LoweredOp::Add(Box::new(LoweredOp::Var(0)), Box::new(LoweredOp::Var(1)));
    let result = expr.check_units(&[Units::METER, Units::SECOND]);
    assert!(matches!(
        result,
        Err(UnitError::IncompatibleAddSub { left, right })
            if left == Units::METER && right == Units::SECOND
    ));
}

#[test]
fn mul_combines_units() {
    // x0 [m] * x1 [s] → [m·s]
    let expr = LoweredOp::Mul(Box::new(LoweredOp::Var(0)), Box::new(LoweredOp::Var(1)));
    let result = expr.check_units(&[Units::METER, Units::SECOND]);
    let expected = Units::new([1, 0, 1, 0, 0, 0, 0]);
    assert_eq!(result, Ok(expected));
}

#[test]
fn div_subtracts_units() {
    // x0 [m] / x1 [s] → [m/s]  = [1,0,-1,0,0,0,0]
    let expr = LoweredOp::Div(Box::new(LoweredOp::Var(0)), Box::new(LoweredOp::Var(1)));
    let result = expr.check_units(&[Units::METER, Units::SECOND]);
    let expected = Units::new([1, 0, -1, 0, 0, 0, 0]);
    assert_eq!(result, Ok(expected));
}

#[test]
fn pow_integer_scales_units() {
    // x0 [m] ^ 2 → [m²]  = [2,0,0,0,0,0,0]
    let expr = LoweredOp::Pow(Box::new(LoweredOp::Var(0)), Box::new(LoweredOp::Const(2.0)));
    let result = expr.check_units(&[Units::METER]);
    let expected = Units::new([2, 0, 0, 0, 0, 0, 0]);
    assert_eq!(result, Ok(expected));
}

#[test]
fn pow_non_integer_with_units_err() {
    // x0 [m] ^ 0.5  — non-integer exponent with dimensional base → error
    let expr = LoweredOp::Pow(Box::new(LoweredOp::Var(0)), Box::new(LoweredOp::Const(0.5)));
    let result = expr.check_units(&[Units::METER]);
    assert!(
        matches!(result, Err(UnitError::NonRationalPower { .. })),
        "expected NonRationalPower, got {result:?}"
    );
}

#[test]
fn exp_requires_dimensionless() {
    // exp(x0 [m]) → error: argument must be dimensionless
    let expr = LoweredOp::Exp(Box::new(LoweredOp::Var(0)));
    let result = expr.check_units(&[Units::METER]);
    assert!(
        matches!(
            result,
            Err(UnitError::NonDimensionlessArgument { op: "exp", .. })
        ),
        "expected NonDimensionlessArgument(exp), got {result:?}"
    );
}

#[test]
fn exp_dimensionless_ok() {
    // exp(x0 [dimensionless]) → dimensionless
    let expr = LoweredOp::Exp(Box::new(LoweredOp::Var(0)));
    let result = expr.check_units(&[Units::DIMENSIONLESS]);
    assert_eq!(result, Ok(Units::DIMENSIONLESS));
}

#[test]
fn newton_formula_checks() {
    // F = m * (v/t): Mul(Var(0), Div(Var(1), Var(2)))
    // var_units = [kg, m/s, s]  →  kg * (m/s / s) = kg * m/s² = N
    let expr = LoweredOp::Mul(
        Box::new(LoweredOp::Var(0)),
        Box::new(LoweredOp::Div(
            Box::new(LoweredOp::Var(1)),
            Box::new(LoweredOp::Var(2)),
        )),
    );
    let velocity = Units::METER.div(&Units::SECOND); // m/s
    let var_units = [Units::KILOGRAM, velocity, Units::SECOND];
    let result = expr.check_units(&var_units);
    assert_eq!(
        result,
        Ok(Units::NEWTON),
        "F = m*(v/t) should have units of Newton"
    );
}

#[test]
fn unit_filter_reduces_symreg_search() {
    // Scenario: y = x0 (identity mapping), var 0 has units of METER.
    // With unit_filter = Some(([METER], METER)), topologies that output METER
    // are retained; those that output dimensionless, SECOND, etc. are dropped.
    //
    // This test verifies:
    //   (a) unit_filter doesn't crash and returns at least one formula;
    //   (b) the filtered run returns fewer or equal formulas than the unfiltered run;
    //   (c) every returned formula is dimensionally consistent (output units == METER).
    let inputs: Vec<Vec<f64>> = (1..=10).map(|i| vec![i as f64 * 0.5]).collect();
    let targets: Vec<f64> = inputs.iter().map(|x| x[0]).collect(); // y = x0

    let config_filtered = SymRegConfig {
        max_depth: 2,
        max_iter: 200,
        num_restarts: 1,
        unit_filter: Some((vec![Units::METER], Units::METER)),
        ..SymRegConfig::default()
    };

    let config_unfiltered = SymRegConfig {
        max_depth: 2,
        max_iter: 200,
        num_restarts: 1,
        ..SymRegConfig::default()
    };

    let engine_filtered = SymRegEngine::new(config_filtered);
    let engine_unfiltered = SymRegEngine::new(config_unfiltered);

    let filtered = engine_filtered
        .discover(&inputs, &targets, 1)
        .expect("unit-filtered discover should succeed");
    let unfiltered = engine_unfiltered
        .discover(&inputs, &targets, 1)
        .expect("unfiltered discover should succeed");

    // (a) unit filter must still yield at least one formula (the identity Var(0) is METER)
    assert!(
        !filtered.is_empty(),
        "unit filter should still yield formulas: the identity topology Var(0) has units METER"
    );

    // (b) filtered run should produce no more formulas than the unfiltered run
    assert!(
        filtered.len() <= unfiltered.len(),
        "unit filter should reduce or equal the formula count: filtered={}, unfiltered={}",
        filtered.len(),
        unfiltered.len()
    );

    // (c) every returned formula must have output units == METER
    for formula in &filtered {
        let lowered = formula.eml_tree.lower().simplify();
        let units = lowered.check_units(&[Units::METER]);
        assert_eq!(
            units,
            Ok(Units::METER),
            "formula '{}' should have METER output units, got {units:?}",
            formula.pretty
        );
    }
}

#[test]
fn units_to_string_meter_per_second() {
    let v = Units::METER.div(&Units::SECOND);
    let s = v.to_string();
    assert!(s.contains('m'), "expected 'm' in unit string '{s}'");
    assert!(s.contains('s'), "expected 's' in unit string '{s}'");
}

#[test]
fn var_index_out_of_range_err() {
    // Var(5) with only 1 unit supplied → VarIndexOutOfRange
    let result = LoweredOp::Var(5).check_units(&[Units::METER]);
    assert!(
        matches!(
            result,
            Err(UnitError::VarIndexOutOfRange {
                index: 5,
                n_vars: 1
            })
        ),
        "expected VarIndexOutOfRange, got {result:?}"
    );
}

// ---------------------------------------------------------------------------
// Additional checks: all transcendentals, negation, Sub, NamedConst
// ---------------------------------------------------------------------------

#[test]
fn sub_compatible_units_ok() {
    let expr = LoweredOp::Sub(Box::new(LoweredOp::Var(0)), Box::new(LoweredOp::Var(1)));
    let result = expr.check_units(&[Units::KILOGRAM, Units::KILOGRAM]);
    assert_eq!(result, Ok(Units::KILOGRAM));
}

#[test]
fn neg_preserves_units() {
    let expr = LoweredOp::Neg(Box::new(LoweredOp::Var(0)));
    let result = expr.check_units(&[Units::METER]);
    assert_eq!(result, Ok(Units::METER));
}

#[test]
fn ln_requires_dimensionless() {
    let expr = LoweredOp::Ln(Box::new(LoweredOp::Var(0)));
    let result = expr.check_units(&[Units::SECOND]);
    assert!(
        matches!(
            result,
            Err(UnitError::NonDimensionlessArgument { op: "ln", .. })
        ),
        "expected NonDimensionlessArgument(ln), got {result:?}"
    );
}

#[test]
fn sin_requires_dimensionless() {
    let expr = LoweredOp::Sin(Box::new(LoweredOp::Var(0)));
    let result = expr.check_units(&[Units::AMPERE]);
    assert!(
        matches!(
            result,
            Err(UnitError::NonDimensionlessArgument { op: "sin", .. })
        ),
        "expected NonDimensionlessArgument(sin), got {result:?}"
    );
}

#[test]
fn pow_with_symbolic_exponent_and_units_err() {
    // x0 [m] ^ x1 [dimensionless but non-const] → NonRationalPower
    let expr = LoweredOp::Pow(Box::new(LoweredOp::Var(0)), Box::new(LoweredOp::Var(1)));
    let result = expr.check_units(&[Units::METER, Units::DIMENSIONLESS]);
    assert!(
        matches!(result, Err(UnitError::NonRationalPower { .. })),
        "expected NonRationalPower for symbolic exponent with dimensioned base, got {result:?}"
    );
}

#[test]
fn pow_dimensionless_base_any_exponent_ok() {
    // dimensionless ^ x1 [dimensionless] → DIMENSIONLESS
    let expr = LoweredOp::Pow(Box::new(LoweredOp::Var(0)), Box::new(LoweredOp::Var(1)));
    let result = expr.check_units(&[Units::DIMENSIONLESS, Units::DIMENSIONLESS]);
    assert_eq!(result, Ok(Units::DIMENSIONLESS));
}

#[test]
fn named_const_is_dimensionless() {
    use oxieml::NamedConst;
    let expr = LoweredOp::NamedConst(NamedConst::Pi);
    let result = expr.check_units(&[]);
    assert_eq!(result, Ok(Units::DIMENSIONLESS));
}

#[test]
fn unit_filter_none_is_default() {
    let config = SymRegConfig::default();
    assert!(
        config.unit_filter.is_none(),
        "unit_filter must default to None"
    );
}
