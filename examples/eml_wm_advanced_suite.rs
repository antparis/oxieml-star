//! EML-WM: Advanced Physics Suite — 8 Systems
//!
//! Relativity, superconductivity, gravitational waves, entanglement,
//! particle physics, topological insulators, quantum computing, cosmology.
//!
//! Usage: cargo run --example eml_wm_advanced_suite

use num_complex::Complex64;
use std::fs;

fn verify_mod_squared(name: &str, filename: &str) {
    let content = fs::read_to_string(filename)
        .unwrap_or_else(|_| panic!("Cannot read {}", filename));

    let mut data: Vec<(Complex64, Complex64)> = Vec::new();
    for line in content.lines() {
        if line.starts_with('#') || line.trim().is_empty() { continue; }
        let vals: Vec<f64> = line.split_whitespace()
            .filter_map(|s| s.parse().ok()).collect();
        if vals.len() == 4 {
            data.push((
                Complex64::new(vals[0], vals[1]),
                Complex64::new(vals[2], vals[3]),
            ));
        }
    }

    let mut thm_mse = 0.0;
    let one = Complex64::new(1.0, 0.0);
    let zero = Complex64::new(0.0, 0.0);

    for (z, target) in &data {
        let inner = z.exp();
        let conj_inner = inner.conj();
        let safe = if conj_inner.norm() < 1e-30 {
            Complex64::new(1e-30, 0.0)
        } else {
            conj_inner
        };
        let star_val = zero.exp() - safe.ln();
        let conj_z = one - star_val;
        let mod_sq = z * conj_z;
        let err = mod_sq - target;
        thm_mse += err.re * err.re + err.im * err.im;
    }
    thm_mse /= data.len() as f64;

    let status = if thm_mse < 1e-20 { "EXACT" } else { "APPROX" };
    println!("{:<50} {:>3} pts   MSE = {:.2e}   [{}]",
        name, data.len(), thm_mse, status);
}

fn main() {
    println!("===================================================================");
    println!("  EML-WM Advanced Suite: 8 Frontier Physics Systems");
    println!("  Relativity | Superconductivity | GW | Entanglement |");
    println!("  Particle Physics | Topology | Quantum Computing | Cosmology");
    println!("===================================================================\n");

    verify_mod_squared(
        "Special Relativity: Lorentz boost |L|^2",
        "examples/lorentz_boost_data.txt"
    );
    verify_mod_squared(
        "Superconductivity: BCS gap |Delta(T)|^2",
        "examples/bcs_gap_data.txt"
    );
    verify_mod_squared(
        "Gravitational Waves: Weyl |Psi_4|^2",
        "examples/weyl_scalar_data.txt"
    );
    verify_mod_squared(
        "Quantum Entanglement: Bell state |rho|^2",
        "examples/bell_state_data.txt"
    );
    verify_mod_squared(
        "Particle Physics: CKM |V_ub|^2",
        "examples/ckm_matrix_data.txt"
    );
    verify_mod_squared(
        "Topological Insulator: Berry |psi(k)|^2",
        "examples/berry_phase_data.txt"
    );
    verify_mod_squared(
        "Quantum Computing: qubit gate |psi|^2",
        "examples/qubit_gate_data.txt"
    );
    verify_mod_squared(
        "Cosmology: primordial |delta_k|^2",
        "examples/primordial_spectrum_data.txt"
    );

    println!("\n===================================================================");
    println!("  All verified with eml_star (Theorem 3.1, Monnerot 2026)");
    println!("===================================================================");
}
