# Methane Combustion Enthalpy Using MOPAC PM7

## Objective

This exercise investigates the gas-phase combustion enthalpy of methane using the semi-empirical PM7 method implemented in MOPAC.

The calculations are performed through ASE and provide an opportunity to examine the accuracy and limitations of semi-empirical methods in predicting molecular thermochemical properties.

## Chemical reaction

The reaction considered is:

$$
\mathrm{CH_4(g)} + 2\,\mathrm{O_2(g)} \rightarrow \mathrm{CO_2(g)} + 2\,\mathrm{H_2O(g)}
$$

The experimental gas-phase combustion enthalpy at 298.15 K is:

$$
\Delta_c H^\circ_{\mathrm{exp}} = -802.30\ \mathrm{kJ\,mol^{-1}}
$$

## Importance of the O₂ spin state

Molecular oxygen has a triplet ground electronic state.

Consequently, an appropriate unrestricted Hartree–Fock (UHF) treatment with triplet multiplicity is required for the oxygen calculation.

The MOPAC input therefore uses:

```text
TRIPLET UHF
