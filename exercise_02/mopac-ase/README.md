# Methane Combustion Enthalpy Using MOPAC PM7

## Objective

This exercise investigates the gas-phase combustion enthalpy of methane using the semi-empirical **PM7 method** implemented in MOPAC.

The calculations are performed through ASE and provide an opportunity to examine the accuracy and limitations of semi-empirical methods in predicting molecular thermochemical properties.

## Chemical reaction

The reaction considered is:

$$
\mathrm{CH_4(g)+2O_2(g)\rightarrow CO_2(g)+2H_2O(g)}
$$

The experimental gas-phase combustion enthalpy at 298.15 K is:

$$
\Delta_c H^\circ_{\mathrm{exp}}
=
-802.30\ \mathrm{kJ\,mol^{-1}}
$$

## Importance of the O₂ spin state

Molecular oxygen has a triplet ground electronic state.

Consequently, an appropriate unrestricted Hartree–Fock (UHF) treatment with triplet multiplicity is required for the oxygen calculation.

The MOPAC input therefore uses:

```text
TRIPLET UHF
```

Using an incorrect spin state would produce an inappropriate electronic reference energy and could significantly affect the calculated combustion enthalpy.

The calculation also examines possible systematic offsets associated with the PM7 description of homonuclear diatomic molecules.

## Computational procedure

The Python script

```text
methane_combustion_mopac_01.py
```

uses ASE to perform the molecular calculations with MOPAC.

The thermochemical analysis includes:

- Heats of formation of the reactants and products.
- Molecular equilibrium geometries.
- The contribution of the oxygen reference energy.
- The resulting reaction enthalpy.

## Interpretation of the results

The PM7 calculations provide a useful opportunity to distinguish between geometrical accuracy and thermochemical accuracy.

The analysis considers three main contributions:

1. **Molecular geometries and water energetics:** PM7 provides a reasonable description of the geometries of CH₄, CO₂, and H₂O and closely reproduces the experimental heat of formation of water.
2. **Oxygen reference energy:** A systematic error in the triplet O₂ energy can introduce a significant contribution to the calculated reaction enthalpy.
3. **Residual molecular-energy errors:** Additional deviations in the calculated CH₄ and CO₂ energies contribute to the overall reaction-energy difference.

These effects accumulate according to the stoichiometry of the combustion reaction.

## Execution

Run the calculation using:

```bash
python methane_combustion_mopac_01.py
```

MOPAC must be installed and accessible from the computational environment.

The saved logfile provides a reference for examining the calculation and its numerical output.

## Learning outcomes

This exercise illustrates:

- The application of semi-empirical quantum chemistry to reaction thermochemistry.
- The importance of spin multiplicity in molecular calculations.
- The influence of systematic errors in individual heats of formation.
- The relationship between molecular geometry and reaction-energy accuracy.

