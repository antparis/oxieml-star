"""Generate publication-quality figures for the eml★ galaxy paper."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import csv

# Load data
rows = []
with open('master_galaxy_table.csv', 'r') as f:
    reader = csv.DictReader(f)
    for r in reader:
        try:
            row = {
                'name': r['name'],
                'luminosity': float(r['luminosity']) if r['luminosity'] else None,
                'improvement_pct': float(r['improvement_pct']) if r['improvement_pct'] else None,
                'uses_emlstar': r['uses_emlstar'].strip().lower() == 'true',
                'vflat': float(r['vflat']) if r.get('vflat') and r['vflat'] else None,
            }
            rows.append(row)
        except (ValueError, KeyError):
            continue

print(f"Loaded {len(rows)} galaxies")

# Filter valid
valid = [r for r in rows if r['luminosity'] is not None 
         and r['improvement_pct'] is not None
         and r['luminosity'] > 0]
print(f"Valid (with luminosity): {len(valid)}")

lum = np.array([r['luminosity'] for r in valid])
imp = np.array([r['improvement_pct'] for r in valid])
eml = np.array([r['uses_emlstar'] for r in valid])
log_lum = np.log10(lum)

# === FIGURE 1: Luminosity vs Improvement ===
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(log_lum[eml], imp[eml], c='#2ca02c', s=40, alpha=0.7, 
           label=f'eml★ active (n={eml.sum()})', zorder=3, edgecolors='k', linewidths=0.3)
ax.scatter(log_lum[~eml], imp[~eml], c='#d62728', s=40, alpha=0.7,
           label=f'eml★ inactive (n={(~eml).sum()})', zorder=3, edgecolors='k', linewidths=0.3)

# Spearman correlation
rho, pval = stats.spearmanr(log_lum, imp)
ax.set_xlabel('log₁₀(Luminosity) [L☉]', fontsize=13)
ax.set_ylabel('Improvement (%)', fontsize=13)
ax.set_title('eml★ improvement vs galaxy luminosity', fontsize=14)
ax.legend(fontsize=11)
ax.text(0.02, 0.98, f'Spearman ρ = {rho:.3f}\np = {pval:.4f}', 
        transform=ax.transAxes, fontsize=11, va='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig1_luminosity_vs_improvement.png', dpi=300, bbox_inches='tight')
plt.savefig('fig1_luminosity_vs_improvement.pdf', bbox_inches='tight')
print("Figure 1 saved: fig1_luminosity_vs_improvement.png/pdf")
plt.close()

# === FIGURE 2: Histogram of improvement ===
fig, ax = plt.subplots(figsize=(8, 5))
imp_eml = imp[eml]
imp_no = imp[~eml]
bins = np.linspace(min(imp), max(imp), 25)
ax.hist(imp_eml, bins=bins, alpha=0.7, color='#2ca02c', label=f'eml★ active (n={len(imp_eml)})', edgecolor='k', linewidth=0.5)
ax.hist(imp_no, bins=bins, alpha=0.7, color='#d62728', label=f'eml★ inactive (n={len(imp_no)})', edgecolor='k', linewidth=0.5)
ax.set_xlabel('Improvement (%)', fontsize=13)
ax.set_ylabel('Count', fontsize=13)
ax.set_title('Distribution of eml★ improvement across galaxies', fontsize=14)
ax.legend(fontsize=11)
ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)

# Mann-Whitney
if len(imp_eml) > 0 and len(imp_no) > 0:
    u_stat, u_pval = stats.mannwhitneyu(imp_eml, imp_no, alternative='greater')
    ax.text(0.98, 0.98, f'Mann-Whitney p = {u_pval:.4f}', 
            transform=ax.transAxes, fontsize=11, va='top', ha='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig2_improvement_histogram.png', dpi=300, bbox_inches='tight')
plt.savefig('fig2_improvement_histogram.pdf', bbox_inches='tight')
print("Figure 2 saved: fig2_improvement_histogram.png/pdf")
plt.close()

# === FIGURE 3: Characterization battery ===
tests = ['H1\nz²', 'H2\nexp(z)', 'A1\nconj(z)', 'A2\nconj(z)²', 'M1\n|z|', 'M2\nRe(z)']
eml_scores = [0, 0, 5, 5, 3, 5]  # out of 5
colors = ['#d62728', '#d62728', '#2ca02c', '#2ca02c', '#ff7f0e', '#2ca02c']
categories = ['Holomorphic', 'Holomorphic', 'Anti-holo', 'Anti-holo', 'Mixed', 'Mixed']

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(range(len(tests)), eml_scores, color=colors, edgecolor='k', linewidth=0.8)
ax.set_xticks(range(len(tests)))
ax.set_xticklabels(tests, fontsize=11)
ax.set_ylabel('eml★ activations (out of 5 runs)', fontsize=13)
ax.set_title('Characterization battery: eml★ as non-holomorphicity detector', fontsize=14)
ax.set_ylim(0, 5.5)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, eml_scores)):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
            f'{val}/5', ha='center', va='bottom', fontsize=12, fontweight='bold')

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#d62728', label='Holomorphic (expect 0)'),
                   Patch(facecolor='#2ca02c', label='Anti-holomorphic (expect 5)'),
                   Patch(facecolor='#ff7f0e', label='Mixed')]
ax.legend(handles=legend_elements, fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('fig3_characterization_battery.png', dpi=300, bbox_inches='tight')
plt.savefig('fig3_characterization_battery.pdf', bbox_inches='tight')
print("Figure 3 saved: fig3_characterization_battery.png/pdf")
plt.close()

print("\n=== All 3 figures generated ===")
