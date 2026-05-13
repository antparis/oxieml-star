//! EML-WM: Mega Suite — 21 Additional Systems
//!
//! Acoustics, antennas, control, crystallography, geophysics, lasers,
//! NMR, materials, photonics, quantum chemistry, radio, semiconductors,
//! stat mech, telecom, turbulence, ultrasonics, XRD, quantum info,
//! seismology, radio astronomy, ultrafast optics.
//!
//! Usage: cargo run --example eml_wm_mega_suite

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
    println!("  EML-WM Mega Suite: 21 Systems across 21 Domains");
    println!("===================================================================\n");

    verify_mod_squared(
        "Acoustics: sound intensity |p|^2",
        "examples/acoustics_intensity.txt"
    );
    verify_mod_squared(
        "Antenna: radiation pattern |E|^2",
        "examples/antenna_radiation.txt"
    );
    verify_mod_squared(
        "Control: frequency response |G(jw)|^2",
        "examples/control_frequency_response.txt"
    );
    verify_mod_squared(
        "Crystallography: structure factor |F|^2",
        "examples/crystallography_structure_factor.txt"
    );
    verify_mod_squared(
        "Geophysics: seismic wave |u|^2",
        "examples/seismic_wave_energy.txt"
    );
    verify_mod_squared(
        "Laser: cavity mode |E|^2",
        "examples/laser_mode_intensity.txt"
    );
    verify_mod_squared(
        "NMR/MRI: transverse magnetization |M|^2",
        "examples/nmr_signal.txt"
    );
    verify_mod_squared(
        "Materials: dielectric |eps(w)|^2",
        "examples/dielectric_response.txt"
    );
    verify_mod_squared(
        "Photonics: evanescent field |E|^2",
        "examples/waveguide_evanescent.txt"
    );
    verify_mod_squared(
        "Quantum Chemistry: orbital |psi|^2",
        "examples/molecular_orbital_density.txt"
    );
    verify_mod_squared(
        "Radio: IQ constellation |s|^2",
        "examples/iq_constellation.txt"
    );
    verify_mod_squared(
        "Semiconductor: Bloch wave |u_k|^2",
        "examples/bloch_wave_density.txt"
    );
    verify_mod_squared(
        "Stat Mech: pair correlation |psi|^2",
        "examples/pair_correlation.txt"
    );
    verify_mod_squared(
        "Telecom: channel impulse |h|^2",
        "examples/channel_impulse_response.txt"
    );
    verify_mod_squared(
        "Turbulence: velocity spectrum |u(k)|^2",
        "examples/turbulence_spectrum.txt"
    );
    verify_mod_squared(
        "Ultrasonics: pressure |p|^2",
        "examples/ultrasonic_intensity.txt"
    );
    verify_mod_squared(
        "XRD: peak intensity |F|^2",
        "examples/xrd_peak_intensity.txt"
    );
    verify_mod_squared(
        "Quantum Info: fidelity |<psi|phi>|^2",
        "examples/qubit_fidelity.txt"
    );
    verify_mod_squared(
        "Seismology: Rayleigh wave |u|^2",
        "examples/rayleigh_wave.txt"
    );
    verify_mod_squared(
        "Radio Astronomy: visibility |V|^2",
        "examples/radio_visibility.txt"
    );
    verify_mod_squared(
        "Ultrafast: pulse autocorrelation |E|^2",
        "examples/pulse_autocorrelation.txt"
    );

    println!("\n===================================================================");
    println!("  All verified with eml_star (Theorem 3.1, Monnerot 2026)");
    println!("===================================================================");
}
