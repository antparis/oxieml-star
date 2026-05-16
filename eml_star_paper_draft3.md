# Symbolic regression with anti-holomorphic operators reveals non-holomorphic structure in low-luminosity galaxy rotation curves

**Anthony Monnerot**

---

## Abstract

We introduce eml★, an anti-holomorphic extension of the EML operator (Odrzywołek 2019), into genetic programming symbolic regression applied to galaxy rotation curves. Through a characterization battery on synthetic complex fields, we establish that eml★ acts as a detector of non-holomorphic structure: it appears in 100% of anti-holomorphic targets (conj(z), conj(z)²) and 0% of holomorphic targets (z², exp(z)). Applied to 125 SPARC galaxies and 23 LITTLE THINGS dwarf galaxies, eml★ preferentially improves rotation curve fits for low-luminosity systems (Spearman rho = −0.27, p = 0.004). The signal reproduces on the independent LITTLE THINGS sample at a consistent rate. Neither MOND acceleration threshold (p = 0.35) nor dark matter fraction (p = 0.81) are significant predictors; luminosity alone best predicts eml★ response. These results suggest that the gravitational potential in dark-matter-dominated galaxies contains a non-holomorphic component that becomes detectable when the baryonic contribution is subdominant. We report all negative results (MOND, dark matter fraction, vortex topology tests) to constrain the interpretation. Code and sample data are available at github.com/antparis/eml_star. Full result tables will be released upon publication.

---

## 1. Introduction

The rotation curves of disk galaxies remain one of the most compelling observational signatures of dark matter. The SPARC database (Lelli, McGaugh & Schombert 2016) provides high-quality rotation curves for 175 galaxies with Spitzer 3.6μm photometry, enabling systematic comparisons between observed kinematics and baryonic mass models. The discrepancy between observed rotation velocities and those predicted by visible matter alone — the mass discrepancy — grows systematically in low-luminosity, dark-matter-dominated systems.

Symbolic regression, in which algorithms search for closed-form mathematical expressions that fit data, has emerged as a tool for scientific discovery (Schmidt & Lipson 2009). Unlike neural networks, symbolic regression produces interpretable formulas, enabling physical insight. Genetic programming (GP) implementations such as PySR (Cranmer 2023) and DEAP (Fortin et al. 2012) allow custom operator sets, making it possible to embed domain-specific mathematical structure into the search space.

Odrzywołek (2019) introduced the EML operator, defined as EML(x, y) = exp(x) − ln(y), which combines exponential and logarithmic functions in a single primitive. We extend this to the complex domain with three operators: eml(z, w) = exp(z) − ln(w), eml★(z, w) = exp(conj(z)) − ln(conj(w)), and conj_eml(z) = conj(eml(z, z)). The critical distinction is that eml★ incorporates complex conjugation, making it an anti-holomorphic operator. A function f(z) is holomorphic if ∂f/∂z̄ = 0 (the Cauchy-Riemann equations are satisfied); eml★ introduces ∂f/∂z̄ ≠ 0 into the search space.

This distinction has physical content. Many potentials in physics are holomorphic or harmonic functions of complex coordinates. When a physical system requires anti-holomorphic terms — when conjugation enters the governing equations — it signals a departure from the standard analytic structure. In the context of galaxy rotation curves, the appearance of eml★ in a symbolic regression fit implies that the underlying potential contains a non-holomorphic component that cannot be captured by standard (holomorphic) functions alone.

In this work, we first characterize eml★ on synthetic complex fields to establish its detection properties (Section 2.5, 3.1). We then apply GP with eml★ operators to 125 SPARC galaxies and 23 LITTLE THINGS dwarf galaxies, comparing fits with and without anti-holomorphic operators (Section 3.2, 3.3). We identify the physical properties that predict eml★ response (Section 3.4) and report negative results for MOND and dark matter fraction as predictors (Section 3.5). We discuss the interpretation of non-holomorphic structure in dark-matter-dominated potentials (Section 4).

---

## 2. Methods

### 2.1 The eml★ operator

We define three complex-valued operators derived from the EML operator of Odrzywołek (2019):

- eml(z, w) = exp(z) − ln(w)
- eml★(z, w) = exp(z̄) − ln(w̄)
- conj_eml(z) = conj(eml(z, z)) = conj(exp(z) − ln(z))

where z̄ denotes the complex conjugate of z. The operator eml★ is anti-holomorphic: it maps through the conjugation z → z̄ before applying analytic functions. In the Wirtinger calculus framework, a function f(z, z̄) satisfies ∂f/∂z̄ = 0 if and only if it is holomorphic. The inclusion of eml★ in the GP search space allows the algorithm to construct expressions with ∂f/∂z̄ ≠ 0, enabling detection of non-holomorphic structure in the target data.

### 2.2 Genetic programming implementation

We use the DEAP framework (Fortin et al. 2012) for tree-based genetic programming. The primitive set includes binary operators {+, −, ×, ÷, pow, eml, eml★} and unary operators {conj_eml, ln, log₁₀, sin, cos, exp, arcsin, arccos, arctan}. Constants include {0, 1, i, ½, 2, π} and ephemeral random constants drawn from U(−10, 10). All arithmetic is complex-valued with safe guards against overflow, division by zero, and logarithm of zero. A parsimony pressure of λ = 0.0002 × tree_size is added to the MSE fitness to penalize complexity. After evolution, constants in the best individual are refined via Nelder-Mead optimization (scipy.optimize.minimize).

Standard parameters: population = 300, generations = 60, 5 independent runs per galaxy, tournament selection (size 3), crossover probability 0.7, mutation probability 0.2, maximum tree depth 8.

### 2.3 Data

We use two datasets of galaxy rotation curves.

SPARC (Lelli, McGaugh & Schombert 2016): 175 galaxies with Spitzer 3.6μm photometry. Of these, 125 had sufficient data points for symbolic regression, and 111 had complete photometric and kinematic catalog entries used in all subsequent statistical analyses. Each rotation curve provides radius r, observed velocity V_obs, and baryonic velocity V_bar. We use r and V_bar as input variables (z0, z1) and V_obs as the target. Data are publicly available and were not modified.

LITTLE THINGS (Hunter et al. 2012): 23 dwarf irregular galaxies, providing an independent low-mass sample. Same input/output format as SPARC.

### 2.4 Experimental protocol

For each galaxy, we run two GP experiments: (1) with the full operator set including eml★, and (2) without anti-holomorphic operators (eml★ and conj_eml removed). Both use identical parameters and random seeds. The improvement metric is:

Δ = (MSE_without − MSE_with) / MSE_without × 100%

A galaxy is classified as "eml★-responsive" if the best formula from experiment (1) contains eml★ or conj_eml AND Δ > 10%. The 10% threshold excludes marginal improvements attributable to the larger operator set.

### 2.5 Synthetic characterization battery

To establish what eml★ detects independently of astrophysical data, we test six synthetic complex functions with 200 random points in [−2, 2] × [−2, 2]:

- H1: f(z) = z² (holomorphic polynomial)
- H2: f(z) = exp(z) (holomorphic transcendental)
- A1: f(z) = z̄ (anti-holomorphic pure)
- A2: f(z) = z̄² (anti-holomorphic squared)
- M1: f(z) = |z| (mixed nonlinear)
- M2: f(z) = Re(z) (mixed linear)

Each test uses 5 GP runs with standard parameters. If eml★ appears exclusively in non-holomorphic targets, we conclude that it acts as a non-holomorphicity detector rather than fitting arbitrary complex data.

---

## 3. Results

### 3.1 Characterization battery

Table 1 summarizes the synthetic characterization results.

| Test | Function | Category | eml★ runs | Best MSE |
|------|----------|----------|-----------|----------|
| H1 | z² | holomorphic | 0/5 | exact |
| H2 | exp(z) | holomorphic | 0/5 | exact |
| A1 | conj(z) | anti-holomorphic | 5/5 | exact |
| A2 | conj(z)² | anti-holomorphic | 5/5 | 1.32 |
| M1 | \|z\| | mixed nonlinear | 3/5 | 0.083 |
| M2 | Re(z) | mixed linear | 5/5 | 0.077 |

*Figure 3 summarizes the characterization battery results.*

The GP never selects eml★ for holomorphic targets (0/10 runs) and consistently selects it for anti-holomorphic targets (10/10 runs). For mixed targets containing implicit conjugation (|z| = √(z·z̄), Re(z) = (z+z̄)/2), eml★ appears in 8/10 runs. We conclude that eml★ acts as a non-holomorphicity detector: it is selected if and only if the target function depends on z̄.

### 3.2 SPARC galaxies

We applied the with/without protocol to 125 SPARC galaxies. Of the 125, 124 completed successfully (1 timeout). Of the 111 galaxies with complete catalog data, 51 (46%) were classified as eml★-responsive under the strict criterion. The raw PySR count before catalog matching was 58/125. The improvement distribution is bimodal: eml★-responsive galaxies show median Δ = +25%, while non-responsive galaxies show median Δ = −12%, indicating that eml★ degrades the fit when the underlying structure is holomorphic.

*Figure 2 shows the distribution of improvement Δ for eml★-responsive and non-responsive galaxies.*

### 3.3 LITTLE THINGS replication

We repeated the protocol on 23 LITTLE THINGS dwarf galaxies. 10 of 23 (43.5%) were classified as eml★-responsive, consistent with the SPARC rate. This replication on an independent, low-mass dataset strengthens the finding: the eml★ signal is not an artifact of the SPARC sample.

### 3.4 Physical property correlations

Table 2 shows the Spearman correlation between improvement Δ and galaxy properties from the SPARC catalog.

| Property | rho | p-value | Significant |
|----------|-----|---------|-------------|
| Vflat (km/s) | −0.281 | 0.003 | Yes |
| Luminosity (10⁹ L☉) | −0.273 | 0.004 | Yes |
| M_HI (10⁹ M☉) | −0.236 | 0.013 | Yes |
| Reff (kpc) | −0.264 | 0.005 | Yes |
| Surface brightness | −0.137 | 0.151 | No |

*Figure 1 shows the scatter plot of eml★ improvement versus luminosity.*

All significant correlations are negative: eml★ improvement increases as galaxies become smaller, slower, less luminous, and less gas-rich. These are characteristics of dark-matter-dominated systems. A logistic regression confirms that luminosity alone is the best predictor of eml★ response (AIC = 147.7 vs 153.7 for dark matter fraction).

Median physical properties of eml★-responsive vs non-responsive galaxies:

| Property | eml★ median | Non median | p-value |
|----------|-------------|------------|---------|
| Vflat (km/s) | 110.6 | 153.2 | 0.024 |
| Luminosity (10⁹ L☉) | 6.54 | 44.29 | 0.033 |
| Reff (kpc) | 2.94 | 4.33 | 0.015 |

### 3.5 Negative results

We report three negative results that constrain the interpretation of eml★.

MOND acceleration: The median centripetal acceleration of eml★ galaxies (1.14 × a₀) is not significantly different from non-eml★ galaxies (1.60 × a₀, Mann-Whitney p = 0.35). eml★ response does not track the Milgrom threshold.

Dark matter fraction: Using M_dyn = V²_flat × R_HI / G and M_bar = Υ_disk × L + 1.33 × M_HI with Υ_disk = 0.5, the dark matter fraction f_DM shows no correlation with eml★ improvement (Spearman rho = 0.023, p = 0.81). All galaxies in the sample are dark-matter-dominated (median f_DM = 0.80), so f_DM lacks discriminating power.

Vortex topology: Synthetic tests on optical vortex fields showed that eml★ appears in a fake vortex with zero amplitude but no phase winding (5/5 runs). eml★ detects non-holomorphic structure, not topological charge. This rules out the interpretation of eml★ as a topological detector.

---

## 4. Discussion

### 4.1 eml★ as a non-holomorphicity detector

The characterization battery (Section 3.1) establishes that eml★ is selected by the GP if and only if the target function depends on z̄. This is not a trivial result. The GP search space contains standard analytic functions (exp, ln, sin, cos, pow) that can approximate many complex functions. The fact that the GP consistently rejects eml★ for holomorphic targets and consistently selects it for anti-holomorphic ones demonstrates that the operator fills a genuine gap in the search space: it provides the only pathway to z̄-dependence.

In the Wirtinger formalism, any smooth function f of a complex variable can be decomposed as f(z, z̄) = g(z) + h(z̄) + mixed terms, where g is holomorphic and h is anti-holomorphic. The GP with eml★ effectively performs this decomposition empirically. When eml★ appears in the best formula, it signals the presence of h(z̄) or mixed terms — that is, the target cannot be expressed as a function of z alone.

### 4.2 Why low luminosity?

The correlation between eml★ response and low luminosity (rho = −0.27, p = 0.004) admits a simple interpretation. In high-luminosity galaxies, the baryonic contribution to the rotation curve is dominant, especially in the inner regions. The gravitational potential is well-described by standard (holomorphic) Newtonian terms. In low-luminosity galaxies, the baryonic contribution is subdominant: the rotation curve is shaped primarily by the dark matter halo. If the dark matter potential introduces a non-holomorphic component, it would be masked by the dominant baryonic signal in bright galaxies and revealed only when that signal is weak.

This is analogous to observing a faint star: it is invisible in daylight but detectable at night. The non-holomorphic component does not grow stronger in low-luminosity galaxies — it becomes detectable because the holomorphic baryonic foreground diminishes.

We emphasize that this interpretation is descriptive. We do not claim that dark matter is intrinsically non-holomorphic. The GP discovers that the mapping from (r, V_bar) to V_obs requires z̄-dependent terms in dark-matter-dominated systems. Whether this reflects a property of the dark matter potential, an interaction between baryonic and dark components, or a mathematical artifact of the coordinate representation remains open.

### 4.3 Limitations

Several limitations constrain the strength of our conclusions.

Hyperparameter sensitivity: The rate of eml★-responsive galaxies depends on GP parameters (population size, generations, maximum tree depth). Previous runs with lower power settings yielded approximately 15% rather than the 46% reported here. The qualitative result — that eml★ preferentially selects low-luminosity galaxies — is robust across settings, but the absolute rate is not a physical quantity.

Velocity confound: The correlation between eml★ improvement and luminosity cannot be fully separated from the correlation with rotation velocity (Vflat), galaxy size (Reff), or gas mass (M_HI). These properties are mutually correlated in disk galaxies. A partial correlation analysis controlling for Vflat reduces the significance of the fuzzy dark matter zone test from p = 0.008 to p = 0.15 (Section 3.5). Luminosity remains the strongest single predictor, but we cannot exclude that it serves as a proxy for a combination of physical properties.

Interpretive gap: eml★ detects non-holomorphic mathematical structure, but translating this into a specific physical mechanism requires additional theoretical work. The Wirtinger derivative ∂f/∂z̄ ≠ 0 is a necessary condition for non-holomorphicity, but it does not uniquely identify the physical source.

### 4.4 Comparison with existing approaches

MOND (Milgrom 1983) predicts a transition in dynamics at the acceleration scale a₀ ≈ 1.2 × 10⁻¹⁰ m/s². Our data show no significant difference in acceleration between eml★ and non-eml★ galaxies (p = 0.35), suggesting that eml★ captures a different aspect of the mass discrepancy than MOND.

NFW profiles (Navarro, Frenk & White 1996) describe dark matter halos as smooth, spherically symmetric density distributions. The non-holomorphic structure detected by eml★ may reflect departures from NFW symmetry in low-mass halos, consistent with the cusp-core problem in dwarf galaxies (de Blok 2010).

Fuzzy dark matter models (Hu, Barkana & Gruzinov 2000) predict wave-like behavior at the de Broglie scale. While our initial tests showed that eml★ galaxies preferentially occupy the "quantum zone" (Reff/λ_dB < 5, Fisher p = 0.002), this signal did not survive control for rotation velocity (p = 0.15). We cannot distinguish a fuzzy DM signature from a velocity-driven selection effect with the present data.

---

## 5. Conclusion

We introduced eml★, an anti-holomorphic extension of the EML operator, into genetic programming symbolic regression. Through synthetic characterization, we established that eml★ is selected by the GP exclusively when the target function depends on z̄, confirming its role as a non-holomorphicity detector.

Applied to 125 SPARC and 23 LITTLE THINGS galaxy rotation curves, eml★ preferentially improves fits for low-luminosity, dark-matter-dominated systems. The signal reproduces on the independent LITTLE THINGS sample. Luminosity is the best single predictor of eml★ response (rho = −0.27, p = 0.004); neither MOND acceleration nor dark matter fraction are significant predictors.

We summarize our findings by epistemic status:

Established: (1) eml★ detects non-holomorphic structure in complex-valued functions. (2) eml★ improvement correlates with low luminosity in galaxy rotation curves. (3) The signal replicates on an independent dataset.

Not established: (1) Whether the non-holomorphic component originates from the dark matter potential, from baryonic-dark matter interaction, or from the coordinate representation. (2) Whether eml★ response reflects a single physical mechanism or a combination of correlated galaxy properties.

Ruled out: (1) eml★ as a topological detector. (2) MOND acceleration as a predictor. (3) Dark matter fraction as a predictor.

The central open question is physical: why does the mapping from baryonic to observed kinematics require anti-holomorphic terms in dark-matter-dominated galaxies? Answering this will require theoretical work connecting the Wirtinger decomposition to gravitational potential theory, and observational work extending the analysis to independent datasets such as gravitational lensing fields and interferometric HI maps.

Code and sample data are available at github.com/antparis/eml_star. Full result tables will be released upon publication.

---

## References

- Cranmer, M. 2023, arXiv:2305.01582 (PySR)
- de Blok, W.J.G. 2010, Advances in Astronomy, 2010, 789293
- Fortin, F.-A. et al. 2012, Journal of Machine Learning Research, 13, 2171 (DEAP)
- Hu, W., Barkana, R. & Gruzinov, A. 2000, Physical Review Letters, 85, 1158
- Hunter, D.A. et al. 2012, AJ, 144, 134 (LITTLE THINGS)
- Lelli, F., McGaugh, S.S. & Schombert, J.M. 2016, AJ, 152, 157 (SPARC)
- Milgrom, M. 1983, ApJ, 270, 365
- Navarro, J.F., Frenk, C.S. & White, S.D.M. 1996, ApJ, 462, 563
- Odrzywołek, A. 2019, arXiv:1902.09425
- Schmidt, M. & Lipson, H. 2009, Science, 324, 81

---

## Appendix A — Best eml★ formulas for selected galaxies

We list the best-fit formulas containing eml★ for five galaxies with high improvement (Δ > 70%). Variables: r = radius, V_b = baryonic velocity. The overline notation (z̄) denotes complex conjugation — the anti-holomorphic component detected by eml★.

**KK98-251** (Δ = +73.9%, dwarf irregular)

GP output:

    sin(atan(x0) + sin(x0 * ((x0 + 0.40) * cos(cos(emlstar_re(x0, 0.43) * exp(x0))))))

LaTeX:

$$\sin\!\Big(\arctan(r) + \sin\!\big(r \cdot (r + 0.40) \cdot \cos(\cos(e^{\bar{r}} - \ln(\overline{0.43}) \cdot e^r))\big)\Big)$$

**UGC05721** (Δ = +93.1%, dwarf spiral)

GP output:

    cos((cos(x0) * double_emlstar(0.05, double_emlstar(0.27, atan(atan(x0))))) /
        cos(emlstar_self(cos(emlstar_self((sin(emlstar_re(-1.69, x0 + -0.10)) * x0) + x0)))))

LaTeX:

$$\cos\!\bigg(\frac{\cos(r) \cdot \text{eml★}\big(0.05,\; \text{eml★}(0.27, \arctan(\arctan(r)))\big)}{\cos\!\big(\text{eml★}(s, s)\big)}\bigg)$$

where $s = \sin(e^{\overline{-1.69}} - \ln(\overline{r - 0.10})) \cdot r + r$

**NGC3917** (Δ = +85.1%, Scd)

GP output:

    sin(atan((sqrt(emlstar_self(exp(atan(exp(cos(cos(exp(double_emlstar(x0, 0.16)))))))) - 3.00)
        * x0) * (atan(atan(sqrt(x0))) + sqrt(x0))))

LaTeX:

$$\sin\!\bigg(\arctan\!\Big(\big(\sqrt{\text{eml★}(g, g)} - 3.00\big) \cdot r\Big) \cdot \big(\arctan(\arctan(\sqrt{r})) + \sqrt{r}\big)\bigg)$$

where $g = e^{\arctan(e^{\cos(\cos(e^{\text{eml★}(r,\;0.16)}))})}$

**NGC4100** (Δ = +77.3%, Sbc)

GP output:

    sqrt(sin(emlstar_self(emlstar_self(emlstar_re(-0.13, x0)
        * ((x0 * (sin(x0 * 25.90) * 0.24)) + 3.59)))) + -0.02)

LaTeX:

$$\sqrt{\sin\!\Big(\text{eml★}\big(h, h\big)\Big) - 0.02}$$

where $h = \text{eml★}\big((e^{\overline{-0.13}} - \ln(\bar{r})) \cdot (0.24\,r\sin(25.9\,r) + 3.59),\; \text{self}\big)$

**NGC3972** (Δ = +76.7%, Sbc)

GP output:

    atan(x0 - atan((exp(-0.22 / x0) + (-0.79 / emlstar_re(0.54 / x0,
        cos(double_emlstar(x1, x0 / 5.59))))) / -0.67))

LaTeX:

$$\arctan\!\bigg(r - \arctan\!\Big(\frac{e^{-0.22/r} - \frac{0.79}{e^{\overline{0.54/r}} - \ln(\overline{\cos(\text{eml★}(V_b,\; r/5.59))})}}{-0.67}\Big)\bigg)$$

In all five cases, the conjugation operator (z̄) appears in nested positions within the formula tree, indicating that the anti-holomorphic contribution is not additive but multiplicatively coupled to the holomorphic structure. The constants have been rounded to two decimal places for readability; full-precision values are available in the supplementary data.

## Appendix B — Complete galaxy table

The complete table of 148 galaxies (125 SPARC + 23 LITTLE THINGS) with improvement Δ, eml★ flag, and physical properties is available as a machine-readable CSV file (master_galaxy_table.csv) in the supplementary materials and at github.com/antparis/eml_star upon publication.
