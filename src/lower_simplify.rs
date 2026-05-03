//! Algebraic simplification for the lowered IR.
//!
//! Applies constant folding and algebraic identities to [`LoweredOp`] trees.
//! Also provides canonical pattern recognition (e.g. `sin(x)/cos(x) → tan(x)`).

use crate::lower::LoweredOp;

/// Compute a u64 structural hash of a `LoweredOp` node using `DefaultHasher`.
///
/// Used internally for structural-equality checks in the simplifier's
/// canonical pattern recognisers (e.g. `sin(x)/cos(x) → tan(x)`).
pub(crate) fn ops_struct_hash(op: &LoweredOp) -> u64 {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::Hasher;
    let mut h = DefaultHasher::new();
    op.structural_hash(&mut h);
    h.finish()
}

impl LoweredOp {
    /// Simplify the lowered operation tree.
    ///
    /// Applies constant folding and algebraic simplifications.
    pub fn simplify(&self) -> Self {
        match self {
            Self::Add(a, b) => {
                let a_s = a.simplify();
                let b_s = b.simplify();
                // 0 + x = x
                if let Self::Const(c) = &a_s {
                    if c.abs() < 1e-15 {
                        return b_s;
                    }
                }
                // x + 0 = x
                if let Self::Const(c) = &b_s {
                    if c.abs() < 1e-15 {
                        return a_s;
                    }
                }
                // const + const
                if let (Self::Const(a_c), Self::Const(b_c)) = (&a_s, &b_s) {
                    return Self::Const(a_c + b_c);
                }
                // a + (-b) = a - b
                if let Self::Neg(inner) = &b_s {
                    return Self::Sub(Box::new(a_s), inner.clone());
                }
                Self::Add(Box::new(a_s), Box::new(b_s))
            }
            Self::Sub(a, b) => {
                let a_s = a.simplify();
                let b_s = b.simplify();
                // x - 0 = x
                if let Self::Const(c) = &b_s {
                    if c.abs() < 1e-15 {
                        return a_s;
                    }
                }
                // 0 - x = -x
                if let Self::Const(c) = &a_s {
                    if c.abs() < 1e-15 {
                        return Self::Neg(Box::new(b_s));
                    }
                }
                if let (Self::Const(a_c), Self::Const(b_c)) = (&a_s, &b_s) {
                    return Self::Const(a_c - b_c);
                }
                // a - (-b) = a + b
                if let Self::Neg(inner) = &b_s {
                    return Self::Add(Box::new(a_s), inner.clone());
                }
                Self::Sub(Box::new(a_s), Box::new(b_s))
            }
            Self::Mul(a, b) => {
                let a_s = a.simplify();
                let b_s = b.simplify();
                // 0 * x = 0
                if let Self::Const(c) = &a_s {
                    if c.abs() < 1e-15 {
                        return Self::Const(0.0);
                    }
                }
                if let Self::Const(c) = &b_s {
                    if c.abs() < 1e-15 {
                        return Self::Const(0.0);
                    }
                }
                // 1 * x = x
                if let Self::Const(c) = &a_s {
                    if (*c - 1.0).abs() < 1e-15 {
                        return b_s;
                    }
                }
                if let Self::Const(c) = &b_s {
                    if (*c - 1.0).abs() < 1e-15 {
                        return a_s;
                    }
                }
                if let (Self::Const(a_c), Self::Const(b_c)) = (&a_s, &b_s) {
                    return Self::Const(a_c * b_c);
                }
                // -1 * x = -x
                if let Self::Const(c) = &a_s {
                    if (*c + 1.0).abs() < 1e-15 {
                        return Self::Neg(Box::new(b_s));
                    }
                }
                // x * -1 = -x
                if let Self::Const(c) = &b_s {
                    if (*c + 1.0).abs() < 1e-15 {
                        return Self::Neg(Box::new(a_s));
                    }
                }
                Self::Mul(Box::new(a_s), Box::new(b_s))
            }
            Self::Div(a, b) => {
                let a_s = a.simplify();
                let b_s = b.simplify();
                // x / 1 = x
                if let Self::Const(c) = &b_s {
                    if (*c - 1.0).abs() < 1e-15 {
                        return a_s;
                    }
                }
                // Canonical pattern recognizer: sin(x) / cos(x) -> tan(x)
                if let (Self::Sin(sa), Self::Cos(ca)) = (&a_s, &b_s) {
                    if ops_struct_hash(sa) == ops_struct_hash(ca) {
                        return Self::Tan(sa.clone());
                    }
                }
                // Canonical pattern recognizer: sinh(x) / cosh(x) -> tanh(x)
                if let (Self::Sinh(sa), Self::Cosh(ca)) = (&a_s, &b_s) {
                    if ops_struct_hash(sa) == ops_struct_hash(ca) {
                        return Self::Tanh(sa.clone());
                    }
                }
                // Canonical pattern recognizer: (exp(x) - exp(-x)) / 2 -> sinh(x)
                // a_s must be Sub(Exp(x), Exp(Neg(x))) and b_s must be Const(2.0)
                if let Self::Const(d) = &b_s {
                    if (*d - 2.0).abs() < 1e-15 {
                        if let Self::Sub(sub_a, sub_b) = &a_s {
                            if let (Self::Exp(ea), Self::Exp(eb)) = (sub_a.as_ref(), sub_b.as_ref())
                            {
                                if let Self::Neg(neg_inner) = eb.as_ref() {
                                    if ops_struct_hash(ea) == ops_struct_hash(neg_inner) {
                                        return Self::Sinh(ea.clone());
                                    }
                                }
                            }
                        }
                    }
                }
                // Canonical pattern recognizer: (exp(x) + exp(-x)) / 2 -> cosh(x)
                // a_s must be Add(Exp(x), Exp(Neg(x))) and b_s must be Const(2.0)
                if let Self::Const(d) = &b_s {
                    if (*d - 2.0).abs() < 1e-15 {
                        if let Self::Add(add_a, add_b) = &a_s {
                            if let (Self::Exp(ea), Self::Exp(eb)) = (add_a.as_ref(), add_b.as_ref())
                            {
                                if let Self::Neg(neg_inner) = eb.as_ref() {
                                    if ops_struct_hash(ea) == ops_struct_hash(neg_inner) {
                                        return Self::Cosh(ea.clone());
                                    }
                                }
                            }
                        }
                    }
                }
                // Constant folding (propagates NaN/Inf)
                if let (Self::Const(a_c), Self::Const(b_c)) = (&a_s, &b_s) {
                    return Self::Const(a_c / b_c);
                }
                Self::Div(Box::new(a_s), Box::new(b_s))
            }
            Self::Exp(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    if c.abs() < 1e-15 {
                        return Self::Const(1.0); // exp(0) = 1
                    }
                    // General const fold: exp(c), propagates NaN/Inf as-is
                    return Self::Const(c.exp());
                }
                // exp(ln(x)) = x
                if let Self::Ln(inner) = &a_s {
                    return *inner.clone();
                }
                Self::Exp(Box::new(a_s))
            }
            Self::Ln(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    if (*c - 1.0).abs() < 1e-15 {
                        return Self::Const(0.0); // ln(1) = 0
                    }
                    // General const fold: ln(c), propagates NaN for c <= 0
                    return Self::Const(c.ln());
                }
                // ln(exp(x)) = x
                if let Self::Exp(inner) = &a_s {
                    return *inner.clone();
                }
                Self::Ln(Box::new(a_s))
            }
            Self::Neg(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    return Self::Const(-c);
                }
                // neg(neg(x)) = x
                if let Self::Neg(inner) = &a_s {
                    return *inner.clone();
                }
                // -(a - b) = b - a
                if let Self::Sub(lhs, rhs) = &a_s {
                    return Self::Sub(rhs.clone(), lhs.clone());
                }
                Self::Neg(Box::new(a_s))
            }
            Self::Pow(a, b) => {
                let a_s = a.simplify();
                let b_s = b.simplify();
                // x^0 = 1
                if let Self::Const(c) = &b_s {
                    if c.abs() < 1e-15 {
                        return Self::Const(1.0);
                    }
                    // x^1 = x
                    if (*c - 1.0).abs() < 1e-15 {
                        return a_s;
                    }
                }
                // Constant folding: propagates NaN/Inf as-is
                if let (Self::Const(a_c), Self::Const(b_c)) = (&a_s, &b_s) {
                    return Self::Const(a_c.powf(*b_c));
                }
                Self::Pow(Box::new(a_s), Box::new(b_s))
            }
            Self::Sin(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    return Self::Const(c.sin());
                }
                // sin(arcsin(x)) -> x
                if let Self::Arcsin(inner) = &a_s {
                    return *inner.clone();
                }
                Self::Sin(Box::new(a_s))
            }
            Self::Cos(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    return Self::Const(c.cos());
                }
                // Canonical pattern recognizer: cos(arccos(x)) -> x
                if let Self::Arccos(inner) = &a_s {
                    return *inner.clone();
                }
                Self::Cos(Box::new(a_s))
            }
            Self::Tan(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    return Self::Const(c.tan());
                }
                // tan(arctan(x)) -> x
                if let Self::Arctan(inner) = &a_s {
                    return *inner.clone();
                }
                Self::Tan(Box::new(a_s))
            }
            Self::Sinh(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    return Self::Const(c.sinh());
                }
                // sinh(arcsinh(x)) -> x
                if let Self::Arcsinh(inner) = &a_s {
                    return *inner.clone();
                }
                Self::Sinh(Box::new(a_s))
            }
            Self::Cosh(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    return Self::Const(c.cosh());
                }
                // cosh(arccosh(x)) -> x
                if let Self::Arccosh(inner) = &a_s {
                    return *inner.clone();
                }
                Self::Cosh(Box::new(a_s))
            }
            Self::Tanh(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    return Self::Const(c.tanh());
                }
                // tanh(arctanh(x)) -> x
                if let Self::Arctanh(inner) = &a_s {
                    return *inner.clone();
                }
                Self::Tanh(Box::new(a_s))
            }
            Self::Arcsin(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    return Self::Const(c.asin());
                }
                Self::Arcsin(Box::new(a_s))
            }
            Self::Arccos(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    return Self::Const(c.acos());
                }
                Self::Arccos(Box::new(a_s))
            }
            Self::Arctan(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    return Self::Const(c.atan());
                }
                Self::Arctan(Box::new(a_s))
            }
            Self::Arcsinh(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    return Self::Const(c.asinh());
                }
                Self::Arcsinh(Box::new(a_s))
            }
            Self::Arccosh(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    return Self::Const(c.acosh());
                }
                Self::Arccosh(Box::new(a_s))
            }
            Self::Arctanh(a) => {
                let a_s = a.simplify();
                if let Self::Const(c) = &a_s {
                    return Self::Const(c.atanh());
                }
                Self::Arctanh(Box::new(a_s))
            }
            Self::Const(_) | Self::Var(_) | Self::NamedConst(_) => self.clone(),
        }
    }
}
