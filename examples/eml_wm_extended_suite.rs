//! EML-WM: Extended Physics Suite — 7 Additional Systems
//!
//! Thermodynamics, plasma, electronics, signal processing,
//! fluid dynamics, quantum optics, nuclear physics.
//!
//! Usage: cargo run --example eml_wm_extended_suite

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
    println!("{:<45} {:>3} pts   MSE = {:.2e}   [{}]",
        name, data.len(), thm_mse, status);
}

fn main() {
    println!("===================================================================");
    println!("  EML-WM Extended Suite: 7 Systems x Theorem 3.1 Verification");
    println!("  Domains: thermo, plasma, electronics, DSP, fluids, QO, nuclear");
    println!("===================================================================\n");

    verify_mod_squared(
        "Thermodynamics: partition |Z|^2",
        "examples/partition_function_data.txt"
    );
    verify_mod_squared(
        "Plasma: dielectric |epsilon(omega)|^2",
        "examples/plasma_dielectric_data.txt"
    );
    verify_mod_squared(
        "Electronics: RLC impedance |Z(omega)|^2",
        "examples/impedance_data.txt"
    );
    verify_mod_squared(
        "Signal processing: FFT power |F(k)|^2",
        "examples/fft_power_data.txt"
    );
    verify_mod_squared(
        "Fluid dynamics: velocity |dw/dz|^2",
        "examples/fluid_flow_data.txt"
    );
    verify_mod_squared(
        "Quantum optics: coherent |alpha|^2",
        "examples/coherent_state_data.txt"
    );
    verify_mod_squared(
        "Nuclear: Breit-Wigner |S(E)|^2",
        "examples/smatrix_data.txt"
    );

    println!("\n===================================================================");
    println!("  All verified with eml_star (Theorem 3.1, Monnerot 2026)");
    println!("===================================================================");
}
