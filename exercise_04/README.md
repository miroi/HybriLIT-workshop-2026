
# Exercise 04 — Molecular Magnetizability of H₂

## Objective

In this exercise, you will calculate the magnetic-response properties of molecular hydrogen (H₂) using **PySCF** and the **Atomic Simulation Environment (ASE)**.

The main objective is to calculate the molecular magnetizability tensor using the Gauge-Including Atomic Orbital (GIAO) method.

Magnetizability describes how the energy of a molecule responds to an external magnetic field. It provides information about the diamagnetic and paramagnetic contributions to the molecular magnetic response.

H₂ is a useful test system because it is a simple, closed-shell molecule.

## Computational methodology

The calculation uses the following methods and software:

| Component | Method or software |
|---|---|
| Electronic-structure program | PySCF |
| Geometry optimization | ASE with the BFGS optimizer |
| Density-functional approximation | B3LYP |
| Basis set | aug-cc-pVTZ |
| Magnetic-response method | GIAO |
| Numerical integration grid | PySCF grid level 4 |

The calculation is performed by the Python script `magnetizability_h2_pyscf.py`.

It consists of two main stages.

### 1. Geometry optimization

The H₂ geometry is optimized using the ASE BFGS algorithm. Molecular energies and forces are evaluated by a custom ASE calculator that calls PySCF.

The electronic-structure calculation uses restricted Kohn–Sham DFT (RKS) with the B3LYP functional and aug-cc-pVTZ basis set.

The geometry optimization uses the following maximum-force convergence criterion:

\[
f_{\max}=0.001\ \mathrm{eV\,\AA^{-1}}
\]

### 2. GIAO magnetizability calculation

After geometry optimization, the magnetizability tensor is calculated analytically using the PySCF magnetizability implementation.

The total magnetizability tensor contains diamagnetic and paramagnetic contributions:

\[
\boldsymbol{\chi}
=
\boldsymbol{\chi}^{d}
+
\boldsymbol{\chi}^{p}
\]

It is defined in terms of the second derivative of the molecular energy with respect to the external magnetic field:

\[
\chi_{\alpha\beta}
=
-\left.
\frac{\partial^2 E}
{\partial B_\alpha\,\partial B_\beta}
\right|_{\mathbf B=\mathbf 0}
\]

Two useful quantities derived from the tensor are the isotropic magnetizability and the magnetizability anisotropy.

The isotropic magnetizability is the average of the three diagonal tensor components:

\[
\chi_{\mathrm{iso}}
=
\frac{1}{3}\operatorname{Tr}(\boldsymbol{\chi})
\]

For a diatomic molecule, the magnetizability anisotropy is defined as:

\[
\Delta\chi
=
\chi_{\parallel}
-
\chi_{\perp}
\]

where \(\chi_{\parallel}\) and \(\chi_{\perp}\) are the magnetizabilities parallel and perpendicular to the molecular axis, respectively.

These quantities describe the average magnetic response and its dependence on the orientation of the molecule relative to the applied magnetic field.

## Reference results

The included calculation reports the following results at the B3LYP/aug-cc-pVTZ level:

| Property | PySCF calculation | Experimental reference |
|---|---:|---:|
| H–H equilibrium bond length (Å) | 0.7429 | 0.7414 |
| Isotropic magnetizability (a.u.) | −0.8582 | −0.847 |
| Isotropic magnetizability (J/T²) | −6.77 × 10⁻²⁹ | −6.68 × 10⁻²⁹ |
| Molar magnetic susceptibility (cm³/mol) | −4.08 × 10⁻⁶ | −4.02 × 10⁻⁶ |
| Magnetizability anisotropy (a.u.) | +0.1085 | +0.114 |

The calculated isotropic magnetizability differs from the experimental reference by approximately 1.3%.

The negative isotropic magnetizability is consistent with the diamagnetic response of closed-shell molecular hydrogen. The positive anisotropy indicates that the magnetic response depends on the orientation of the molecule relative to the applied field.

*Note: The numerical values above are the reference values documented for this exercise. They should be checked against the output produced by the script when changing software versions or computational settings.*

## Unit conversions

The magnetizability is calculated in atomic units (a.u.) and converted to SI and cgs units.

The atomic unit used by the script is:

\[
1\ \mathrm{a.u.}
=
\frac{e^2a_0^2}{m_e}
\]

The conversion factors used in the script are:

\[
1\ \mathrm{a.u.}
=
7.8910366\times10^{-29}\ \mathrm{J\,T^{-2}}
\]

and

\[
1\ \mathrm{a.u.}
=
4.751991\times10^{-6}\ \mathrm{cm^3\,mol^{-1}}
\]

The latter conversion gives the molar magnetic susceptibility in cgs units.

## Installation

Run the following commands in the Python environment used for the workshop:

```bash
conda install -c conda-forge numpy ase pyscf
pip install pyscf-properties
```

Make sure that all packages are installed in the same environment and that the `python` command refers to that environment.

## Execution

From the `exercise_04` directory, run:

```bash
python magnetizability_h2_pyscf.py
```

The script performs the following operations:

1. Creates the H₂ molecule using ASE.
2. Optimizes the H–H bond length using BFGS and PySCF.
3. Calculates the GIAO magnetizability tensor.
4. Determines the isotropic magnetizability and anisotropy.
5. Converts the results to SI and cgs units.
6. Prints a summary of the calculated properties and experimental reference values.

A calculation logfile is included in this directory for comparison.

## Learning outcomes

After completing this exercise, you should be able to:

- Optimize a molecular geometry using ASE and PySCF.
- Perform a DFT calculation using the B3LYP functional and an augmented triple-zeta basis set.
- Explain the purpose of the GIAO method in magnetic-response calculations.
- Calculate and interpret a molecular magnetizability tensor.
- Distinguish diamagnetic and paramagnetic contributions to magnetic response.
- Calculate isotropic magnetizability and magnetic anisotropy.
- Compare calculated magnetic properties with experimental reference data.

This exercise introduces molecular magnetic-response calculations and illustrates how quantum-chemical methods can be used to investigate properties beyond conventional molecular energies and geometries.

