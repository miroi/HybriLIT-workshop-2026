
# Exercise 04: Molecular Magnetizability of H₂

## Objective

This exercise investigates the magnetic-response properties of molecular hydrogen (H₂) using PySCF and the Atomic Simulation Environment (ASE).

The main objective is to calculate the molecular magnetizability tensor using the Gauge-Including Atomic Orbital (GIAO) method.

Magnetizability describes the response of the electronic energy to an external magnetic field. It provides information about the diamagnetic and paramagnetic contributions to the magnetic properties of a molecule.

Molecular hydrogen is used as a simple closed-shell system for exploring these properties using quantum-chemical methods.

## Computational methodology

The calculation uses the following methods and software:

- **Electronic-structure program:** PySCF
- **Geometry optimization:** ASE with the BFGS optimizer
- **Exchange-correlation functional:** B3LYP
- **Basis set:** aug-cc-pVTZ
- **Magnetic-response method:** Gauge-Including Atomic Orbitals (GIAO)

The calculation is performed by the Python script `magnetizability_h2_pyscf.py`.

It consists of two main computational steps.

### 1. Geometry optimization

The equilibrium geometry of H₂ is optimized using the ASE BFGS algorithm.

The maximum-force convergence criterion is:

$$
f_{\max} = 0.001\ \mathrm{eV\,\AA^{-1}}
$$

A custom ASE calculator evaluates molecular energies and forces using PySCF. The electronic-structure calculation uses restricted Kohn–Sham density functional theory (RKS-DFT) with the B3LYP functional and aug-cc-pVTZ basis set.

The numerical integration grid is set to level 4.

### 2. GIAO magnetizability calculation

After geometry optimization, the magnetizability tensor is calculated analytically using the PySCF magnetizability property implementation.

The total magnetizability tensor contains diamagnetic and paramagnetic contributions:

$$
\boldsymbol{\chi}
=
\boldsymbol{\chi}^{d}
+
\boldsymbol{\chi}^{p}
$$

The tensor is defined as the negative second derivative of the molecular energy with respect to the external magnetic field:

$$
\chi_{\alpha\beta}
=
-\left.
\frac{\partial^2 E}
{\partial B_\alpha\,\partial B_\beta}
\right|_{\mathbf{B}=\mathbf{0}}
$$

Two useful quantities derived from the tensor are the isotropic magnetizability and the magnetizability anisotropy.

The isotropic magnetizability is calculated as:

$$
\chi_{\mathrm{iso}}
=
\frac{1}{3}\operatorname{Tr}(\boldsymbol{\chi})
$$

The magnetizability anisotropy is defined as:

$$
\Delta\chi
=
\chi_{\parallel}
-
\chi_{\perp}
$$

Here, $\chi_{\parallel}$ and $\chi_{\perp}$ are the magnetizabilities parallel and perpendicular to the molecular axis, respectively.

These quantities describe the average magnetic response and its dependence on the orientation of the molecule relative to the applied magnetic field.

## Reference results

The included PySCF calculation gives the following results:

| Property | PySCF (B3LYP/aug-cc-pVTZ) | Experimental reference |
|:---|---:|---:|
| H–H equilibrium bond length (Å) | 0.7429 | 0.7414 |
| Isotropic magnetizability (a.u.) | −0.8582 | −0.847 |
| Isotropic magnetizability (SI) (J/T²) | −6.77 × 10⁻²⁹ | −6.68 × 10⁻²⁹ |
| Molar magnetic susceptibility (cm³/mol) | −4.08 × 10⁻⁶ | −4.02 × 10⁻⁶ |
| Magnetizability anisotropy (a.u.) | +0.1085 | +0.114 |

The calculated isotropic magnetizability differs from the experimental reference by approximately 1.3%.

The negative isotropic magnetizability is consistent with the diamagnetic response of closed-shell molecular hydrogen. The positive anisotropy reflects the directional dependence of the molecular magnetic response.

## Unit conversions

The magnetizability is reported in atomic units and SI units.

The atomic unit used in the calculation is:

$$
1\ \mathrm{a.u.}
=
\frac{e^2 a_0^2}{m_e}
$$

where $e$ is the elementary charge, $a_0$ is the Bohr radius, and $m_e$ is the electron mass.

The calculation also reports the molar magnetic susceptibility in cgs units, allowing comparison with experimental molecular magnetic data.

## Installation

Install the required Python packages:

```bash
conda install -c conda-forge ase pyscf
pip install pyscf-properties
```

Make sure that the packages are installed in the Python environment used for the workshop.

## Execution

Run the calculation from the `exercise_04` directory:

```bash
python magnetizability_h2_pyscf.py
```

The script performs the following operations:

1. Creates the H₂ molecule using ASE.
2. Optimizes the H–H bond length using BFGS and PySCF.
3. Calculates the GIAO magnetizability tensor.
4. Determines the isotropic magnetizability and anisotropy.
5. Converts the results to SI and cgs units.
6. Prints the calculated properties and reference values.

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

