# Exercise 04 — Molecular Magnetizability of H₂

## Objective

This exercise investigates the magnetic-response properties of molecular hydrogen (H₂) using PySCF and the Atomic Simulation Environment (ASE).

The main objective is to calculate the molecular magnetizability tensor using the Gauge-Including Atomic Orbital (GIAO) formalism.

Magnetizability describes the response of the electronic energy to an external magnetic field. It provides information about the diamagnetic and paramagnetic contributions to the magnetic properties of a molecule.

Molecular hydrogen is used as a simple closed-shell system for exploring these properties using quantum-chemical methods.

## Computational methodology

The calculation is performed using:

- Electronic-structure program: PySCF
- Geometry optimization: ASE with the BFGS optimizer
- Exchange-correlation functional: B3LYP
- Basis set: aug-cc-pVTZ
- Magnetic-response method: Gauge-Including Atomic Orbitals (GIAO)

The Python script `magnetizability_h2_pyscf.py` performs two main computational steps.

### 1. Geometry optimization

The equilibrium geometry of H₂ is optimized using the ASE BFGS algorithm.

The maximum-force convergence criterion is:

$$
f_{\max} = 0.001\ \mathrm{eV}\,\mathrm{\mathring{A}}^{-1}
$$

A custom ASE calculator provides the molecular energies and forces through PySCF using restricted Kohn–Sham DFT at the B3LYP/aug-cc-pVTZ level.

The numerical integration grid is set to level 4.

### 2. GIAO magnetizability calculation

After geometry optimization, the magnetizability tensor is calculated analytically using the PySCF magnetizability property implementation.

The total magnetizability tensor contains diamagnetic and paramagnetic contributions:

$$
\boldsymbol{\chi} = \boldsymbol{\chi}^{d} + \boldsymbol{\chi}^{p}
$$

The tensor is defined as the second derivative of the molecular energy with respect to the external magnetic field:

$$
\chi_{\alpha\beta} =
\left. \frac{\partial^2 E(\mathbf{B})}
{\partial B_\alpha \partial B_\beta} \right|_{\mathbf{B}=\mathbf{0}}
$$

Two useful quantities derived from the tensor are the isotropic magnetizability and the magnetizability anisotropy.

The isotropic magnetizability is:

$$
\chi_{\mathrm{iso}} = \frac{1}{3}\operatorname{Tr}(\boldsymbol{\chi})
$$

The magnetizability anisotropy is:

$$
\Delta\chi = \chi_{\parallel} - \chi_{\perp}
$$

These quantities describe the average magnetic response and its dependence on the orientation of the molecule relative to the applied magnetic field.

## Reference results

The included PySCF calculation gives the following results:

| Property | PySCF (B3LYP/aug-cc-pVTZ) | Experimental reference |
|---|---|---|
| H–H equilibrium bond length (Å) | 0.7429 | 0.7414 |
| Isotropic magnetizability (a.u.) | −0.8582 | −0.847 |
| Isotropic magnetizability (SI) (J/T²) | −6.77 × 10⁻²⁹ | −6.68 × 10⁻²⁹ |
| Molar magnetic susceptibility (cm³/mol) | −4.08 × 10⁻⁶ | −4.02 × 10⁻⁶ |
| Magnetizability anisotropy (a.u.) | +0.1085 | +0.114 |

The calculated isotropic magnetizability differs from the experimental reference by approximately 1.3%.

The negative isotropic magnetizability is consistent with the diamagnetic response of closed-shell molecular hydrogen.

The positive anisotropy reflects the directional dependence of the molecular magnetic response.

## Unit conversions

The magnetizability is reported in atomic units and SI units.

The atomic unit used in the calculation is:

$$
1\ \mathrm{a.u.} = \frac{e^2 a_0^2}{m_e}
$$

The calculation also reports the molar magnetic susceptibility in cgs units, allowing comparison with experimental molecular magnetic data.

## Execution

Install the required Python packages:

```bash
conda install -c conda-forge ase pyscf
pip install pyscf-properties
