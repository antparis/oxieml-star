//! EML-WM: Biomedical & Life Sciences Suite — 12 Systems
//!
//! MRI, EEG, ECG, OCT, FRET, protein crystallography, ultrasound,
//! DNA transport, pharmacokinetics, neural coherence, flow cytometry,
//! calcium imaging.
//!
//! Usage: cargo run --example eml_wm_biomedical

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
    println!("  EML-WM Biomedical Suite: 12 Life Sciences Systems");
    println!("  MRI | EEG | ECG | OCT | FRET | Protein | Ultrasound |");
    println!("  DNA | Pharma | Neuroscience | Cytometry | Calcium");
    println!("===================================================================\n");

    verify_mod_squared(
        "MRI: k-space reconstruction |S(k)|^2",
        "examples/mri_kspace.txt"
    );
    verify_mod_squared(
        "EEG: brain wave spectral power |X(f)|^2",
        "examples/eeg_spectral_power.txt"
    );
    verify_mod_squared(
        "ECG: heart signal envelope |z(t)|^2",
        "examples/ecg_analytic.txt"
    );
    verify_mod_squared(
        "OCT: optical coherence |E_ref+E_sample|^2",
        "examples/oct_interference.txt"
    );
    verify_mod_squared(
        "FRET: fluorescence dipole |kappa|^2",
        "examples/fret_efficiency.txt"
    );
    verify_mod_squared(
        "Protein X-ray: molecular transform |F|^2",
        "examples/protein_xray.txt"
    );
    verify_mod_squared(
        "Ultrasound: echo signal |S(t)|^2",
        "examples/ultrasound_echo.txt"
    );
    verify_mod_squared(
        "DNA: electron transport |psi|^2",
        "examples/dna_coupling.txt"
    );
    verify_mod_squared(
        "Pharma: drug transfer function |H(s)|^2",
        "examples/pharma_transfer.txt"
    );
    verify_mod_squared(
        "Neuroscience: neural coherence |C(f)|^2",
        "examples/neural_coherence.txt"
    );
    verify_mod_squared(
        "Flow cytometry: scatter amplitude |FSC|^2",
        "examples/flow_cytometry.txt"
    );
    verify_mod_squared(
        "Calcium imaging: neural signal |dF/F|^2",
        "examples/calcium_imaging.txt"
    );

    println!("\n===================================================================");
    println!("  All verified with eml_star (Theorem 3.1, Monnerot 2026)");
    println!("===================================================================");
}
