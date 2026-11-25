# Exercise 03 — Diels–Alder [4+2] Cycloaddition

## Objective

This exercise investigates the thermochemistry of the Diels–Alder reaction, an important pericyclic reaction in organic chemistry.

The reaction considered is the [4+2] cycloaddition of 1,3-butadiene and ethene to form cyclohexene.

The main objective is to calculate the reaction enthalpy using different computational methods and investigate the contributions of electronic energy, zero-point vibrational energy, and thermal corrections.

## Chemical reaction

The reaction is:

$$
\mathrm{C_4H_6(g)+C_2H_4(g)\rightarrow C_6H_{10}(g)}
$$

where 1,3-butadiene reacts with ethene to produce cyclohexene.

The experimental gas-phase reaction enthalpy at 298.15 K used as the reference is:

$$
\Delta_r H^\circ_{\mathrm{exp}}
=
-166.70\ \mathrm{kJ\,mol^{-1}}
$$

## Computational approaches

The reaction is investigated using two computational methods.

### 1. MACE-OFF23

[`mace-ase/`](mace-ase/README.md)

The MACE-OFF23 machine-learning interatomic potential is used to calculate the molecular energies, optimize the molecular geometries, and evaluate the reaction enthalpy.

The analysis includes:

- Electronic reaction energy.
- Zero-point energy correction.
- Thermal enthalpy contribution.
- Optimized C=C bond lengths.
- Comparison with the experimental reaction enthalpy.

### 2. MOPAC PM7

[`mopac-ase/`](mopac-ase/README.md)

The semi-empirical PM7 method is used to calculate the heats of formation of the reactants and product.

The reaction enthalpy is obtained from the corresponding thermochemical data, and the individual molecular contributions are compared with experimental reference values.

## Scientific discussion

The Diels–Alder reaction provides an interesting example of how computational methods describe changes in molecular bonding.

During the cycloaddition:

- The π-bond framework of the reactants is reorganized.
- Two new carbon–carbon σ bonds are formed.
- The molecular connectivity changes from two separate molecules to one cyclic product.
- The vibrational spectrum changes as the new molecular structure is formed.

These structural changes influence the electronic energy and vibrational contributions to the reaction enthalpy.

## Additional challenge

The exercise overview also refers to a cyclopentadiene challenge as a related problem for further investigation.

The numerical results currently documented in the method-specific directories concern the reaction of 1,3-butadiene with ethene.

## Execution

The calculations are performed using the Python scripts in the corresponding method directories.

Refer to the individual READMEs for execution instructions.

## Learning outcomes

By completing this exercise, participants should understand:

- The computational description of pericyclic reactions.
- The calculation of reaction enthalpies from molecular energies.
- The importance of zero-point and thermal corrections.
- The relationship between molecular geometry and chemical bonding.
- The strengths and limitations of machine-learning and semi-empirical methods in reaction thermochemistry.

