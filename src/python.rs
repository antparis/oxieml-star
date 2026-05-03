//! Python bindings for OxiEML via PyO3.
//!
//! Exposes [`PySymRegConfig`], [`PySymRegEngine`], and [`PyDiscoveredFormula`]
//! to Python, matching the Rust API in [`crate::symreg`].
//!
//! # Usage (Python)
//! ```python
//! import numpy as np
//! import oxieml
//!
//! config = oxieml.SymRegConfig.quick()
//! engine = oxieml.SymRegEngine(config)
//!
//! X = np.column_stack([x_data])   # shape (n, n_features)
//! y = y_data                       # shape (n,)
//!
//! formulas = engine.discover(X, y)
//! for f in formulas:
//!     print(f.pretty, f.mse)
//! ```

use numpy::{PyReadonlyArray1, PyReadonlyArray2};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

// ---------------------------------------------------------------------------
// PySymRegConfig
// ---------------------------------------------------------------------------

/// Configuration for the symbolic regression engine.
///
/// Use the class-methods `quick`, `balanced`, or `exhaustive` for
/// sensible presets, then override individual attributes as needed.
#[pyclass(name = "SymRegConfig", from_py_object)]
#[derive(Clone)]
pub struct PySymRegConfig {
    inner: crate::symreg::SymRegConfig,
    /// Maximum number of formulas to return from [`PySymRegEngine::discover`].
    ///
    /// The engine may find more candidates; this limits the returned slice.
    /// `0` means unlimited (return all).
    pub max_formulas: usize,
}

#[pymethods]
impl PySymRegConfig {
    /// Create a quick (shallow/fast) configuration preset.
    #[staticmethod]
    pub fn quick() -> Self {
        Self {
            inner: crate::symreg::SymRegConfig::quick(),
            max_formulas: 0,
        }
    }

    /// Create a balanced (production-default) configuration preset.
    #[staticmethod]
    pub fn balanced() -> Self {
        Self {
            inner: crate::symreg::SymRegConfig::balanced(),
            max_formulas: 0,
        }
    }

    /// Create an exhaustive (slow but thorough) configuration preset.
    #[staticmethod]
    pub fn exhaustive() -> Self {
        Self {
            inner: crate::symreg::SymRegConfig::exhaustive(),
            max_formulas: 0,
        }
    }

    /// Maximum tree depth to explore.
    #[getter]
    pub fn depth_limit(&self) -> usize {
        self.inner.max_depth
    }

    /// Set the maximum tree depth.
    #[setter]
    pub fn set_depth_limit(&mut self, v: usize) {
        self.inner.max_depth = v;
    }

    /// Maximum number of formulas to return (0 = unlimited).
    #[getter]
    pub fn get_max_formulas(&self) -> usize {
        self.max_formulas
    }

    /// Set the maximum number of formulas to return.
    #[setter]
    pub fn set_max_formulas(&mut self, v: usize) {
        self.max_formulas = v;
    }

    /// Adam optimizer iteration budget per topology.
    #[getter]
    pub fn adam_steps(&self) -> usize {
        self.inner.max_iter
    }

    /// Set the Adam optimizer iteration budget.
    #[setter]
    pub fn set_adam_steps(&mut self, v: usize) {
        self.inner.max_iter = v;
    }

    /// Optional RNG seed for reproducible runs.
    #[getter]
    pub fn seed(&self) -> Option<u64> {
        self.inner.seed
    }

    /// Set the RNG seed (`None` for non-deterministic).
    #[setter]
    pub fn set_seed(&mut self, v: Option<u64>) {
        self.inner.seed = v;
    }

    /// Human-readable representation.
    pub fn __repr__(&self) -> String {
        format!(
            "SymRegConfig(depth_limit={}, adam_steps={}, max_formulas={})",
            self.inner.max_depth, self.inner.max_iter, self.max_formulas
        )
    }
}

// ---------------------------------------------------------------------------
// PyDiscoveredFormula
// ---------------------------------------------------------------------------

/// A symbolic formula discovered by the regression engine.
#[pyclass(name = "DiscoveredFormula", from_py_object)]
#[derive(Clone)]
pub struct PyDiscoveredFormula {
    inner: crate::symreg::DiscoveredFormula,
}

#[pymethods]
impl PyDiscoveredFormula {
    /// Human-readable string representation of the formula.
    #[getter]
    pub fn pretty(&self) -> &str {
        &self.inner.pretty
    }

    /// Mean squared error on the training data.
    #[getter]
    pub fn mse(&self) -> f64 {
        self.inner.mse
    }

    /// Tree node count used as a complexity measure.
    #[getter]
    pub fn complexity(&self) -> usize {
        self.inner.complexity
    }

    /// Combined score: `mse + complexity_penalty * complexity`.
    #[getter]
    pub fn score(&self) -> f64 {
        self.inner.score
    }

    /// Cross-validated MSE, or `None` when CV was not enabled.
    #[getter]
    pub fn cv_mse(&self) -> Option<f64> {
        self.inner.cv_mse
    }

    /// Convert the formula to a LaTeX math expression.
    pub fn to_latex(&self) -> String {
        self.inner.to_latex()
    }

    /// Evaluate the formula at the given variable values.
    ///
    /// `xs` must contain at least as many elements as the number of distinct
    /// variables referenced in the formula.
    pub fn eval(&self, xs: Vec<f64>) -> PyResult<f64> {
        let lowered = self.inner.eml_tree.lower().simplify();
        let n_vars = lowered.count_vars();
        if xs.len() < n_vars {
            return Err(PyValueError::new_err(format!(
                "formula references {} variable(s) but xs has only {} element(s)",
                n_vars,
                xs.len()
            )));
        }
        Ok(lowered.eval(&xs))
    }

    /// Human-readable representation.
    pub fn __repr__(&self) -> String {
        format!(
            "DiscoveredFormula(pretty={:?}, mse={:.6}, complexity={})",
            self.inner.pretty, self.inner.mse, self.inner.complexity
        )
    }
}

// ---------------------------------------------------------------------------
// PySymRegEngine
// ---------------------------------------------------------------------------

/// Symbolic regression engine.
///
/// Construct with a `SymRegConfig` and call `discover` with NumPy arrays.
#[pyclass(name = "SymRegEngine")]
pub struct PySymRegEngine {
    config: PySymRegConfig,
}

#[pymethods]
impl PySymRegEngine {
    /// Create a new engine from the given configuration.
    #[new]
    pub fn new(config: &PySymRegConfig) -> Self {
        Self {
            config: config.clone(),
        }
    }

    /// Discover symbolic formulas from data.
    ///
    /// Parameters
    /// ----------
    /// x : numpy.ndarray, shape (n_samples, n_features), dtype float64
    ///     Input feature matrix.
    /// y : numpy.ndarray, shape (n_samples,), dtype float64
    ///     Target values.
    ///
    /// Returns
    /// -------
    /// list of DiscoveredFormula, sorted best-first by score.
    pub fn discover<'py>(
        &self,
        py: Python<'py>,
        x: PyReadonlyArray2<'py, f64>,
        y: PyReadonlyArray1<'py, f64>,
    ) -> PyResult<Vec<PyDiscoveredFormula>> {
        let x_arr = x.as_array();
        let y_arr = y.as_array();

        let n_samples = y_arr.len();
        let n_features = x_arr.ncols();

        if x_arr.nrows() != n_samples {
            return Err(PyValueError::new_err(format!(
                "X has {} rows but y has {} elements",
                x_arr.nrows(),
                n_samples
            )));
        }

        if n_samples == 0 {
            return Err(PyValueError::new_err("input arrays must not be empty"));
        }

        // Convert from row-major matrix to per-row sample vectors.
        // `inputs[i]` = feature vector of the i-th data point.
        let mut inputs: Vec<Vec<f64>> = Vec::with_capacity(n_samples);
        for i in 0..n_samples {
            let mut row = Vec::with_capacity(n_features);
            for j in 0..n_features {
                let val = x_arr.get((i, j)).copied().ok_or_else(|| {
                    PyValueError::new_err(format!("index ({i},{j}) out of bounds"))
                })?;
                row.push(val);
            }
            inputs.push(row);
        }

        let targets: Vec<f64> = y_arr.iter().copied().collect();
        let engine = crate::symreg::SymRegEngine::new(self.config.inner.clone());
        let max_formulas = self.config.max_formulas;

        // Release the GIL during the compute-intensive discovery pass.
        let result = py.detach(|| engine.discover(&inputs, &targets, n_features));

        let mut formulas = result.map_err(|e| PyValueError::new_err(e.to_string()))?;

        // Optionally truncate to requested number of formulas.
        if max_formulas > 0 && formulas.len() > max_formulas {
            formulas.truncate(max_formulas);
        }

        formulas
            .into_iter()
            .map(|f| Ok(PyDiscoveredFormula { inner: f }))
            .collect()
    }

    /// Human-readable representation.
    pub fn __repr__(&self) -> String {
        format!(
            "SymRegEngine(depth_limit={}, adam_steps={})",
            self.config.inner.max_depth, self.config.inner.max_iter
        )
    }
}

// ---------------------------------------------------------------------------
// Module definition
// ---------------------------------------------------------------------------

/// Register the `oxieml._core` Python extension module.
#[pymodule]
pub fn _core(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PySymRegConfig>()?;
    m.add_class::<PyDiscoveredFormula>()?;
    m.add_class::<PySymRegEngine>()?;
    Ok(())
}
