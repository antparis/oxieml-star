//! DISCOVERY TEST: Can oxieml-star rediscover eml_star formulas?
//!
//! We generate data from KNOWN eml_star formulas, then run the
//! topology search to see if the engine rediscovers them.
//! This is the real test of symbolic regression with eml_star.
//!
//! Usage: cargo run --example discovery_test

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

fn run_discovery(name: &str, data: &[(Vec<Complex64>, Complex64)], expected: &str) {
    println!("\n--- DISCOVERY TEST: {} ---", name);
    println!("Expected formula: {}", expected);
    println!("Data points: {}", data.len());

    let max_depth = 2;
    let topologies = enumerate_topologies(max_depth, 1);
    println!("Topologies searched: {}\n", topologies.len());

    let mut results: Vec<(f64, String, bool)> = Vec::new();
    for top in &topologies {
        let mse = complex_mse(top, data);
        if mse.is_finite() {
            results.push((mse, top.to_string(), has_eml_star(&top.root)));
        }
    }
    results.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());

    println!("Top 5:");
    for (i, (mse, formula, star)) in results.iter().take(5).enumerate() {
        let s = if *star { "YES" } else { "no" };
        let exact = if *mse < 1e-20 { " <<<< EXACT REDISCOVERY" } else { "" };
        println!("  {}. MSE={:.4e} eml_star={} {}{}",
            i+1, mse, s, formula, exact);
    }

    let best_mse = results.first().map(|r| r.0).unwrap_or(f64::INFINITY);
    if best_mse < 1e-20 {
        println!("\n  RESULT: FORMULA REDISCOVERED TO MACHINE PRECISION");
    } else {
        println!("\n  RESULT: Best MSE = {:.4e} (not exact at this depth)", best_mse);
    }
}

fn main() {
    println!("===================================================================");
    println!("  DISCOVERY TEST: Can eml_star rediscover unknown formulas?");
    println!("===================================================================");

    // Test 1: target = eml_star(1, z) = e - ln(conj(z))
    // Depth 1 formula — should be found easily
    let mut data1: Vec<(Vec<Complex64>, Complex64)> = Vec::new();
    for re in (-10..=10).map(|i| i as f64 * 0.2) {
        for im in (-10..=10).map(|i| i as f64 * 0.2) {
            if im.abs() < std::f64::consts::PI - 0.1 && (re*re + im*im) > 0.1 {
                let z = Complex64::new(re, im);
                let target = Complex64::new(1.0, 0.0).exp() - z.conj().ln();
                if target.re.is_finite() && target.im.is_finite() {
                    data1.push((vec![z], target));
                }
            }
        }
    }
    run_discovery(
        "e - ln(conj(z))",
        &data1,
        "eml_star(1, x0)"
    );

    // Test 2: target = eml_star(z, 1) = exp(z) - ln(conj(1)) = exp(z)
    // Should find both eml(z,1) and eml_star(z,1) since conj(1) = 1
    let mut data2: Vec<(Vec<Complex64>, Complex64)> = Vec::new();
    for re in (-10..=10).map(|i| i as f64 * 0.2) {
        for im in (-10..=10).map(|i| i as f64 * 0.2) {
            if re.abs() < 3.0 {
                let z = Complex64::new(re, im);
                let target = z.exp();
                if target.re.is_finite() && target.im.is_finite() {
                    data2.push((vec![z], target));
                }
            }
        }
    }
    run_discovery(
        "exp(z)",
        &data2,
        "eml(x0, 1) or eml_star(x0, 1)"
    );

    // Test 3: target = eml_star(z, z) = exp(z) - ln(conj(z))
    // Genuinely anti-holomorphic — ONLY eml_star can produce this
    let mut data3: Vec<(Vec<Complex64>, Complex64)> = Vec::new();
    for re in (-10..=10).map(|i| i as f64 * 0.2) {
        for im in (-10..=10).map(|i| i as f64 * 0.2) {
            if im.abs() < std::f64::consts::PI - 0.1 && re.abs() < 3.0
                && (re*re + im*im) > 0.1 {
                let z = Complex64::new(re, im);
                let target = z.exp() - z.conj().ln();
                if target.re.is_finite() && target.im.is_finite() {
                    data3.push((vec![z], target));
                }
            }
        }
    }
    run_discovery(
        "exp(z) - ln(conj(z))",
        &data3,
        "eml_star(x0, x0)"
    );

    println!("\n===================================================================");
    println!("  Discovery test complete");
    println!("===================================================================");
}
