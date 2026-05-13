//! Symbolic equation solving for `LoweredOp` expression trees.
//!
//! Given an equation `f(x) == rhs`, [`LoweredOp::solve_for`] attempts to derive
//! a closed-form expression for the target variable by recursively applying
//! algebraic inversion rules (inverse operations for +, -, *, /, exp, ln, trig, pow).
//!
//! When no closed-form inversion is possible (e.g. `x + sin(x) == 1`) the method
//! returns the residual `f - rhs` which can be used for numeric root-finding.

use crate::lower::LoweredOp;

/// Result of symbolically solving `f(x) == rhs` for a target variable.
#[derive(Debug, Clone)]
pub enum SolveResult {
    /// Closed-form solution: the expression for the target variable.
    ///
    /// Evaluate this with the *other* variables' values to get the target
    /// variable's value. For example, solving `2*x + 3 == 7` yields
    /// `Closed(Const(2.0))`.
    Closed(LoweredOp),

    /// Could not find a closed-form solution.
    ///
    /// The residual `f(x) - rhs` can be passed to a numeric root-finder.
    /// For example, `x + sin(x) == 1` is not algebraically invertible and
    /// yields `Residual(x + sin(x) - 1)`.
    Residual(LoweredOp),
}

impl LoweredOp {
    /// Returns `true` if this expression tree contains `Var(var)` anywhere.
    ///
    /// Used by [`solve_for`](Self::solve_for) to determine which branch of a
    /// binary node contains the target variable before attempting inversion.
    pub fn contains_var(&self, var: usize) -> bool {
        match self {
            Self::Var(i) => *i == var,
            Self::Const(_) | Self::NamedConst(_) => false,
            // Unary nodes: check the child.
            Self::Neg(x) | Self::Conj(x)
            | Self::Sin(x)
            | Self::Cos(x)
            | Self::Tan(x)
            | Self::Sinh(x)
            | Self::Cosh(x)
            | Self::Tanh(x)
            | Self::Arcsin(x)
            | Self::Arccos(x)
            | Self::Arctan(x)
            | Self::Arcsinh(x)
            | Self::Arccosh(x)
            | Self::Arctanh(x)
            | Self::Exp(x)
            | Self::Ln(x) => x.contains_var(var),
            // Binary nodes: check either branch.
            Self::Add(a, b)
            | Self::Sub(a, b)
            | Self::Mul(a, b)
            | Self::Div(a, b)
            | Self::Pow(a, b) => a.contains_var(var) || b.contains_var(var),
        }
    }

    /// Symbolically solve `self == rhs` for the given target variable.
    ///
    /// Applies algebraic inversion rules recursively. Returns
    /// [`SolveResult::Closed`] when a closed-form solution can be derived, or
    /// [`SolveResult::Residual`]`(self − rhs)` when no algebraic inversion is
    /// known (e.g. both operands contain the target variable, or the function
    /// has no elementary inverse in a simple form).
    ///
    /// Only the *principal branch* is returned for multi-valued inverses (e.g.
    /// `arcsin` for `sin`).
    ///
    /// # Example
    ///
    /// ```
    /// use oxieml::lower::LoweredOp;
    /// use oxieml::SolveResult;
    ///
    /// // Solve 2*x + 3 == 7  →  x == 2
    /// let expr = LoweredOp::Add(
    ///     Box::new(LoweredOp::Mul(
    ///         Box::new(LoweredOp::Const(2.0)),
    ///         Box::new(LoweredOp::Var(0)),
    ///     )),
    ///     Box::new(LoweredOp::Const(3.0)),
    /// );
    /// let rhs = LoweredOp::Const(7.0);
    /// let result = expr.solve_for(0, &rhs);
    /// assert!(matches!(result, SolveResult::Closed(_)));
    /// if let SolveResult::Closed(solution) = result {
    ///     assert!((solution.eval(&[]) - 2.0).abs() < 1e-10);
    /// }
    /// ```
    pub fn solve_for(&self, target_var: usize, rhs: &LoweredOp) -> SolveResult {
        self.solve_inner(target_var, rhs.clone())
    }

    /// Recursive implementation of `solve_for`.
    ///
    /// Invariant at each call: we are solving `self == rhs` for `target_var`.
    /// The method rewrites the equation, moving nodes from `self` to `rhs`
    /// (applying the inverse operation) until `self` is exactly `Var(target_var)`.
    fn solve_inner(&self, target_var: usize, rhs: LoweredOp) -> SolveResult {
        match self {
            // ---- Base cases -----------------------------------------------

            // Isolated the variable: return the accumulated rhs as the solution.
            Self::Var(i) if *i == target_var => SolveResult::Closed(rhs.simplify()),

            // This subtree does not contain the target variable at all.
            // The equation degenerates to a constant identity; return residual.
            _ if !self.contains_var(target_var) => SolveResult::Residual(
                LoweredOp::Sub(Box::new(self.clone()), Box::new(rhs)).simplify(),
            ),

            // ---- Unary operators ------------------------------------------

            // −x == rhs  →  x == −rhs
            Self::Neg(x) | Self::Conj(x) => x.solve_inner(target_var, LoweredOp::Neg(Box::new(rhs)).simplify()),

            // exp(x) == rhs  →  x == ln(rhs)
            Self::Exp(x) => x.solve_inner(target_var, LoweredOp::Ln(Box::new(rhs)).simplify()),

            // ln(x) == rhs  →  x == exp(rhs)
            Self::Ln(x) => x.solve_inner(target_var, LoweredOp::Exp(Box::new(rhs)).simplify()),

            // sin(x) == rhs  →  x == arcsin(rhs)  (principal branch)
            Self::Sin(x) => x.solve_inner(target_var, LoweredOp::Arcsin(Box::new(rhs)).simplify()),

            // cos(x) == rhs  →  x == arccos(rhs)  (principal branch)
            Self::Cos(x) => x.solve_inner(target_var, LoweredOp::Arccos(Box::new(rhs)).simplify()),

            // tan(x) == rhs  →  x == arctan(rhs)
            Self::Tan(x) => x.solve_inner(target_var, LoweredOp::Arctan(Box::new(rhs)).simplify()),

            // sinh(x) == rhs  →  x == arcsinh(rhs)
            Self::Sinh(x) => {
                x.solve_inner(target_var, LoweredOp::Arcsinh(Box::new(rhs)).simplify())
            }

            // cosh(x) == rhs  →  x == arccosh(rhs)  (principal branch, rhs ≥ 1)
            Self::Cosh(x) => {
                x.solve_inner(target_var, LoweredOp::Arccosh(Box::new(rhs)).simplify())
            }

            // tanh(x) == rhs  →  x == arctanh(rhs)
            Self::Tanh(x) => {
                x.solve_inner(target_var, LoweredOp::Arctanh(Box::new(rhs)).simplify())
            }

            // arcsin(x) == rhs  →  x == sin(rhs)
            Self::Arcsin(x) => x.solve_inner(target_var, LoweredOp::Sin(Box::new(rhs)).simplify()),

            // arccos(x) == rhs  →  x == cos(rhs)
            Self::Arccos(x) => x.solve_inner(target_var, LoweredOp::Cos(Box::new(rhs)).simplify()),

            // arctan(x) == rhs  →  x == tan(rhs)
            Self::Arctan(x) => x.solve_inner(target_var, LoweredOp::Tan(Box::new(rhs)).simplify()),

            // arcsinh(x) == rhs  →  x == sinh(rhs)
            Self::Arcsinh(x) => {
                x.solve_inner(target_var, LoweredOp::Sinh(Box::new(rhs)).simplify())
            }

            // arccosh(x) == rhs  →  x == cosh(rhs)
            Self::Arccosh(x) => {
                x.solve_inner(target_var, LoweredOp::Cosh(Box::new(rhs)).simplify())
            }

            // arctanh(x) == rhs  →  x == tanh(rhs)
            Self::Arctanh(x) => {
                x.solve_inner(target_var, LoweredOp::Tanh(Box::new(rhs)).simplify())
            }

            // ---- Binary operators -----------------------------------------

            // a + b == rhs
            Self::Add(a, b) => {
                if a.contains_var(target_var) && !b.contains_var(target_var) {
                    // a == rhs − b
                    a.solve_inner(
                        target_var,
                        LoweredOp::Sub(Box::new(rhs), b.clone()).simplify(),
                    )
                } else if b.contains_var(target_var) && !a.contains_var(target_var) {
                    // b == rhs − a
                    b.solve_inner(
                        target_var,
                        LoweredOp::Sub(Box::new(rhs), a.clone()).simplify(),
                    )
                } else {
                    // Both contain target_var — cannot invert algebraically.
                    SolveResult::Residual(
                        LoweredOp::Sub(Box::new(self.clone()), Box::new(rhs)).simplify(),
                    )
                }
            }

            // a − b == rhs
            Self::Sub(a, b) => {
                if a.contains_var(target_var) && !b.contains_var(target_var) {
                    // a == rhs + b
                    a.solve_inner(
                        target_var,
                        LoweredOp::Add(Box::new(rhs), b.clone()).simplify(),
                    )
                } else if b.contains_var(target_var) && !a.contains_var(target_var) {
                    // −b == rhs − a  →  b == a − rhs
                    b.solve_inner(
                        target_var,
                        LoweredOp::Sub(a.clone(), Box::new(rhs)).simplify(),
                    )
                } else {
                    SolveResult::Residual(
                        LoweredOp::Sub(Box::new(self.clone()), Box::new(rhs)).simplify(),
                    )
                }
            }

            // a * b == rhs
            Self::Mul(a, b) => {
                if a.contains_var(target_var) && !b.contains_var(target_var) {
                    // a == rhs / b
                    a.solve_inner(
                        target_var,
                        LoweredOp::Div(Box::new(rhs), b.clone()).simplify(),
                    )
                } else if b.contains_var(target_var) && !a.contains_var(target_var) {
                    // b == rhs / a
                    b.solve_inner(
                        target_var,
                        LoweredOp::Div(Box::new(rhs), a.clone()).simplify(),
                    )
                } else {
                    SolveResult::Residual(
                        LoweredOp::Sub(Box::new(self.clone()), Box::new(rhs)).simplify(),
                    )
                }
            }

            // a / b == rhs
            Self::Div(a, b) => {
                if a.contains_var(target_var) && !b.contains_var(target_var) {
                    // a == rhs * b
                    a.solve_inner(
                        target_var,
                        LoweredOp::Mul(Box::new(rhs), b.clone()).simplify(),
                    )
                } else if b.contains_var(target_var) && !a.contains_var(target_var) {
                    // a / b == rhs  →  b == a / rhs
                    b.solve_inner(
                        target_var,
                        LoweredOp::Div(a.clone(), Box::new(rhs)).simplify(),
                    )
                } else {
                    SolveResult::Residual(
                        LoweredOp::Sub(Box::new(self.clone()), Box::new(rhs)).simplify(),
                    )
                }
            }

            // base^exp == rhs
            Self::Pow(base, exp) => {
                if base.contains_var(target_var) && !exp.contains_var(target_var) {
                    // base == rhs^(1/exp)
                    let inv_exp = LoweredOp::Div(Box::new(LoweredOp::Const(1.0)), exp.clone());
                    base.solve_inner(
                        target_var,
                        LoweredOp::Pow(Box::new(rhs), Box::new(inv_exp)).simplify(),
                    )
                } else if exp.contains_var(target_var) && !base.contains_var(target_var) {
                    // base^exp == rhs  →  exp == ln(rhs) / ln(base)
                    let ln_rhs = LoweredOp::Ln(Box::new(rhs));
                    let ln_base = LoweredOp::Ln(base.clone());
                    exp.solve_inner(
                        target_var,
                        LoweredOp::Div(Box::new(ln_rhs), Box::new(ln_base)).simplify(),
                    )
                } else {
                    SolveResult::Residual(
                        LoweredOp::Sub(Box::new(self.clone()), Box::new(rhs)).simplify(),
                    )
                }
            }

            // Fallback for any variant not covered above (e.g. Var(i) where i != target_var
            // that somehow passed the contains_var guard — should not occur in practice).
            _ => SolveResult::Residual(
                LoweredOp::Sub(Box::new(self.clone()), Box::new(rhs)).simplify(),
            ),
        }
    }
}
