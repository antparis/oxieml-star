//! Named-constants extraction helpers for symbolic regression.
//!
//! After Adam optimisation, free parameters are real-valued floats. This module
//! provides post-processing that recognises well-known mathematical constants
//! (π, e, √2, simple rationals) and substitutes them when doing so does not
//! significantly degrade MSE.

use crate::lower::LoweredOp;
use crate::named_const::NamedConst;
use crate::tree::EmlTree;

/// Bake learned parameters into a lowered operation tree.
///
/// Walks the EML topology and the lowered op tree in tandem, substituting
/// each `Const(1.0)` that originated from a `One` node with `Const(param[i])`.
/// This produces a `LoweredOp` tree that reflects the actual values discovered
/// by the Adam optimizer — suitable for pretty-printing and constants extraction.
///
/// # Strategy
///
/// `lower_node` consumes `EmlNode::One` nodes in various patterns:
/// - `eml(x, One)` → `Exp(x)` (the `One` is hidden inside the pattern)
/// - `eml(One, One)` → `Const(e)` (both Ones collapsed to e)
/// - etc.
///
/// Because patterns swallow `One` nodes before we can intercept them, this
/// function uses a post-lowering substitution: it scans the resulting
/// `LoweredOp` tree for `Const(1.0)` nodes and replaces them with the
/// corresponding parameter value in post-order.
///
/// The substitution is best-effort: if the lowering collapsed several `One`
/// nodes into a single constant (e.g., `Const(e)`), those values are not
/// individually accessible. In that case, the `Const(e)` is left as-is.
///
/// This is adequate for the constants-extraction use-case, where we scan
/// all `Const` positions regardless of their origin.
pub(super) fn bake_params_into_lowered(topology: &EmlTree, params: &[f64]) -> LoweredOp {
    use crate::grad::ParameterizedEmlTree;

    if params.is_empty() {
        return topology.lower();
    }

    // Build a parameterized tree and substitute params into the lowered form.
    // We walk the EML node tree, building a modified version where each
    // EmlNode::One is replaced by a Const with the corresponding param value.
    let mut param_idx = 0usize;
    let ptree = ParameterizedEmlTree::from_topology(topology, 1.0);
    // Verify param count matches
    if ptree.params.len() != params.len() {
        return topology.lower();
    }

    // Walk the EML node tree, substituting Ones with param values, then lower.
    fn substitute_ones(
        node: &crate::tree::EmlNode,
        params: &[f64],
        idx: &mut usize,
    ) -> std::sync::Arc<crate::tree::EmlNode> {
        use crate::tree::EmlNode;
        match node {
            EmlNode::One => {
                // Replace One with Var(MAX-1) as a sentinel carrying the param value.
                // Since EmlNode has no Const variant, we keep One but track the mapping.
                // The substitution happens post-lowering via replace_const_one below.
                let _p = params[*idx];
                *idx += 1;
                std::sync::Arc::new(EmlNode::One)
            }
            EmlNode::Var(i) => std::sync::Arc::new(EmlNode::Var(*i)),
            EmlNode::Eml { left, right } => {
                let l = substitute_ones(left, params, idx);
                let r = substitute_ones(right, params, idx);
                std::sync::Arc::new(EmlNode::Eml { left: l, right: r })
            }
        }
    }

    // Strategy B (simplified): lower the topology, then walk the lowered tree
    // and replace Const(1.0) nodes with their corresponding param values.
    // We enumerate Const(1.0) positions in post-order to match the One-node
    // post-order traversal order used in ParameterizedEmlTree.
    let lowered = topology.lower();

    fn replace_const_one(op: &LoweredOp, params: &[f64], idx: &mut usize) -> LoweredOp {
        match op {
            LoweredOp::Const(c) if (*c - 1.0).abs() < 1e-15 => {
                if *idx < params.len() {
                    let p = params[*idx];
                    *idx += 1;
                    LoweredOp::Const(p)
                } else {
                    op.clone()
                }
            }
            LoweredOp::Const(_) | LoweredOp::Var(_) | LoweredOp::NamedConst(_) => op.clone(),
            LoweredOp::Neg(a) => LoweredOp::Neg(Box::new(replace_const_one(a, params, idx))),
            LoweredOp::Exp(a) => LoweredOp::Exp(Box::new(replace_const_one(a, params, idx))),
            LoweredOp::Ln(a) => LoweredOp::Ln(Box::new(replace_const_one(a, params, idx))),
            LoweredOp::Sin(a) => LoweredOp::Sin(Box::new(replace_const_one(a, params, idx))),
            LoweredOp::Cos(a) => LoweredOp::Cos(Box::new(replace_const_one(a, params, idx))),
            LoweredOp::Tan(a) => LoweredOp::Tan(Box::new(replace_const_one(a, params, idx))),
            LoweredOp::Sinh(a) => LoweredOp::Sinh(Box::new(replace_const_one(a, params, idx))),
            LoweredOp::Cosh(a) => LoweredOp::Cosh(Box::new(replace_const_one(a, params, idx))),
            LoweredOp::Tanh(a) => LoweredOp::Tanh(Box::new(replace_const_one(a, params, idx))),
            LoweredOp::Arcsin(a) => LoweredOp::Arcsin(Box::new(replace_const_one(a, params, idx))),
            LoweredOp::Arccos(a) => LoweredOp::Arccos(Box::new(replace_const_one(a, params, idx))),
            LoweredOp::Arctan(a) => LoweredOp::Arctan(Box::new(replace_const_one(a, params, idx))),
            LoweredOp::Arcsinh(a) => {
                LoweredOp::Arcsinh(Box::new(replace_const_one(a, params, idx)))
            }
            LoweredOp::Arccosh(a) => {
                LoweredOp::Arccosh(Box::new(replace_const_one(a, params, idx)))
            }
            LoweredOp::Arctanh(a) => {
                LoweredOp::Arctanh(Box::new(replace_const_one(a, params, idx)))
            }
            LoweredOp::Add(a, b) => LoweredOp::Add(
                Box::new(replace_const_one(a, params, idx)),
                Box::new(replace_const_one(b, params, idx)),
            ),
            LoweredOp::Sub(a, b) => LoweredOp::Sub(
                Box::new(replace_const_one(a, params, idx)),
                Box::new(replace_const_one(b, params, idx)),
            ),
            LoweredOp::Mul(a, b) => LoweredOp::Mul(
                Box::new(replace_const_one(a, params, idx)),
                Box::new(replace_const_one(b, params, idx)),
            ),
            LoweredOp::Div(a, b) => LoweredOp::Div(
                Box::new(replace_const_one(a, params, idx)),
                Box::new(replace_const_one(b, params, idx)),
            ),
            LoweredOp::Pow(a, b) => LoweredOp::Pow(
                Box::new(replace_const_one(a, params, idx)),
                Box::new(replace_const_one(b, params, idx)),
            ),
        }
    }

    // Suppress unused-function warning for substitute_ones (used for clarity)
    let _ = substitute_ones;

    replace_const_one(&lowered, params, &mut param_idx)
}

/// Candidate named constants for constants extraction, ordered by priority.
fn named_const_candidates() -> Vec<(f64, NamedConst)> {
    vec![
        (std::f64::consts::PI, NamedConst::Pi),
        (-std::f64::consts::PI, NamedConst::NegPi),
        (std::f64::consts::E, NamedConst::E),
        (-std::f64::consts::E, NamedConst::NegE),
        (std::f64::consts::SQRT_2, NamedConst::Sqrt2),
        (-std::f64::consts::SQRT_2, NamedConst::NegSqrt2),
        (0.5, NamedConst::Half),
        (-0.5, NamedConst::NegHalf),
        (1.0 / 3.0, NamedConst::Third),
        (0.25, NamedConst::Quarter),
    ]
}

/// Substitute the `target_idx`-th `Const` node (in post-order traversal) with
/// `replacement`, returning the modified tree.
fn substitute_const(
    op: &LoweredOp,
    target_idx: usize,
    replacement: &LoweredOp,
    current_idx: &mut usize,
) -> LoweredOp {
    match op {
        LoweredOp::Const(_) | LoweredOp::NamedConst(_) => {
            let this_idx = *current_idx;
            *current_idx += 1;
            if this_idx == target_idx {
                replacement.clone()
            } else {
                op.clone()
            }
        }
        LoweredOp::Var(_) => op.clone(),
        LoweredOp::Neg(a) => LoweredOp::Neg(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Exp(a) => LoweredOp::Exp(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Ln(a) => LoweredOp::Ln(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Sin(a) => LoweredOp::Sin(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Cos(a) => LoweredOp::Cos(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Tan(a) => LoweredOp::Tan(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Sinh(a) => LoweredOp::Sinh(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Cosh(a) => LoweredOp::Cosh(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Tanh(a) => LoweredOp::Tanh(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Arcsin(a) => LoweredOp::Arcsin(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Arccos(a) => LoweredOp::Arccos(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Arctan(a) => LoweredOp::Arctan(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Arcsinh(a) => LoweredOp::Arcsinh(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Arccosh(a) => LoweredOp::Arccosh(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Arctanh(a) => LoweredOp::Arctanh(Box::new(substitute_const(
            a,
            target_idx,
            replacement,
            current_idx,
        ))),
        LoweredOp::Add(a, b) => LoweredOp::Add(
            Box::new(substitute_const(a, target_idx, replacement, current_idx)),
            Box::new(substitute_const(b, target_idx, replacement, current_idx)),
        ),
        LoweredOp::Sub(a, b) => LoweredOp::Sub(
            Box::new(substitute_const(a, target_idx, replacement, current_idx)),
            Box::new(substitute_const(b, target_idx, replacement, current_idx)),
        ),
        LoweredOp::Mul(a, b) => LoweredOp::Mul(
            Box::new(substitute_const(a, target_idx, replacement, current_idx)),
            Box::new(substitute_const(b, target_idx, replacement, current_idx)),
        ),
        LoweredOp::Div(a, b) => LoweredOp::Div(
            Box::new(substitute_const(a, target_idx, replacement, current_idx)),
            Box::new(substitute_const(b, target_idx, replacement, current_idx)),
        ),
        LoweredOp::Pow(a, b) => LoweredOp::Pow(
            Box::new(substitute_const(a, target_idx, replacement, current_idx)),
            Box::new(substitute_const(b, target_idx, replacement, current_idx)),
        ),
    }
}

/// Count `Const` and `NamedConst` nodes in post-order.
fn count_const_nodes(op: &LoweredOp) -> usize {
    match op {
        LoweredOp::Const(_) | LoweredOp::NamedConst(_) => 1,
        LoweredOp::Var(_) => 0,
        LoweredOp::Neg(a)
        | LoweredOp::Exp(a)
        | LoweredOp::Ln(a)
        | LoweredOp::Sin(a)
        | LoweredOp::Cos(a)
        | LoweredOp::Tan(a)
        | LoweredOp::Sinh(a)
        | LoweredOp::Cosh(a)
        | LoweredOp::Tanh(a)
        | LoweredOp::Arcsin(a)
        | LoweredOp::Arccos(a)
        | LoweredOp::Arctan(a)
        | LoweredOp::Arcsinh(a)
        | LoweredOp::Arccosh(a)
        | LoweredOp::Arctanh(a) => count_const_nodes(a),
        LoweredOp::Add(a, b)
        | LoweredOp::Sub(a, b)
        | LoweredOp::Mul(a, b)
        | LoweredOp::Div(a, b)
        | LoweredOp::Pow(a, b) => count_const_nodes(a) + count_const_nodes(b),
    }
}

/// Evaluate MSE of a `LoweredOp` tree directly against data.
fn eval_lowered_mse(op: &LoweredOp, inputs: &[Vec<f64>], targets: &[f64]) -> f64 {
    let ops = op.to_oxiblas_ops();
    let mut total = 0.0;
    let mut count = 0usize;
    for (input, &target) in inputs.iter().zip(targets) {
        let val = LoweredOp::eval_ops(&ops, input);
        if val.is_finite() {
            total += (val - target) * (val - target);
            count += 1;
        }
    }
    if count == 0 {
        f64::INFINITY
    } else {
        total / count as f64
    }
}

/// Run greedy named-constants extraction on a `LoweredOp` tree.
///
/// For each `Const` position (in post-order), tries each candidate constant
/// and accepts the substitution if `new_mse ≤ (1 + eps) * current_mse`.
/// Returns the (possibly modified) tree and its MSE.
pub(super) fn extract_named_constants(
    op: LoweredOp,
    initial_mse: f64,
    eps: f64,
    inputs: &[Vec<f64>],
    targets: &[f64],
) -> (LoweredOp, f64) {
    let candidates = named_const_candidates();
    let mut current = op;
    let mut current_mse = initial_mse;

    let n_consts = count_const_nodes(&current);
    for const_idx in 0..n_consts {
        // Find the best candidate for this position
        let mut best_candidate: Option<(LoweredOp, f64)> = None;

        for (cand_val, cand_nc) in &candidates {
            let replacement = LoweredOp::NamedConst(cand_nc.clone());
            let candidate_tree = substitute_const(&current, const_idx, &replacement, &mut 0);
            let new_mse = eval_lowered_mse(&candidate_tree, inputs, targets);
            if new_mse <= (1.0 + eps) * current_mse {
                // Prefer the candidate with lowest MSE
                let accept = match &best_candidate {
                    None => true,
                    Some((_, prev_mse)) => new_mse < *prev_mse,
                };
                if accept {
                    // Only accept if it's actually "closer" than current raw value
                    // (avoid replacing a well-fit constant with a distant named one)
                    fn get_const_val(
                        op: &LoweredOp,
                        target_idx: usize,
                        ctr: &mut usize,
                    ) -> Option<f64> {
                        match op {
                            LoweredOp::Const(c) => {
                                let i = *ctr;
                                *ctr += 1;
                                if i == target_idx { Some(*c) } else { None }
                            }
                            LoweredOp::NamedConst(nc) => {
                                let i = *ctr;
                                *ctr += 1;
                                if i == target_idx {
                                    Some(nc.value())
                                } else {
                                    None
                                }
                            }
                            LoweredOp::Var(_) => None,
                            LoweredOp::Neg(a)
                            | LoweredOp::Exp(a)
                            | LoweredOp::Ln(a)
                            | LoweredOp::Sin(a)
                            | LoweredOp::Cos(a)
                            | LoweredOp::Tan(a)
                            | LoweredOp::Sinh(a)
                            | LoweredOp::Cosh(a)
                            | LoweredOp::Tanh(a)
                            | LoweredOp::Arcsin(a)
                            | LoweredOp::Arccos(a)
                            | LoweredOp::Arctan(a)
                            | LoweredOp::Arcsinh(a)
                            | LoweredOp::Arccosh(a)
                            | LoweredOp::Arctanh(a) => get_const_val(a, target_idx, ctr),
                            LoweredOp::Add(a, b)
                            | LoweredOp::Sub(a, b)
                            | LoweredOp::Mul(a, b)
                            | LoweredOp::Div(a, b)
                            | LoweredOp::Pow(a, b) => get_const_val(a, target_idx, ctr)
                                .or_else(|| get_const_val(b, target_idx, ctr)),
                        }
                    }
                    let orig_val = {
                        let mut ctr = 0usize;
                        get_const_val(&current, const_idx, &mut ctr).unwrap_or(f64::NAN)
                    };
                    // Accept only when the candidate is genuinely close to the
                    // original constant value (within 5%).
                    let close_enough =
                        (cand_val - orig_val).abs() <= 0.05 * orig_val.abs().max(1e-12);
                    if close_enough {
                        best_candidate = Some((candidate_tree, new_mse));
                    }
                }
            }
        }

        if let Some((new_tree, new_mse)) = best_candidate {
            current = new_tree;
            current_mse = new_mse;
        }
    }

    (current, current_mse)
}
