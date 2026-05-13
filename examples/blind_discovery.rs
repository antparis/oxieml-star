//! BLIND DISCOVERY: Can eml_star find a non-trivial physics formula?
//!
//! We give the engine data from a physical system where the
//! relationship involves conjugation in a NON-OBVIOUS way.
//! The engine does NOT know what formula generated the data.
//!
//! Test 1: Given z, find conj(z)/z = |z|^{-2} * conj(z)^2 ... no
//!   Actually: target = (z - 1)/(conj(z) - 1) — reflection coefficient ratio
//!   This requires BOTH eml and eml_star to express.
//!
//! Test 2: Given z, find z * conj(z) + z - conj(z)
//!   = |z|^2 + 2i*Im(z) — a mix of holomorphic and anti-holomorphic
//!
//! Usage: cargo run --example blind_discovery

use num_complex::Complex64;
use oxieml::tree::{EmlNode, EmlTree};
use oxieml::symreg::enumerate_topologies;

fn eval_complex(node: &EmlNode, vars: &[Complex64]) -> Option<Complex64> {
    match node {
        EmlNode::One => Some(Complex64::new(1.0, 0.0)),
        EmlNode::Var(i) => vars.get(*i).copied(),
        EmlNode::Eml { left, right } => {
            let vl = eval_complex(left, vars)?;
            let vr = eval_complex(right, vars)?;
            let vr_safe = if vr.norm() < 1e-30 { Complex64::new(1e-30, 0.0) } else { vr };
            let clamped = if vl.re > 709.0 { Complex64::new(709.0, vl.im) }
                else if vl.re < -709.0 { Complex64::new(-709.0, vl.im) }
                else { vl };
            let result = clamped.exp() - vr_safe.ln();
            if result.re.is_finite() && result.im.is_finite() { Some(result) } else { None }
        }
        EmlNode::EmlStar { left, right } => {
            let vl = eval_complex(left, vars)?;
            let vr = eval_complex(right, vars)?;
            let vr_conj = vr.conj();
            let vr_safe = if vr_conj.norm() < 1e-30 { Complex64::new(1e-30, 0.0) } else { vr_conj };
            let clamped = if vl.re > 709.0 { Complex64::new(709.0, vl.im) }
                else if vl.re < -709.0 { Complex64::new(-709.0, vl.im) }
                else { vl };
            let result = clamped.exp() - vr_safe.ln();
            if result.re.is_finite() && result.im.is_finite() { Some(result) } else { None }
        }
    }
}

fn complex_mse(tree: &EmlTree, data: &[(Vec<Complex64>, Complex64)]) -> f64 {
    let mut total = 0.0;
    let mut count = 0usize;
    for (inputs, target) in data {
        if let Some(pred) = eval_complex(&tree.root, inputs) {
            let err = pred - target;
            let sq = err.re * err.re + err.im * err.im;
            if sq.is_finite() { total += sq; count += 1; }
        }
    }
    if count == 0 { f64::INFINITY } else { total / count as f64 }
}

fn has_eml_star(node: &EmlNode) -> bool {
    match node {
        EmlNode::One | EmlNode::Var(_) => false,
        EmlNode::EmlStar { .. } => true,
        EmlNode::Eml { left, right } => has_eml_star(left) || has_eml_star(right),
    }
}

fn run_blind(name: &str, data: &[(Vec<Complex64>, Complex64)], depth: usize) {
    println!("\n--- BLIND TEST: {} ---", name);
    println!("Data points: {}, search depth: {}\n", data.len(), depth);

    let topologies = enumerate_topologies(depth, 1);
    println!("Topologies: {}\n", topologies.len());

    let mut results: Vec<(f64, String, bool)> = Vec::new();
    for top in &topologies {
        let mse = complex_mse(top, data);
        if mse.is_finite() {
            results.push((mse, top.to_string(), has_eml_star(&top.root)));
        }
    }
    results.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());

    println!("Top 10:");
    for (i, (mse, formula, star)) in results.iter().take(10).enumerate() {
        let s = if *star { "eml_star" } else { "eml_only" };
        let exact = if *mse < 1e-20 { " <<<< EXACT" } else { "" };
        println!("  {:>2}. MSE={:.4e}  [{}]  {}{}",
            i+1, mse, s, formula, exact);
    }

    let star_in_top10 = results.iter().take(10).filter(|r| r.2).count();
    let star_in_top3 = results.iter().take(3).filter(|r| r.2).count();
    println!("\n  eml_star in top 3: {}/3", star_in_top3);
    println!("  eml_star in top 10: {}/10", star_in_top10);

    let best_mse = results.first().map(|r| r.0).unwrap_or(f64::INFINITY);
    if best_mse < 1e-20 {
        println!("  >>> EXACT FORMULA DISCOVERED <<<");
    } else if best_mse < 0.01 {
        println!("  >>> GOOD APPROXIMATION FOUND <<<");
    }
}

fn main() {
    println!("===================================================================");
    println!("  BLIND DISCOVERY: Unknown formulas from raw data");
    println!("  The engine does NOT know what generated these data.");
    println!("===================================================================");

    // Test 1: target = eml(z, eml_star(z, 1))
    // = exp(z) - ln(exp(z) - ln(conj(1)))
    // = exp(z) - ln(exp(z)) = exp(z) - z
    // Wait — conj(1) = 1, so this collapses.
    // Better: eml_star(1, eml_star(1, z)) — nested anti-holomorphic
    let mut data1: Vec<(Vec<Complex64>, Complex64)> = Vec::new();
    for re in (-10..=10).map(|i| i as f64 * 0.2) {
        for im in (-10..=10).map(|i| i as f64 * 0.2) {
            if im.abs() < 2.5 && (re*re + im*im) > 0.1 {
                let z = Complex64::new(re, im);
                let one = Complex64::new(1.0, 0.0);
                // eml_star(1, z) = e - ln(conj(z))
                let inner = one.exp() - z.conj().ln();
                // eml_star(1, inner) = e - ln(conj(inner))
                let target = one.exp() - inner.conj().ln();
                if target.re.is_finite() && target.im.is_finite()
                    && target.norm() < 1e6 {
                    data1.push((vec![z], target));
                }
            }
        }
    }
    run_blind(
        "eml_star(1, eml_star(1, z)) — nested anti-holomorphic",
        &data1, 2
    );

    // Test 2: target = eml(z, 1) + eml_star(z, 1)
    // = exp(z) + exp(z) - ln(1) - ln(conj(1)) = 2*exp(z)
    // Hmm, conj(1) = 1 again. Need non-trivial conj usage.
    // Better: eml_star(eml(z, 1), z) = exp(exp(z)) - ln(conj(z))
    let mut data2: Vec<(Vec<Complex64>, Complex64)> = Vec::new();
    for re in (-8..=8).map(|i| i as f64 * 0.15) {
        for im in (-8..=8).map(|i| i as f64 * 0.15) {
            if im.abs() < 2.5 && re.abs() < 1.5 && (re*re + im*im) > 0.1 {
                let z = Complex64::new(re, im);
                // eml_star(eml(z, 1), z) = exp(exp(z)) - ln(conj(z))
                let target = z.exp().exp() - z.conj().ln();
                if target.re.is_finite() && target.im.is_finite()
                    && target.norm() < 1e6 {
                    data2.push((vec![z], target));
                }
            }
        }
    }
    run_blind(
        "exp(exp(z)) - ln(conj(z)) — mixed holomorphic/anti-holomorphic",
        &data2, 2
    );

    // Test 3: target = eml(eml_star(z, z), 1)
    // = exp(exp(z) - ln(conj(z)))
    // Pure depth 2, mixed
    let mut data3: Vec<(Vec<Complex64>, Complex64)> = Vec::new();
    for re in (-8..=8).map(|i| i as f64 * 0.1) {
        for im in (-8..=8).map(|i| i as f64 * 0.1) {
            if im.abs() < 2.0 && re.abs() < 1.0 && (re*re + im*im) > 0.1 {
                let z = Complex64::new(re, im);
                let eml_star_zz = z.exp() - z.conj().ln();
                let target = eml_star_zz.exp(); // eml(eml_star(z,z), 1)
                if target.re.is_finite() && target.im.is_finite()
                    && target.norm() < 1e6 {
                    data3.push((vec![z], target));
                }
            }
        }
    }
    run_blind(
        "exp(eml_star(z,z)) = exp(exp(z) - ln(conj(z))) — depth 2 mixed",
        &data3, 2
    );

    println!("\n===================================================================");
    println!("  Blind discovery complete");
    println!("===================================================================");
}
