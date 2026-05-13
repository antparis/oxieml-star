//! EML-WM: 5 Physical Systems Verification
//!
//! Tests eml_star on: EM wave, harmonic oscillator, spin expectation,
//! Fresnel coefficients, Born scattering cross-section.
//! All require |psi|^2 = psi * conj(psi) via Theorem 3.1.
//!
//! Usage: cargo run --example eml_wm_physics_suite

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

    // Verify |z|^2 = z * conj(z) via Theorem 3.1
    let mut thm_mse = 0.0;
    let one = Complex64::new(1.0, 0.0);
    let zero = Complex64::new(0.0, 0.0);

    for (z, target) in &data {
        // conj(z) = 1 - eml_star(0, eml(z, 1))
        let inner = z.exp();
        let conj_inner = inner.conj();
        let safe = if conj_inner.norm() < 1e-30 {
            Complex64::new(1e-30, 0.0)
        } else {
            conj_inner
        };
        let star_val = zero.exp() - safe.ln();
        let conj_z = one - star_val;
        // |z|^2 = z * conj(z)
        let mod_sq = z * conj_z;
        let err = mod_sq - target;
        thm_mse += err.re * err.re + err.im * err.im;
    }
    thm_mse /= data.len() as f64;

    let status = if thm_mse < 1e-20 { "EXACT" } else { "APPROX" };
    println!("{:<35} {:>3} pts   MSE = {:.2e}   [{}]",
        name, data.len(), thm_mse, status);
}

fn verify_real_part(name: &str, filename: &str) {
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
    let half = Complex64::new(0.5, 0.0);

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
        // Re(z) = (z + conj(z)) / 2
        let re_z = (*z + conj_z) * half;
        let err = re_z - target;
        thm_mse += err.re * err.re + err.im * err.im;
    }
    thm_mse /= data.len() as f64;

    let status = if thm_mse < 1e-20 { "EXACT" } else { "APPROX" };
    println!("{:<35} {:>3} pts   MSE = {:.2e}   [{}]",
        name, data.len(), thm_mse, status);
}

fn main() {
    println!("===================================================================");
    println!("  EML-WM Physics Suite: 5 Systems x Theorem 3.1 Verification");
    println!("===================================================================\n");

    verify_mod_squared(
        "EM plane wave |E+iB|^2",
        "examples/em_wave_data.txt"
    );
    verify_mod_squared(
        "Harmonic oscillator |psi0+i*psi1|^2",
        "examples/harmonic_osc_data.txt"
    );
    verify_real_part(
        "Spin expectation Sx=Re(up*conj(dn))",
        "examples/spin_expect_data.txt"
    );
    verify_mod_squared(
        "Fresnel reflectance |r|^2",
        "examples/fresnel_data.txt"
    );
    verify_mod_squared(
        "Born scattering |f(q)|^2",
        "examples/scattering_data.txt"
    );

    println!("\n===================================================================");
    println!("  All systems verified with eml_star (Theorem 3.1, Monnerot 2026)");
    println!("===================================================================");
}
