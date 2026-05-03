//! Numerical differentiation helpers for ODE discovery.
//!
//! These are private utilities used by [`super::SymRegEngine::discover_ode`]
//! to estimate time-derivatives from trajectory data before running symbolic
//! regression on the `(x, dx/dt)` pairs.

/// Estimate `dx/dt` via central differences.
///
/// Interior points use the central-difference formula
/// `(x[i+1] - x[i-1]) / (2*dt)`.
/// The first endpoint uses forward differences `(x[1] - x[0]) / dt`
/// and the last endpoint uses backward differences `(x[n-1] - x[n-2]) / dt`.
///
/// Returns a `Vec` of length equal to `x.len()`.
pub(super) fn central_differences(x: &[f64], dt: f64) -> Vec<f64> {
    let n = x.len();
    if n < 2 {
        return vec![0.0; n];
    }
    let mut dx = vec![0.0; n];
    // Endpoints: forward / backward
    dx[0] = (x[1] - x[0]) / dt;
    dx[n - 1] = (x[n - 1] - x[n - 2]) / dt;
    // Interior: central
    for i in 1..n - 1 {
        dx[i] = (x[i + 1] - x[i - 1]) / (2.0 * dt);
    }
    dx
}

/// Savitzky-Golay smoothed derivative with window=5, polynomial degree=2.
///
/// Falls back to [`central_differences`] when `n < 5`.
///
/// The SG derivative coefficients for window=5, poly=2 are
/// `[-2, -1, 0, 1, 2]`, normalised by `10 * dt`.
pub(super) fn savitzky_golay_derivative(x: &[f64], dt: f64) -> Vec<f64> {
    let n = x.len();
    if n < 5 {
        return central_differences(x, dt);
    }
    let coeffs = [-2.0_f64, -1.0, 0.0, 1.0, 2.0];
    let norm = 10.0 * dt;
    // Fill all positions with central differences first (handles endpoints)
    let mut dx = central_differences(x, dt);
    // Overwrite interior positions (indices 2..n-2) with SG filter
    for i in 2..n - 2 {
        dx[i] = coeffs
            .iter()
            .enumerate()
            .map(|(k, &c)| c * x[i + k - 2])
            .sum::<f64>()
            / norm;
    }
    dx
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn central_differences_linear() {
        // x(t) = 2t → dx/dt = 2 everywhere
        let dt = 0.1_f64;
        let n = 10;
        let x: Vec<f64> = (0..n).map(|i| 2.0 * i as f64 * dt).collect();
        let dx = central_differences(&x, dt);
        for &d in &dx {
            assert!((d - 2.0).abs() < 1e-10, "expected 2.0, got {d}");
        }
    }

    #[test]
    fn central_differences_short_slice() {
        // Single element → returns [0.0]
        let dx = central_differences(&[42.0], 0.1);
        assert_eq!(dx, vec![0.0]);
    }

    #[test]
    fn savitzky_golay_falls_back_for_small_n() {
        // n=4 < 5 → should behave identically to central_differences
        let dt = 0.1_f64;
        let x = vec![1.0, 2.0, 3.0, 4.0];
        let sg = savitzky_golay_derivative(&x, dt);
        let cd = central_differences(&x, dt);
        for (a, b) in sg.iter().zip(cd.iter()) {
            assert!((a - b).abs() < 1e-12, "mismatch: sg={a}, cd={b}");
        }
    }

    #[test]
    fn savitzky_golay_linear_recovers_exact_slope() {
        // For a linear signal, SG deriv equals exact slope everywhere
        let dt = 0.1_f64;
        let n = 20;
        let x: Vec<f64> = (0..n).map(|i| 3.0 * i as f64 * dt).collect();
        let dx = savitzky_golay_derivative(&x, dt);
        for &d in &dx {
            assert!((d - 3.0).abs() < 1e-9, "expected 3.0, got {d}");
        }
    }
}
