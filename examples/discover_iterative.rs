//! Iterative deepening complex symbolic regression.
//! Evaluates depth by depth, keeps only the best results.
//! Never explodes in memory.

use num_complex::Complex64;
use oxieml::tree::{EmlNode, EmlTree};
use oxieml::symreg::enumerate_topologies;
use std::env;
use std::fs;
use std::time::Instant;

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
            let r = clamped.exp() - vr_safe.ln();
            if r.re.is_finite() && r.im.is_finite() { Some(r) } else { None }
        }
        EmlNode::EmlStar { left, right } => {
            let vl = eval_complex(left, vars)?;
            let vr = eval_complex(right, vars)?;
            let vc = vr.conj();
            let vr_safe = if vc.norm() < 1e-30 { Complex64::new(1e-30, 0.0) } else { vc };
            let clamped = Complex64::new(vl.re.clamp(-709.0, 709.0), vl.im);
            let r = clamped.exp() - vr_safe.ln();
            if r.re.is_finite() && r.im.is_finite() { Some(r) } else { None }
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
        eprintln!("Usage: discover_iterative <file> [--max-depth N] [--top K]");
        eprintln!("File format: re_z im_z re_target im_target");
        std::process::exit(1);
    }

    let file_path = &args[1];
    let mut max_depth: usize = 8;
    let mut top_k: usize = 20;

    let mut i = 2;
    while i < args.len() - 1 {
        match args[i].as_str() {
            "--max-depth" => { max_depth = args[i+1].parse().unwrap_or(8); i += 2; }
            "--top" => { top_k = args[i+1].parse().unwrap_or(20); i += 2; }
            _ => { i += 1; }
        }
    }

    let text = fs::read_to_string(file_path).expect("Failed to read file");
    let mut data: Vec<(Vec<Complex64>, Complex64)> = Vec::new();
    for line in text.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') { continue; }
        let vals: Vec<f64> = line.split_whitespace()
            .filter_map(|t| t.parse().ok()).collect();
        if vals.len() >= 4 {
            data.push((vec![Complex64::new(vals[0], vals[1])], Complex64::new(vals[2], vals[3])));
        } else if vals.len() >= 3 {
            data.push((vec![Complex64::new(vals[0], vals[1])], Complex64::new(vals[2], 0.0)));
        }
    }

    println!("=== OxiEML-Star: Iterative Deepening Discovery ===");
    println!("File: {} ({} points)", file_path, data.len());
    println!("Max depth: {}\n", max_depth);

    // Global best results across all depths
    let mut global_best: Vec<(f64, String, usize, bool, usize)> = Vec::new();

    for depth in 0..=max_depth {
        let start = Instant::now();

        // Cap total enumeration at 100k to prevent OOM
        let all = enumerate_topologies(depth, 1);
        if all.len() > 200_000 {
            println!("Depth {} would generate {} trees - too many, stopping.", depth, all.len());
            break;
        }
        let new_trees = all;
        let count = new_trees.len();

        // Evaluate in chunks of 10000
        let chunk_size = 10_000;
        let mut depth_results: Vec<(f64, String, usize, bool, usize)> = Vec::new();

        for (chunk_idx, chunk) in new_trees.chunks(chunk_size).enumerate() {
            for top in chunk {
                let mse = complex_mse(top, &data);
                if mse.is_finite() {
                    depth_results.push((
                        mse,
                        top.to_string(),
                        top.size(),
                        has_eml_star(&top.root),
                        depth,
                    ));
                }
            }

            // Keep only top_k per chunk to save memory
            depth_results.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap_or(std::cmp::Ordering::Equal));
            depth_results.truncate(top_k * 10);
        }

        let elapsed = start.elapsed();

        // Merge with global best
        global_best.extend(depth_results);
        global_best.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap_or(std::cmp::Ordering::Equal));
        global_best.truncate(top_k);

        let best_mse = global_best.first().map(|r| r.0).unwrap_or(f64::INFINITY);
        let exact = best_mse < 1e-20;

        println!(
            "Depth {} | {} new trees | best MSE = {:.4e} | {:.1}s{}",
            depth, count, best_mse, elapsed.as_secs_f64(),
            if exact { " <<<< EXACT FOUND" } else { "" }
        );

        // Early stop if exact solution found
        if exact {
            println!("\n*** EXACT SOLUTION FOUND AT DEPTH {} ***\n", depth);
            break;
        }

        // Safety: if this depth already took > 5 minutes, warn
        if elapsed.as_secs() > 300 {
            println!("WARNING: depth {} took > 5 min. Stopping here.", depth);
            break;
        }
    }

    // Print final results
    println!("\n{:<6} {:<14} {:<6} {:<6} {:<8} {}", "Rank", "MSE", "Size", "Depth", "eml*?", "Formula");
    println!("{:-<90}", "");
    for (i, (mse, formula, size, star, depth)) in global_best.iter().take(top_k).enumerate() {
        let tag = if *mse < 1e-20 { " <<<< EXACT" } else { "" };
        println!("{:<6} {:<14.4e} {:<6} {:<6} {:<8} {}{}",
            i+1, mse, size, depth, if *star {"YES"} else {"no"}, formula, tag);
    }

    if let Some((mse, formula, _, star, _)) = global_best.first() {
        println!("\nBest: {} (MSE={:.2e}, eml*={})", formula, mse, star);
    }
}
