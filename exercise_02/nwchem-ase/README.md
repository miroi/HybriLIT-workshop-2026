# Methane Combustion Enthalpy Using NWChem's DFT

## Objective

This exercise calculates the gas-phase combustion enthalpy of methane using density functional theory (DFT) as implemented in NWChem.

The calculation employs the B3LYP exchange-correlation functional and the 6-311++G** basis set.

The purpose is to investigate the performance of a conventional hybrid-DFT approach in predicting molecular geometries and reaction thermochemistry.

## Chemical reaction

The reaction is:

$$
\mathrm{CH_4(g)} + 2\,\mathrm{O_2(g)} \rightarrow \mathrm{CO_2(g)} + 2\,\mathrm{H_2O(g)}
$$

The experimental gas-phase reaction enthalpy at 298.15 K is:

$$
\Delta_c H^\circ_{\mathrm{exp}} = -802.30\ \mathrm{kJ\,mol^{-1}}
$$

## Computational methodology

The calculations are performed using:

- Electronic-structure program: NWChem.
- Exchange-correlation functional: B3LYP.
- Basis set: 6-311++G**.
- Molecular oxygen: Triplet electronic state.

The molecular energies and geometries are used to evaluate the reaction enthalpy.

## Reference results

The included NWChem calculation reports:

$$
\Delta_c H^\circ(298.15\ \mathrm{K}) = -750.51\ \mathrm{kJ\,mol^{-1}}
$$

This differs from the experimental reference by approximately 51.8 kJ mol⁻¹.

The optimized geometries show good agreement with the cited experimental bond lengths:

| Molecule | Bond | Calculated distance (Å) | Experimental reference (Å) |
| --- | --- | --- | --- |
| O₂ (triplet) | O=O | 1.2062 | 1.208 |
| CO₂ | C=O | 1.1608 | 1.160 |
| CH₄ | C–H | 1.0908 | 1.086 |
| H₂O | O–H | 0.9621 | 0.957 |

The calculated bond lengths are close to the corresponding experimental values.

## Discussion of thermochemical accuracy

The results illustrate an important distinction between geometrical accuracy and reaction-energy accuracy.

Although B3LYP/6-311++G** provides good equilibrium geometries, the calculated combustion enthalpy differs appreciably from the experimental value.

The combustion reaction involves the conversion of open-shell triplet O₂ into closed-shell molecular products. Consequently, differences in the description of electron correlation between reactants and products can affect the final reaction energy.

Basis-set incompleteness can also contribute to the remaining discrepancy.

The results therefore provide a useful example of why agreement in equilibrium molecular structures does not necessarily guarantee comparable accuracy in reaction thermochemistry.

## Execution

Run the calculation using:

```bash
python methane_combustion_nwchem.py
