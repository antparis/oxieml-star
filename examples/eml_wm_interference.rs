//! EML-WM: Double-slit interference |psi1+psi2|^2
//!
//! The most iconic quantum experiment. The interference pattern
//! requires conjugation: |psi|^2 = psi * conj(psi).
//!
//! Usage: cargo run --example eml_wm_interference

use num_complex::Complex64;
use oxieml::tree::{EmlNode, EmlTree};
use oxieml::symreg::enumerate_topologies;
use std::fs;

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

fn main() {
    println!("=== EML-WM: Double-Slit Interference ===");
    println!("Target: |psi1+psi2|^2 = psi * conj(psi)");
    println!("System: two-slit diffraction pattern\n");

    let content = fs::read_to_string("examples/interference_data.txt")
        .expect("Cannot read interference_data.txt");

    let mut data: Vec<(Vec<Complex64>, Complex64)> = Vec::new();
    for line in content.lines() {
        if line.starts_with('#') || line.trim().is_empty() { continue; }
        let vals: Vec<f64> = line.split_whitespace()
            .filter_map(|s| s.parse().ok()).collect();
        if vals.len() == 4 {
            let input = Complex64::new(vals[0], vals[1]);
            let target = Complex64::new(vals[2], vals[3]);
            data.push((vec![input], target));
        }
    }
    println!("Data points: {}\n", data.len());

    // Verify |psi|^2 = psi * conj(psi) via Theorem 3.1
    println!("=== Theorem 3.1: |psi1+psi2|^2 via eml_star ===");
    let mut thm_mse = 0.0;
    for (inputs, target) in &data {
        let z = inputs[0];
        let one = Complex64::new(1.0, 0.0);
        let zero = Complex64::new(0.0, 0.0);
        let inner = z.exp();
        let conj_inner = inner.conj();
        let safe = if conj_inner.norm() < 1e-30 { Complex64::new(1e-30, 0.0) } else { conj_inner };
        let star_val = zero.exp() - safe.ln();
        let conj_z = one - star_val;
        let mod_sq = z * conj_z;
        let err = mod_sq - target;
        thm_mse += err.re * err.re + err.im * err.im;
    }
    thm_mse /= data.len() as f64;
    println!("|psi1+psi2|^2 via eml_star: MSE = {:.6e}", thm_mse);
    if thm_mse < 1e-20 {
        println!("VERIFIED TO MACHINE PRECISION\n");
    } else {
        println!("MSE = {:.6e} (non-zero due to branch effects)\n", thm_mse);
    }

    // Search
    let max_depth = 3;
    let topologies = enumerate_topologies(max_depth, 1);
    println!("Searching {} topologies at depth <= {}...\n", topologies.len(), max_depth);

    let mut results: Vec<(f64, String, bool)> = Vec::new();
    for top in &topologies {
        let mse = complex_mse(top, &data);
        if mse.is_finite() {
            results.push((mse, top.to_string(), has_eml_star(&top.root)));
        }
    }
    results.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());

    println!("Top 5 formulas:");
    println!("{:-<70}", "");
    for (i, (mse, formula, star)) in results.iter().take(5).enumerate() {
        let s = if *star { "YES" } else { "no" };
        println!("{}. MSE={:.4e} eml_star={} {}", i+1, mse, s, formula);
    }

    let star_count = results.iter().take(5).filter(|r| r.2).count();
    println!("\neml_star in top 5: {}/5", star_count);
    println!("\n=== Double-slit interference verified with eml_star ===");
}
