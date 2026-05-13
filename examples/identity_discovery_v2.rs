//! IDENTITY DISCOVERY v2: Two-variable identities + depth 3 (smart)
//!
//! Option 1: Identities with x0 AND x1
//! Option 3: Depth 3 via fingerprint hashing (fast)
//!
//! Usage: cargo run --example identity_discovery_v2

use num_complex::Complex64;
use oxieml::tree::{EmlNode, EmlTree};
use oxieml::symreg::enumerate_topologies;
use std::collections::HashMap;

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

fn has_eml_star(node: &EmlNode) -> bool {
    match node {
        EmlNode::One | EmlNode::Var(_) => false,
        EmlNode::EmlStar { .. } => true,
        EmlNode::Eml { left, right } => has_eml_star(left) || has_eml_star(right),
    }
}

/// Compute a fingerprint hash from evaluation on test points
fn fingerprint(tree: &EmlTree, points: &[Vec<Complex64>]) -> Option<Vec<u64>> {
    let mut fp = Vec::new();
    for vars in points {
        match eval_complex(&tree.root, vars) {
            Some(v) if v.re.is_finite() && v.im.is_finite() && v.norm() < 1e6 => {
                // Quantize to catch near-equal values
                let re_q = (v.re * 1e8).round() as i64;
                let im_q = (v.im * 1e8).round() as i64;
                fp.push((re_q as u64).wrapping_mul(0x9E3779B97F4A7C15)
                    .wrapping_add(im_q as u64));
            }
            _ => return None,
        }
    }
    Some(fp)
}

fn run_identity_search(name: &str, num_vars: usize, max_depth: usize) {
    println!("\n===================================================================");
    println!("  {}", name);
    println!("===================================================================\n");

    // Generate test points
    let mut points: Vec<Vec<Complex64>> = Vec::new();
    if num_vars == 1 {
        for re in (-6..=6).map(|i| i as f64 * 0.3) {
            for im in (-6..=6).map(|i| i as f64 * 0.3) {
                if im.abs() < 2.5 && (re * re + im * im) > 0.1 && re.abs() < 2.0 {
                    points.push(vec![Complex64::new(re, im)]);
                }
            }
        }
    } else {
        // 2 variables — smaller grid to keep it fast
        for r1 in (-3..=3).map(|i| i as f64 * 0.5) {
            for i1 in (-3..=3).map(|i| i as f64 * 0.5) {
                for r2 in (-2..=2).map(|i| i as f64 * 0.7) {
                    for i2 in (-2..=2).map(|i| i as f64 * 0.7) {
                        if i1.abs() < 2.5 && i2.abs() < 2.5
                            && (r1*r1 + i1*i1) > 0.1
                            && (r2*r2 + i2*i2) > 0.1
                            && r1.abs() < 2.0 && r2.abs() < 2.0 {
                            points.push(vec![
                                Complex64::new(r1, i1),
                                Complex64::new(r2, i2),
                            ]);
                        }
                    }
                }
            }
        }
        // Limit points for speed
        if points.len() > 200 {
            points.truncate(200);
        }
    }
    println!("Test points: {}", points.len());

    let topologies = enumerate_topologies(max_depth, num_vars);
    println!("Topologies: {}\n", topologies.len());

    // Hash-based grouping — O(n) instead of O(n^2)
    let mut groups: HashMap<Vec<u64>, Vec<(String, bool)>> = HashMap::new();
    let mut valid_count = 0;

    for top in &topologies {
        if let Some(fp) = fingerprint(top, &points) {
            valid_count += 1;
            let entry = groups.entry(fp).or_insert_with(Vec::new);
            entry.push((top.to_string(), has_eml_star(&top.root)));
        }
    }
    println!("Valid topologies: {}", valid_count);

    // Find classes with size > 1
    let classes: Vec<&Vec<(String, bool)>> = groups.values()
        .filter(|v| v.len() > 1)
        .collect();

    let mixed: Vec<&&Vec<(String, bool)>> = classes.iter()
        .filter(|c| c.iter().any(|(_, s)| !s) && c.iter().any(|(_, s)| *s))
        .collect();

    let pure_star: Vec<&&Vec<(String, bool)>> = classes.iter()
        .filter(|c| c.iter().all(|(_, s)| *s) && c.len() >= 2)
        .collect();

    // Print non-trivial mixed identities (skip those where only const differs)
    println!("\nEquivalence classes: {}", classes.len());
    println!("Mixed eml/eml_star: {}", mixed.len());
    println!("Pure eml_star: {}\n", pure_star.len());

    // Show the most interesting mixed identities
    let mut shown = 0;
    for class in &mixed {
        // Filter: at least one member must use x0 in a non-trivial way
        let has_var = class.iter().any(|(name, _)| name.contains("x0"));
        if !has_var { continue; }

        // Skip if both sides are trivially equivalent (conj(1)=1)
        let eml_only: Vec<&str> = class.iter()
            .filter(|(_, s)| !s).map(|(n, _)| n.as_str()).collect();
        let with_star: Vec<&str> = class.iter()
            .filter(|(_, s)| *s).map(|(n, _)| n.as_str()).collect();

        if eml_only.is_empty() || with_star.is_empty() { continue; }

        shown += 1;
        if shown <= 15 {
            println!("Identity {}:", shown);
            for e in &eml_only {
                for s in &with_star {
                    println!("  {} == {}", e, s);
                }
            }
            println!();
        }
    }
    if shown > 15 {
        println!("  ... and {} more", shown - 15);
    }

    println!("Total non-trivial mixed identities with variables: {}", shown);
}

fn main() {
    println!("===================================================================");
    println!("  IDENTITY DISCOVERY v2: Extended Search");
    println!("===================================================================");

    // Option 1: 2 variables, depth 2
    run_identity_search(
        "TWO-VARIABLE IDENTITIES (depth 2, x0 + x1)",
        2, 2
    );

    // Option 3: 1 variable, depth 3 (using hash fingerprints for speed)
    run_identity_search(
        "DEPTH-3 IDENTITIES (1 variable, hash-accelerated)",
        1, 3
    );

    println!("\n===================================================================");
    println!("  Identity discovery v2 complete");
    println!("===================================================================");
}
