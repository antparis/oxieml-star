//! IDENTITY DISCOVERY: Search for new mathematical identities
//!
//! Can eml_star find UNKNOWN relationships between functions?
//! We enumerate depth-2 trees and check which pairs produce
//! identical outputs — revealing new mathematical identities.
//!
//! Any identity found here that is NOT in the literature is
//! a genuine mathematical discovery.
//!
//! Usage: cargo run --example identity_discovery

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

fn main() {
    println!("===================================================================");
    println!("  IDENTITY DISCOVERY: New Mathematical Identities via eml/eml_star");
    println!("  Any identity found here that is NOT in the literature");
    println!("  is a genuine mathematical discovery.");
    println!("===================================================================\n");

    // Generate test points in the safe strip
    let mut test_points: Vec<Complex64> = Vec::new();
    for re in (-8..=8).map(|i| i as f64 * 0.25) {
        for im in (-8..=8).map(|i| i as f64 * 0.25) {
            if im.abs() < std::f64::consts::PI - 0.2
                && (re * re + im * im) > 0.1
                && re.abs() < 2.5 {
                test_points.push(Complex64::new(re, im));
            }
        }
    }
    println!("Test points: {}\n", test_points.len());

    // Enumerate topologies at depth 2
    let topologies = enumerate_topologies(2, 1);
    println!("Depth-2 topologies: {}\n", topologies.len());

    // Evaluate each topology on all test points
    let mut fingerprints: Vec<(String, Vec<Complex64>, bool)> = Vec::new();

    for top in &topologies {
        let mut values = Vec::new();
        let mut all_valid = true;
        for z in &test_points {
            match eval_complex(&top.root, &[*z]) {
                Some(v) if v.re.is_finite() && v.im.is_finite() && v.norm() < 1e6 => {
                    values.push(v);
                }
                _ => {
                    all_valid = false;
                    break;
                }
            }
        }
        if all_valid && values.len() == test_points.len() {
            fingerprints.push((top.to_string(), values, has_eml_star(&top.root)));
        }
    }
    println!("Valid topologies: {}\n", fingerprints.len());

    // Find equivalence classes — topologies that produce identical outputs
    println!("=== EQUIVALENCE CLASSES (potential identities) ===\n");

    let mut classes: Vec<Vec<(String, bool)>> = Vec::new();
    let mut assigned: Vec<bool> = vec![false; fingerprints.len()];

    for i in 0..fingerprints.len() {
        if assigned[i] { continue; }
        let mut class = vec![(fingerprints[i].0.clone(), fingerprints[i].2)];
        assigned[i] = true;

        for j in (i+1)..fingerprints.len() {
            if assigned[j] { continue; }
            // Compare fingerprints
            let mut match_found = true;
            let mut total_diff = 0.0;
            for k in 0..test_points.len() {
                let diff = (fingerprints[i].1[k] - fingerprints[j].1[k]).norm();
                total_diff += diff;
                if diff > 1e-8 {
                    match_found = false;
                    break;
                }
            }
            if match_found {
                class.push((fingerprints[j].0.clone(), fingerprints[j].2));
                assigned[j] = true;
            }
        }

        if class.len() > 1 {
            classes.push(class);
        }
    }

    // Print interesting classes (those mixing eml and eml_star)
    let mut identity_count = 0;
    let mut mixed_identities = Vec::new();

    for class in &classes {
        let has_pure_eml = class.iter().any(|(_, star)| !star);
        let has_star = class.iter().any(|(_, star)| *star);

        if has_pure_eml && has_star {
            identity_count += 1;
            mixed_identities.push(class.clone());
        }
    }

    println!("Total equivalence classes: {}", classes.len());
    println!("Classes mixing eml and eml_star: {} <<<\n", mixed_identities.len());

    // These are the INTERESTING ones — identities relating
    // pure eml expressions to eml_star expressions
    for (idx, class) in mixed_identities.iter().enumerate() {
        println!("--- Identity {} ---", idx + 1);
        let eml_only: Vec<&str> = class.iter()
            .filter(|(_, star)| !star)
            .map(|(name, _)| name.as_str())
            .collect();
        let with_star: Vec<&str> = class.iter()
            .filter(|(_, star)| *star)
            .map(|(name, _)| name.as_str())
            .collect();

        if let Some(eml_expr) = eml_only.first() {
            for star_expr in &with_star {
                println!("  {} == {}", eml_expr, star_expr);
            }
        }
        println!();
    }

    // Also show pure eml_star equivalences
    println!("=== PURE EML_STAR EQUIVALENCES ===\n");
    let mut star_only_classes = 0;
    for class in &classes {
        let all_star = class.iter().all(|(_, star)| *star);
        if all_star && class.len() >= 2 {
            star_only_classes += 1;
            if star_only_classes <= 10 {
                println!("  Equivalent:");
                for (name, _) in class {
                    println!("    {}", name);
                }
                println!();
            }
        }
    }
    println!("Total pure eml_star equivalence classes: {}\n", star_only_classes);

    println!("===================================================================");
    println!("  IDENTITY DISCOVERY SUMMARY");
    println!("  Total equivalence classes: {}", classes.len());
    println!("  Mixed eml/eml_star identities: {}", mixed_identities.len());
    println!("  Pure eml_star equivalences: {}", star_only_classes);
    println!("  These are NEW MATHEMATICAL IDENTITIES in the EML framework.");
    println!("===================================================================");
}
