//! Complex-domain symbolic regression using eml★.
//!
//! This example discovers formulas involving complex conjugation
//! by enumerating EML/EmlStar topologies and evaluating on complex data.
//!
//! Usage: cargo run --example complex_symreg

use num_complex::Complex64;
use std::sync::Arc;

// We use oxieml's public API
use oxieml::tree::{EmlNode, EmlTree};
use oxieml::symreg::enumerate_topologies;

/// Evaluate an EML tree on complex inputs using a stack machine.
fn eval_complex(node: &EmlNode, vars: &[Complex64]) -> Option<Complex64> {
    match node {
        EmlNode::One => Some(Complex64::new(1.0, 0.0)),
        EmlNode::Var(i) => vars.get(*i).copied(),
        EmlNode::Eml { left, right } => {
            let vl = eval_complex(left, vars)?;
            let vr = eval_complex(right, vars)?;
            let vr_safe = if vr.norm() < 1e-30 {
                Complex64::new(1e-30, 0.0)
            } else {
                vr
            };
            let clamped = if vl.re > 709.0 {
                Complex64::new(709.0, vl.im)
            } else if vl.re < -709.0 {
                Complex64::new(-709.0, vl.im)
            } else {
                vl
            };
            let result = clamped.exp() - vr_safe.ln();
            if result.re.is_finite() && result.im.is_finite() {
                Some(result)
            } else {
                None
            }
        }
        EmlNode::EmlStar { left, right } => {
            let vl = eval_complex(left, vars)?;
            let vr = eval_complex(right, vars)?;
            let vr_conj = vr.conj();
            let vr_safe = if vr_conj.norm() < 1e-30 {
                Complex64::new(1e-30, 0.0)
            } else {
                vr_conj
            };
            let clamped = if vl.re > 709.0 {
                Complex64::new(709.0, vl.im)
            } else if vl.re < -709.0 {
                Complex64::new(-709.0, vl.im)
            } else {
                vl
            };
            let result = clamped.exp() - vr_safe.ln();
            if result.re.is_finite() && result.im.is_finite() {
                Some(result)
            } else {
                None
            }
        }
    }
}

/// Compute complex MSE: mean(|pred - target|²)
fn complex_mse(tree: &EmlTree, data: &[(Vec<Complex64>, Complex64)]) -> f64 {
    let mut total = 0.0;
    let mut count = 0usize;
    for (inputs, target) in data {
        if let Some(pred) = eval_complex(&tree.root, inputs) {
            let err = pred - target;
            let sq = err.re * err.re + err.im * err.im;
            if sq.is_finite() {
                total += sq;
                count += 1;
            }
        }
    }
    if count == 0 {
        f64::INFINITY
    } else {
        total / count as f64
    }
}

/// Check if a tree contains any EmlStar nodes.
fn has_eml_star(node: &EmlNode) -> bool {
    match node {
        EmlNode::One | EmlNode::Var(_) => false,
        EmlNode::EmlStar { .. } => true,
        EmlNode::Eml { left, right } => has_eml_star(left) || has_eml_star(right),
    }
}

fn main() {
    println!("=== OxiEML-Star: Complex Symbolic Regression ===\n");

    // ── Generate test data: target = conj(z) ──
    let mut data: Vec<(Vec<Complex64>, Complex64)> = Vec::new();
    for re in (-10..=10).map(|i| i as f64 * 0.3) {
        for im in (-10..=10).map(|i| i as f64 * 0.3) {
            if im.abs() < std::f64::consts::PI - 0.1 {
                let z = Complex64::new(re, im);
                let target = z.conj();
                data.push((vec![z], target));
            }
        }
    }
    println!("Data points: {} (target = conj(z))\n", data.len());

    // ── Enumerate topologies ──
    let max_depth = 3;
    let num_vars = 1;
    let topologies = enumerate_topologies(max_depth, num_vars);
    println!("Topologies at depth <= {}: {}\n", max_depth, topologies.len());

    // ── Verify Theorem 3.1 manually: conj(z) = 1 - eml★(0, eml(z, 1)) ──
    println!("=== Theorem 3.1 Verification ===");
    let mut thm_mse = 0.0;
    let mut thm_count = 0usize;
    for (inputs, target) in &data {
        let z = inputs[0];
        let one = Complex64::new(1.0, 0.0);
        let zero = Complex64::new(0.0, 0.0);
        // eml(z, 1) = exp(z) - ln(1) = exp(z)
        let inner = z.exp();
        // eml★(0, exp(z)) = exp(0) - ln(conj(exp(z))) = 1 - conj(z)
        let conj_inner = inner.conj();
        let safe = if conj_inner.norm() < 1e-30 { Complex64::new(1e-30, 0.0) } else { conj_inner };
        let star_val = zero.exp() - safe.ln();
        // conj(z) = 1 - star_val
        let pred = one - star_val;
        let err = pred - target;
        thm_mse += err.re * err.re + err.im * err.im;
        thm_count += 1;
    }
    thm_mse /= thm_count as f64;
    println!("Theorem 3.1: conj(z) = 1 - eml_star(0, eml(z, 1))");
    println!("MSE on {} points: {:.6e}", thm_count, thm_mse);
    if thm_mse < 1e-20 {
        println!("★ VERIFIED TO MACHINE PRECISION\n");
    } else {
        println!("WARNING: MSE too high\n");
    }

    // ── Evaluate each topology ──
    let mut results: Vec<(f64, String, usize, bool)> = Vec::new();

    for top in &topologies {
        let mse = complex_mse(top, &data);
        if mse.is_finite() {
            let uses_star = has_eml_star(&top.root);
            results.push((mse, top.to_string(), top.size(), uses_star));
        }
    }

    // Sort by MSE
    results.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap_or(std::cmp::Ordering::Equal));

    // ── Print top 10 ──
    println!("Top 10 formulas (sorted by MSE):");
    println!("{:-<80}", "");
    println!(
        "{:<6} {:<12} {:<6} {:<8} {}",
        "Rank", "MSE", "Size", "eml★?", "Formula"
    );
    println!("{:-<80}", "");

    for (i, (mse, formula, size, uses_star)) in results.iter().take(10).enumerate() {
        let star_str = if *uses_star { "YES" } else { "no" };
        println!(
            "{:<6} {:<12.4e} {:<6} {:<8} {}",
            i + 1,
            mse,
            size,
            star_str,
            formula
        );
    }

    println!("\n{:-<80}", "");

    // ── Summary ──
    if let Some((best_mse, best_formula, _, best_star)) = results.first() {
        println!("\nBest formula: {}", best_formula);
        println!("MSE: {:.6e}", best_mse);
        println!("Uses eml★: {}", if *best_star { "YES" } else { "no" });

        if *best_mse < 1e-20 {
            println!("\n★ EXACT SOLUTION FOUND — eml★ successfully reconstructs conj(z)!");
        }
    }

    // ── Count how many top-10 use eml★ ──
    let star_count = results.iter().take(10).filter(|r| r.3).count();
    println!(
        "\neml★ usage in top 10: {}/{}",
        star_count,
        results.iter().take(10).count()
    );
}
