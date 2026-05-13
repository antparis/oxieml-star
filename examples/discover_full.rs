//! Full symbolic regression with conj_eml as primitive.
//! Primitives: {eml, eml_star, conj_eml, add, mul, 0, 1, z}
//! This mirrors the Python GP but as Rust brute force.

use num_complex::Complex64;
use std::sync::Arc;
use std::env;
use std::fs;
use std::time::Instant;

#[derive(Clone, Debug)]
enum Node {
    Zero,
    One,
    Var(usize),
    Half,
    Eml(Arc<Node>, Arc<Node>),
    EmlStar(Arc<Node>, Arc<Node>),
    ConjEml(Arc<Node>),
    RealEml(Arc<Node>),
    ImagEml(Arc<Node>),
    Add(Arc<Node>, Arc<Node>),
    Mul(Arc<Node>, Arc<Node>),
}

impl Node {
    fn eval(&self, vars: &[Complex64]) -> Option<Complex64> {
        match self {
            Node::Zero => Some(Complex64::new(0.0, 0.0)),
            Node::One => Some(Complex64::new(1.0, 0.0)),
            Node::Half => Some(Complex64::new(0.5, 0.0)),
            Node::Var(i) => vars.get(*i).copied(),
            Node::Eml(l, r) => {
                let vl = l.eval(vars)?;
                let vr = r.eval(vars)?;
                let vr_s = if vr.norm() < 1e-30 { Complex64::new(1e-30, 0.0) } else { vr };
                let c = Complex64::new(vl.re.clamp(-709.0, 709.0), vl.im);
                let r = c.exp() - vr_s.ln();
                if r.re.is_finite() && r.im.is_finite() { Some(r) } else { None }
            }
            Node::EmlStar(l, r) => {
                let vl = l.eval(vars)?;
                let vr = r.eval(vars)?;
                let vc = vr.conj();
                let vr_s = if vc.norm() < 1e-30 { Complex64::new(1e-30, 0.0) } else { vc };
                let c = Complex64::new(vl.re.clamp(-709.0, 709.0), vl.im);
                let r = c.exp() - vr_s.ln();
                if r.re.is_finite() && r.im.is_finite() { Some(r) } else { None }
            }
            Node::ConjEml(child) => {
                let z = child.eval(vars)?;
                // conj(z) = 1 - eml_star(0, eml(z, 1))
                let inner = Complex64::new(z.re.clamp(-709.0, 709.0), z.im).exp();
                let ic = inner.conj();
                let ic_s = if ic.norm() < 1e-30 { Complex64::new(1e-30, 0.0) } else { ic };
                let star = Complex64::new(0.0, 0.0).exp() - ic_s.ln();
                let result = Complex64::new(1.0, 0.0) - star;
                if result.re.is_finite() && result.im.is_finite() { Some(result) } else { None }
            }
            Node::RealEml(child) => {
                let z = child.eval(vars)?;
                let cz = Node::ConjEml(Arc::new(Node::Zero)).eval(vars);
                // Re(z) = (z + conj(z)) / 2
                let conj_z = {
                    let inner = Complex64::new(z.re.clamp(-709.0, 709.0), z.im).exp();
                    let ic = inner.conj();
                    let ic_s = if ic.norm() < 1e-30 { Complex64::new(1e-30, 0.0) } else { ic };
                    let star = Complex64::new(0.0, 0.0).exp() - ic_s.ln();
                    Complex64::new(1.0, 0.0) - star
                };
                let result = (z + conj_z) * Complex64::new(0.5, 0.0);
                if result.re.is_finite() && result.im.is_finite() { Some(result) } else { None }
            }
            Node::ImagEml(child) => {
                let z = child.eval(vars)?;
                let conj_z = {
                    let inner = Complex64::new(z.re.clamp(-709.0, 709.0), z.im).exp();
                    let ic = inner.conj();
                    let ic_s = if ic.norm() < 1e-30 { Complex64::new(1e-30, 0.0) } else { ic };
                    let star = Complex64::new(0.0, 0.0).exp() - ic_s.ln();
                    Complex64::new(1.0, 0.0) - star
                };
                let result = (z - conj_z) * Complex64::new(0.0, -0.5);
                if result.re.is_finite() && result.im.is_finite() { Some(result) } else { None }
            }
            Node::Add(l, r) => {
                let vl = l.eval(vars)?;
                let vr = r.eval(vars)?;
                let s = vl + vr;
                if s.re.is_finite() && s.im.is_finite() { Some(s) } else { None }
            }
            Node::Mul(l, r) => {
                let vl = l.eval(vars)?;
                let vr = r.eval(vars)?;
                let p = vl * vr;
                if p.re.is_finite() && p.im.is_finite() { Some(p) } else { None }
            }
        }
    }

    fn size(&self) -> usize {
        match self {
            Node::Zero | Node::One | Node::Half | Node::Var(_) => 1,
            Node::ConjEml(c) | Node::RealEml(c) | Node::ImagEml(c) => 1 + c.size(),
            Node::Eml(l, r) | Node::EmlStar(l, r) | Node::Add(l, r) | Node::Mul(l, r) => {
                1 + l.size() + r.size()
            }
        }
    }

    fn has_star(&self) -> bool {
        match self {
            Node::Zero | Node::One | Node::Half | Node::Var(_) => false,
            Node::EmlStar(..) | Node::ConjEml(_) | Node::RealEml(_) | Node::ImagEml(_) => true,
            Node::Eml(l, r) | Node::Add(l, r) | Node::Mul(l, r) => l.has_star() || r.has_star(),
        }
    }

    fn fmt_str(&self) -> String {
        match self {
            Node::Zero => "0".into(),
            Node::One => "1".into(),
            Node::Half => "0.5".into(),
            Node::Var(i) => format!("x{}", i),
            Node::Eml(l, r) => format!("eml({}, {})", l.fmt_str(), r.fmt_str()),
            Node::EmlStar(l, r) => format!("eml_star({}, {})", l.fmt_str(), r.fmt_str()),
            Node::ConjEml(c) => format!("conj_eml({})", c.fmt_str()),
            Node::RealEml(c) => format!("real_eml({})", c.fmt_str()),
            Node::ImagEml(c) => format!("imag_eml({})", c.fmt_str()),
            Node::Add(l, r) => format!("add({}, {})", l.fmt_str(), r.fmt_str()),
            Node::Mul(l, r) => format!("mul({}, {})", l.fmt_str(), r.fmt_str()),
        }
    }
}

fn enumerate(max_depth: usize) -> Vec<Arc<Node>> {
    let leaves: Vec<Arc<Node>> = vec![
        Arc::new(Node::Zero),
        Arc::new(Node::One),
        Arc::new(Node::Var(0)),
        Arc::new(Node::Half),
    ];

    let mut by_depth: Vec<Vec<Arc<Node>>> = vec![leaves.clone()];

    for d in 1..=max_depth {
        let mut trees: Vec<Arc<Node>> = Vec::new();
        let prev = &by_depth[d - 1];

        // Collect all trees below this depth
        let mut below: Vec<Arc<Node>> = Vec::new();
        for dd in 0..d {
            below.extend(by_depth[dd].iter().cloned());
        }

        // Unary: conj_eml on previous depth
        for t in prev {
            trees.push(Arc::new(Node::ConjEml(t.clone())));
            trees.push(Arc::new(Node::RealEml(t.clone())));
            trees.push(Arc::new(Node::ImagEml(t.clone())));
        }

        // Binary: at least one child at prev depth
        let all_ops = |l: &Arc<Node>, r: &Arc<Node>, out: &mut Vec<Arc<Node>>| {
            out.push(Arc::new(Node::Eml(l.clone(), r.clone())));
            out.push(Arc::new(Node::EmlStar(l.clone(), r.clone())));
            out.push(Arc::new(Node::Add(l.clone(), r.clone())));
            out.push(Arc::new(Node::Mul(l.clone(), r.clone())));
        };

        // Both at prev
        for l in prev {
            for r in prev {
                all_ops(l, r, &mut trees);
            }
        }
        // Left prev, right below
        for l in prev {
            for r in &below {
                all_ops(l, r, &mut trees);
            }
        }
        // Left below, right prev
        for l in &below {
            for r in prev {
                all_ops(l, r, &mut trees);
            }
        }

        // Cap per depth
        if trees.len() > 100_000 {
            trees.truncate(200_000);
        }

        by_depth.push(trees);
    }

    let mut all = Vec::new();
    for level in &by_depth {
        all.extend(level.iter().cloned());
    }
    all
}

fn complex_mse(tree: &Node, data: &[(Complex64, Complex64)]) -> f64 {
    let mut total = 0.0;
    let mut count = 0usize;
    for (z, target) in data {
        if let Some(pred) = tree.eval(&[*z]) {
            let err = pred - target;
            let sq = err.re * err.re + err.im * err.im;
            if sq.is_finite() { total += sq; count += 1; }
        }
    }
    if count == 0 { f64::INFINITY } else { total / count as f64 }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: discover_full <file> [--max-depth N] [--top K]");
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
    let mut data: Vec<(Complex64, Complex64)> = Vec::new();
    for line in text.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') { continue; }
        let v: Vec<f64> = line.split_whitespace().filter_map(|t| t.parse().ok()).collect();
        if v.len() >= 4 {
            data.push((Complex64::new(v[0], v[1]), Complex64::new(v[2], v[3])));
        }
    }

    println!("=== OxiEML-Star: Full Discovery Engine ===");
    println!("Primitives: eml, eml_star, conj_eml, real_eml, imag_eml, add, mul");
    println!("File: {} ({} points)", file_path, data.len());
    println!("Max depth: {}\n", max_depth);

    let mut global_best: Vec<(f64, String, usize, bool)> = Vec::new();

    for depth in 0..=max_depth {
        let start = Instant::now();
        let trees = enumerate(depth);
        let count = trees.len();

        for tree in &trees {
            let mse = complex_mse(tree, &data);
            if mse.is_finite() {
                global_best.push((mse, tree.fmt_str(), tree.size(), tree.has_star()));
            }
        }

        global_best.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap_or(std::cmp::Ordering::Equal));
        global_best.truncate(top_k);

        let best = global_best.first().map(|r| r.0).unwrap_or(f64::INFINITY);
        let exact = best < 1e-20;
        let elapsed = start.elapsed();

        println!("Depth {} | {} trees | best MSE = {:.4e} | {:.1}s{}",
            depth, count, best, elapsed.as_secs_f64(),
            if exact { " <<<< EXACT" } else { "" });

        if exact {
            println!("\n*** EXACT SOLUTION FOUND ***\n");
            break;
        }
        if elapsed.as_secs() > 300 {
            println!("Stopping: > 5 min at depth {}", depth);
            break;
        }
    }

    println!("\n{:<6} {:<14} {:<6} {:<8} {}", "Rank", "MSE", "Size", "eml*?", "Formula");
    println!("{:-<80}", "");
    for (i, (mse, formula, size, star)) in global_best.iter().take(top_k).enumerate() {
        let tag = if *mse < 1e-20 { " <<<< EXACT" } else { "" };
        println!("{:<6} {:<14.4e} {:<6} {:<8} {}{}",
            i+1, mse, size, if *star {"YES"} else {"no"}, formula, tag);
    }
}
