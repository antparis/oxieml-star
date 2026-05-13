//! Complex symbolic regression from file.
//!
//! Usage: cargo run --example complex_cli -- <file> [--max-depth N] [--top K]
//!
//! File format: re_z im_z re_target im_target (one point per line)

use num_complex::Complex64;
use oxieml::tree::{EmlNode, EmlTree};
use oxieml::symreg::enumerate_topologies;
use std::env;
use std::fs;

fn eval_complex(node: &EmlNode, vars: &[Complex64]) -> Option<Complex64> {
    match node {
        EmlNode::One => Some(Complex64::new(1.0, 0.0)),
        EmlNode::Zero => Some(Complex64::new(0.0, 0.0)),
        EmlNode::Var(i) => vars.get(*i).copied(),
        EmlNode::Eml { left, right } => {
            let vl = eval_complex(left, vars)?;
            let vr = eval_complex(right, vars)?;
            let vr_safe = if vr.norm() < 1e-30 { Complex64::new(1e-30, 0.0) } else { vr };
            let clamped = Complex64::new(vl.re.clamp(-709.0, 709.0), vl.im);
            let result = clamped.exp() - vr_safe.ln();
            if result.re.is_finite() && result.im.is_finite() { Some(result) } else { None }
        }
        EmlNode::EmlStar { left, right } => {
            let vl = eval_complex(left, vars)?;
            let vr = eval_complex(right, vars)?;
            let vr_conj = vr.conj();
            let vr_safe = if vr_conj.norm() < 1e-30 { Complex64::new(1e-30, 0.0) } else { vr_conj };
            let clamped = Complex64::new(vl.re.clamp(-709.0, 709.0), vl.im);
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
        EmlNode::One | EmlNode::Zero | EmlNode::Var(_) => false,
        EmlNode::EmlStar { .. } => true,
        EmlNode::Eml { left, right } => has_eml_star(left) || has_eml_star(right),
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: complex_cli <file> [--max-depth N] [--top K]");
        eprintln!("File format: re_z im_z re_target im_target");
        std::process::exit(1);
    }

    let file_path = &args[1];
    let mut max_depth: usize = 3;
    let mut top_k: usize = 10;

    let mut i = 2;
    while i < args.len() - 1 {
        match args[i].as_str() {
            "--max-depth" => { max_depth = args[i+1].parse().unwrap_or(3); i += 2; }
            "--top" => { top_k = args[i+1].parse().unwrap_or(10); i += 2; }
            _ => { i += 1; }
        }
    }

    let text = fs::read_to_string(file_path).expect("Failed to read file");
    let mut data: Vec<(Vec<Complex64>, Complex64)> = Vec::new();

    for line in text.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') { continue; }
        let vals: Vec<f64> = line.split_whitespace()
            .filter_map(|t| t.parse().ok())
            .collect();
        if vals.len() >= 4 {
            let z = Complex64::new(vals[0], vals[1]);
            let target = Complex64::new(vals[2], vals[3]);
            data.push((vec![z], target));
        } else if vals.len() >= 3 {
            let z = Complex64::new(vals[0], vals[1]);
            let target = Complex64::new(vals[2], 0.0);
            data.push((vec![z], target));
        }
    }

    println!("=== OxiEML-Star: Complex Discovery from File ===");
    println!("File: {}", file_path);
    println!("Data points: {}", data.len());
    println!("Max depth: {}", max_depth);

    let topologies = enumerate_topologies(max_depth, 1);
    let topo_count = topologies.len().min(100_000);
    let topologies: Vec<_> = topologies.into_iter().take(100_000).collect();
    println!("Topologies: {}", topo_count);
    println!();

    let mut results: Vec<(f64, String, usize, bool)> = Vec::new();
    for top in &topologies {
        let mse = complex_mse(top, &data);
        if mse.is_finite() {
            results.push((mse, top.to_string(), top.size(), has_eml_star(&top.root)));
        }
    }
    results.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap_or(std::cmp::Ordering::Equal));

    println!("{:<6} {:<14} {:<6} {:<8} {}", "Rank", "MSE", "Size", "eml*?", "Formula");
    println!("{:-<80}", "");
    for (i, (mse, formula, size, star)) in results.iter().take(top_k).enumerate() {
        let tag = if *mse < 1e-20 { " <<<< EXACT" } else { "" };
        println!("{:<6} {:<14.4e} {:<6} {:<8} {}{}",
            i+1, mse, size, if *star {"YES"} else {"no"}, formula, tag);
    }

    if let Some((mse, formula, _, star)) = results.first() {
        println!("\nBest: {} (MSE={:.2e}, eml*={})", formula, mse, star);
        let exact = results.iter().take(top_k).filter(|r| r.0 < 1e-20).count();
        let with_star = results.iter().take(top_k).filter(|r| r.3).count();
        println!("Exact in top {}: {}, with eml*: {}", top_k, exact, with_star);
    }
}
