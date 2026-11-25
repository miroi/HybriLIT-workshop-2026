# Exercise 02 — Methane Combustion Enthalpy

## Objective

In this exercise, the standard gas-phase combustion enthalpy of methane is calculated using different computational approaches.

The exercise provides an opportunity to compare semi-empirical quantum chemistry, density functional theory (DFT), and machine-learning interatomic potentials in the description of molecular thermochemistry.

The central question is how accurately different computational methods reproduce the experimental enthalpy of a chemical reaction.

## Chemical reaction

The complete combustion of methane is described by:

$$
\mathrm{CH_4(g)} + 2\,\mathrm{O_2(g)} \rightarrow \mathrm{CO_2(g)} + 2\,\mathrm{H_2O(g)}
$$

The standard gas-phase combustion enthalpy at 298.15 K is approximately:

$$
\Delta_c H^\circ(298.15\ \mathrm{K}) = -802.30\ \mathrm{kJ\,mol^{-1}}
$$

This value corresponds to the lower heating value (LHV) because the water produced during combustion remains in the gaseous phase.

## Experimental reference data

The reaction enthalpy can be calculated using standard enthalpies of formation:

| Species | Standard enthalpy of formation (kJ mol⁻¹) |
| --- | --- |
| CH₄(g) | −74.87 |
| O₂(g) | 0.00 |
| CO₂(g) | −393.51 |
| H₂O(g) | −241.83 |

According to Hess's law:

$$
\Delta_c H^\circ = \sum_{\mathrm{products}} \nu_i \Delta_f H_i^\circ - \sum_{\mathrm{reactants}} \nu_i \Delta_f H_i^\circ
$$

Therefore,

$$
\Delta_c H^\circ = \left[ -393.51 + 2(-241.83) \right] - \left[ -74.87 + 2(0.00) \right] = -802.30\ \mathrm{kJ\,mol^{-1}}
$$

## Computational approaches

The reaction is investigated using three different computational methods.

### 1. MACE

The MACE-MP-0 model is used to calculate molecular energies and thermochemical properties. Particular attention is given to the description of molecular oxygen in its triplet ground state and the influence of the underlying PBE electronic-structure description.

### 2. MOPAC

The semi-empirical PM7 method is used to calculate the thermochemical properties of the reactants and products. The correct triplet electronic state of O₂ is essential for obtaining a meaningful reaction energy.

### 3. NWChem

The reaction is investigated using density functional theory with the B3LYP exchange-correlation functional and the 6-311++G** basis set.

## Scientific questions

The exercise illustrates several important aspects of computational thermochemistry:

- How does the choice of computational method affect the predicted reaction enthalpy?
- How important is the correct electronic spin state of molecular oxygen?
- How do errors in individual molecular energies propagate into reaction energies?
- What is the contribution of zero-point energy and thermal corrections?
- Why can accurate equilibrium geometries coexist with significant errors in reaction enthalpies?

## Expected outcome

By completing this exercise, participants should be able to calculate a reaction enthalpy from molecular thermochemical data, compare different computational approaches, and identify the principal sources of disagreement with experimental reference values.

Note: All calculations in this exercise use gaseous water as the combustion product. The corresponding reference value is therefore the lower heating value, not the higher heating value.
