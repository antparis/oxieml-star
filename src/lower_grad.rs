//! Symbolic differentiation for the lowered IR.
//!
//! Implements partial derivatives, Jacobian, and Hessian for [`LoweredOp`]
//! trees via the chain rule and standard calculus identities.

use crate::lower::LoweredOp;

impl LoweredOp {
    /// Symbolic partial derivative of this operation tree with respect to
    /// variable `wrt`.
    ///
    /// Applies standard calculus rules (sum, product, quotient, chain) to
    /// every variant of [`LoweredOp`] and returns a new `LoweredOp`
    /// representing the derivative. The result is post-processed via
    /// [`LoweredOp::simplify`] so that constant folding and 0/1 identities
    /// collapse trivial subterms.
    ///
    /// # Variables
    ///
    /// Variables are indexed from 0. `Var(i).grad(v)` is `Const(1.0)` when
    /// `i == v` and `Const(0.0)` otherwise.
    ///
    /// # `Pow`
    ///
    /// The general power rule is used (both base and exponent may depend on
    /// any variable). Concretely,
    /// `d/dx base^expo = base^expo · (expo'·ln(base) + expo·base'/base)`.
    /// For constant exponents this simplifies to the familiar
    /// `n·base^(n-1)·base'` after [`LoweredOp::simplify`] — but because the
    /// current simplifier does not perform algebraic cancellation, the
    /// surface form may keep the generic shape.
    ///
    /// # Examples
    ///
    /// ```
    /// use oxieml::LoweredOp;
    ///
    /// // f(x, y) = x * y, df/dx = y
    /// let op = LoweredOp::Mul(
    ///     Box::new(LoweredOp::Var(0)),
    ///     Box::new(LoweredOp::Var(1)),
    /// );
    /// let df_dx = op.grad(0);
    /// assert!((df_dx.eval(&[3.0, 5.0]) - 5.0).abs() < 1e-12);
    /// ```
    pub fn grad(&self, wrt: usize) -> Self {
        raw_grad(self, wrt).simplify()
    }

    /// Count the number of distinct variable indices present in this tree.
    ///
    /// Returns `max(i) + 1` over all `Var(i)` nodes, or `0` if no `Var`
    /// nodes exist. This gives the minimum variable vector length required
    /// for a valid [`eval`](Self::eval) call.
    pub fn count_vars(&self) -> usize {
        match self {
            Self::Const(_) | Self::NamedConst(_) => 0,
            Self::Var(i) => i + 1,
            Self::Neg(x)
            | Self::Conj(x)
            | Self::Exp(x)
            | Self::Ln(x)
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
            | Self::Arctanh(x) => x.count_vars(),
            Self::Add(a, b)
            | Self::Sub(a, b)
            | Self::Mul(a, b)
            | Self::Div(a, b)
            | Self::Pow(a, b) => a.count_vars().max(b.count_vars()),
        }
    }

    /// Compute the vector of partial derivatives `[∂f/∂x0, ∂f/∂x1, …]`.
    ///
    /// Calls [`grad`](Self::grad) for each index `0..count_vars()` and
    /// simplifies each result.
    pub fn grad_all(&self) -> Vec<Self> {
        let n = self.count_vars();
        (0..n).map(|i| self.grad(i).simplify()).collect()
    }

    /// Return the Jacobian row for this scalar expression with exactly
    /// `n_vars` columns.
    ///
    /// If `n_vars > count_vars()` the vector is padded with `Const(0.0)`.
    /// If `n_vars < count_vars()` the vector is truncated.
    pub fn jacobian(&self, n_vars: usize) -> Vec<Self> {
        let mut grads = self.grad_all();
        while grads.len() < n_vars {
            grads.push(Self::Const(0.0));
        }
        grads.truncate(n_vars);
        grads
    }

    /// Compute the Hessian matrix of second-order partial derivatives.
    ///
    /// Returns an `n_vars × n_vars` matrix where `H[i][j] = ∂²f / ∂xi ∂xj`.
    /// Only the upper triangle is computed (O(n²·|tree|) complexity), then
    /// mirrored to the lower triangle exploiting Schwarz's symmetry theorem.
    pub fn hessian(&self, n_vars: usize) -> Vec<Vec<Self>> {
        let jac = self.jacobian(n_vars);
        // Collect upper-triangle (i, j, entry) tuples first, then assign.
        // This avoids the needless-range-loop lint that fires when `j` is
        // used both for `grad(j)` and for double-indexing `h[i][j]`/`h[j][i]`.
        let upper: Vec<(usize, usize, Self)> = jac
            .iter()
            .enumerate()
            .flat_map(|(i, jac_row)| (i..n_vars).map(move |j| (i, j, jac_row.grad(j).simplify())))
            .collect();
        let mut h = vec![vec![Self::Const(0.0); n_vars]; n_vars];
        for (i, j, entry) in upper {
            // Exploit Schwarz symmetry: H[i][j] == H[j][i].
            h[i][j] = entry.clone();
            h[j][i] = entry;
        }
        h
    }
}

/// Build the raw (un-simplified) symbolic derivative of `op` with respect to
/// variable `wrt`.
///
/// Callers should always route through [`LoweredOp::grad`], which applies
/// [`LoweredOp::simplify`] on the result. This helper exists so the rewrite
/// rules are easy to read and test in isolation.
pub(crate) fn raw_grad(op: &LoweredOp, wrt: usize) -> LoweredOp {
    match op {
        LoweredOp::Const(_) | LoweredOp::NamedConst(_) => LoweredOp::Const(0.0),
        LoweredOp::Var(i) => {
            if *i == wrt {
                LoweredOp::Const(1.0)
            } else {
                LoweredOp::Const(0.0)
            }
        }
        LoweredOp::Add(a, b) => {
            LoweredOp::Add(Box::new(raw_grad(a, wrt)), Box::new(raw_grad(b, wrt)))
        }
        LoweredOp::Sub(a, b) => {
            LoweredOp::Sub(Box::new(raw_grad(a, wrt)), Box::new(raw_grad(b, wrt)))
        }
        LoweredOp::Mul(a, b) => {
            // (a·b)' = a'·b + a·b'
            let da = raw_grad(a, wrt);
            let db = raw_grad(b, wrt);
            LoweredOp::Add(
                Box::new(LoweredOp::Mul(Box::new(da), b.clone())),
                Box::new(LoweredOp::Mul(a.clone(), Box::new(db))),
            )
        }
        LoweredOp::Div(a, b) => {
            // (a/b)' = (a'·b - a·b') / (b·b)
            let da = raw_grad(a, wrt);
            let db = raw_grad(b, wrt);
            let num = LoweredOp::Sub(
                Box::new(LoweredOp::Mul(Box::new(da), b.clone())),
                Box::new(LoweredOp::Mul(a.clone(), Box::new(db))),
            );
            let denom = LoweredOp::Mul(b.clone(), b.clone());
            LoweredOp::Div(Box::new(num), Box::new(denom))
        }
        LoweredOp::Exp(a) => {
            // d/dx exp(f) = exp(f) · f'
            let da = raw_grad(a, wrt);
            LoweredOp::Mul(Box::new(LoweredOp::Exp(a.clone())), Box::new(da))
        }
        LoweredOp::Ln(a) => {
            // d/dx ln(f) = f' / f
            let da = raw_grad(a, wrt);
            LoweredOp::Div(Box::new(da), a.clone())
        }
        LoweredOp::Sin(a) => {
            // d/dx sin(f) = cos(f) · f'
            let da = raw_grad(a, wrt);
            LoweredOp::Mul(Box::new(LoweredOp::Cos(a.clone())), Box::new(da))
        }
        LoweredOp::Cos(a) => {
            // d/dx cos(f) = -sin(f) · f'
            let da = raw_grad(a, wrt);
            LoweredOp::Neg(Box::new(LoweredOp::Mul(
                Box::new(LoweredOp::Sin(a.clone())),
                Box::new(da),
            )))
        }
        LoweredOp::Neg(a) | LoweredOp::Conj(a) => LoweredOp::Neg(Box::new(raw_grad(a, wrt))),
        LoweredOp::Pow(base, expo) => {
            // General power rule via exp-log rewriting:
            //   d/dx base^expo
            //     = base^expo · (expo' · ln(base) + expo · base' / base)
            let base_grad = raw_grad(base, wrt);
            let expo_grad = raw_grad(expo, wrt);
            let bracket = LoweredOp::Add(
                Box::new(LoweredOp::Mul(
                    Box::new(expo_grad),
                    Box::new(LoweredOp::Ln(base.clone())),
                )),
                Box::new(LoweredOp::Div(
                    Box::new(LoweredOp::Mul(expo.clone(), Box::new(base_grad))),
                    base.clone(),
                )),
            );
            LoweredOp::Mul(
                Box::new(LoweredOp::Pow(base.clone(), expo.clone())),
                Box::new(bracket),
            )
        }
        LoweredOp::Tan(a) => {
            // d/dx tan(f) = (1 + tan²(f)) · f'
            let da = raw_grad(a, wrt);
            let tan_sq = LoweredOp::Mul(
                Box::new(LoweredOp::Tan(a.clone())),
                Box::new(LoweredOp::Tan(a.clone())),
            );
            let one_plus_tan_sq = LoweredOp::Add(Box::new(LoweredOp::Const(1.0)), Box::new(tan_sq));
            LoweredOp::Mul(Box::new(one_plus_tan_sq), Box::new(da))
        }
        LoweredOp::Sinh(a) => {
            // d/dx sinh(f) = cosh(f) · f'
            let da = raw_grad(a, wrt);
            LoweredOp::Mul(Box::new(LoweredOp::Cosh(a.clone())), Box::new(da))
        }
        LoweredOp::Cosh(a) => {
            // d/dx cosh(f) = sinh(f) · f'
            let da = raw_grad(a, wrt);
            LoweredOp::Mul(Box::new(LoweredOp::Sinh(a.clone())), Box::new(da))
        }
        LoweredOp::Tanh(a) => {
            // d/dx tanh(f) = (1 - tanh²(f)) · f'
            let da = raw_grad(a, wrt);
            let tanh_sq = LoweredOp::Pow(
                Box::new(LoweredOp::Tanh(a.clone())),
                Box::new(LoweredOp::Const(2.0)),
            );
            let one_minus_tanh_sq =
                LoweredOp::Sub(Box::new(LoweredOp::Const(1.0)), Box::new(tanh_sq));
            LoweredOp::Mul(Box::new(one_minus_tanh_sq), Box::new(da))
        }
        LoweredOp::Arcsin(a) => {
            // d/dx arcsin(f) = 1 / sqrt(1 - f²) · f'
            let da = raw_grad(a, wrt);
            let f_sq = LoweredOp::Pow(a.clone(), Box::new(LoweredOp::Const(2.0)));
            let one_minus_fsq = LoweredOp::Sub(Box::new(LoweredOp::Const(1.0)), Box::new(f_sq));
            let denom = LoweredOp::Pow(Box::new(one_minus_fsq), Box::new(LoweredOp::Const(0.5)));
            let deriv = LoweredOp::Div(Box::new(LoweredOp::Const(1.0)), Box::new(denom));
            LoweredOp::Mul(Box::new(deriv), Box::new(da))
        }
        LoweredOp::Arccos(a) => {
            // d/dx arccos(f) = -1 / sqrt(1 - f²) · f'
            let da = raw_grad(a, wrt);
            let f_sq = LoweredOp::Pow(a.clone(), Box::new(LoweredOp::Const(2.0)));
            let one_minus_fsq = LoweredOp::Sub(Box::new(LoweredOp::Const(1.0)), Box::new(f_sq));
            let denom = LoweredOp::Pow(Box::new(one_minus_fsq), Box::new(LoweredOp::Const(0.5)));
            let neg_deriv = LoweredOp::Neg(Box::new(LoweredOp::Div(
                Box::new(LoweredOp::Const(1.0)),
                Box::new(denom),
            )));
            LoweredOp::Mul(Box::new(neg_deriv), Box::new(da))
        }
        LoweredOp::Arctan(a) => {
            // d/dx arctan(f) = 1 / (1 + f²) · f'
            let da = raw_grad(a, wrt);
            let f_sq = LoweredOp::Pow(a.clone(), Box::new(LoweredOp::Const(2.0)));
            let one_plus_fsq = LoweredOp::Add(Box::new(LoweredOp::Const(1.0)), Box::new(f_sq));
            let deriv = LoweredOp::Div(Box::new(LoweredOp::Const(1.0)), Box::new(one_plus_fsq));
            LoweredOp::Mul(Box::new(deriv), Box::new(da))
        }
        LoweredOp::Arcsinh(a) => {
            // d/dx arcsinh(f) = 1 / sqrt(1 + f²) · f'
            let da = raw_grad(a, wrt);
            let f_sq = LoweredOp::Pow(a.clone(), Box::new(LoweredOp::Const(2.0)));
            let one_plus_fsq = LoweredOp::Add(Box::new(LoweredOp::Const(1.0)), Box::new(f_sq));
            let denom = LoweredOp::Pow(Box::new(one_plus_fsq), Box::new(LoweredOp::Const(0.5)));
            let deriv = LoweredOp::Div(Box::new(LoweredOp::Const(1.0)), Box::new(denom));
            LoweredOp::Mul(Box::new(deriv), Box::new(da))
        }
        LoweredOp::Arccosh(a) => {
            // d/dx arccosh(f) = 1 / sqrt(f² - 1) · f'
            let da = raw_grad(a, wrt);
            let f_sq = LoweredOp::Pow(a.clone(), Box::new(LoweredOp::Const(2.0)));
            let fsq_minus_one = LoweredOp::Sub(Box::new(f_sq), Box::new(LoweredOp::Const(1.0)));
            let denom = LoweredOp::Pow(Box::new(fsq_minus_one), Box::new(LoweredOp::Const(0.5)));
            let deriv = LoweredOp::Div(Box::new(LoweredOp::Const(1.0)), Box::new(denom));
            LoweredOp::Mul(Box::new(deriv), Box::new(da))
        }
        LoweredOp::Arctanh(a) => {
            // d/dx arctanh(f) = 1 / (1 - f²) · f'
            let da = raw_grad(a, wrt);
            let f_sq = LoweredOp::Pow(a.clone(), Box::new(LoweredOp::Const(2.0)));
            let one_minus_fsq = LoweredOp::Sub(Box::new(LoweredOp::Const(1.0)), Box::new(f_sq));
            let deriv = LoweredOp::Div(Box::new(LoweredOp::Const(1.0)), Box::new(one_minus_fsq));
            LoweredOp::Mul(Box::new(deriv), Box::new(da))
        }
    }
}
