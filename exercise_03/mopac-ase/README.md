# Diels–Alder Reaction Enthalpy Using MOPAC PM7

## Objective

This exercise calculates the gas-phase reaction enthalpy of the Diels–Alder cycloaddition of 1,3-butadiene and ethene using the semi-empirical PM7 method implemented in MOPAC.

The calculations are performed through ASE.

The main objective is to evaluate the accuracy of PM7 in predicting the heats of formation of the reactants and product and to investigate how individual molecular-energy errors affect the calculated reaction enthalpy.

## Chemical reaction

The reaction considered is:

$$
\mathrm{C_4H_6(g)} + \mathrm{C_2H_4(g)} \rightarrow \mathrm{C_6H_{10}(g)}
$$

The experimental gas-phase reaction enthalpy at 298.15 K is:

$$
\Delta_r H^\circ_{\mathrm{exp}} = -166.70\ \mathrm{kJ\,mol^{-1}}
$$

## Computational methodology

The Python script `diels-alder-mopac_01.py` performs the molecular calculations using MOPAC and ASE.

The calculations provide the heats of formation of:

- 1,3-Butadiene.
- Ethene.
- Cyclohexene.

The reaction enthalpy is evaluated according to Hess's law:

$$
\Delta_r H^\circ
= \Delta_f H^\circ(\mathrm{C_6H_{10}})
- \Delta_f H^\circ(\mathrm{C_4H_6})
- \Delta_f H^\circ(\mathrm{C_2H_4})
$$

## Reference results

The included PM7 calculation gives:

$$
\Delta_r H^\circ_{\mathrm{PM7}} = -185.70\ \mathrm{kJ\,mol^{-1}}
$$

Compared with the experimental reference:

$$
\Delta_r H^\circ_{\mathrm{exp}} = -166.70\ \mathrm{kJ\,mol^{-1}}
$$

the calculated reaction is approximately 19.0 kJ mol⁻¹ more exothermic.

### Individual heats of formation

The calculated heats of formation are compared with the experimental reference values:

| Molecule | PM7 (kJ mol⁻¹) | Experimental reference (kJ mol⁻¹) |
| --- | --- | --- |
| 1,3-Butadiene | +113.67 | +110.00 |
| Ethene | +57.97 | +52.40 |
| Cyclohexene | −14.06 | −4.30 |

The deviations in the individual heats of formation accumulate when the reaction enthalpy is calculated.

The reactant contribution and product contribution therefore both influence the final reaction-energy error.

## Structural analysis

The optimized structures provide an additional means of assessing the PM7 description of the molecules.

The saved calculation results indicate C=C bond lengths in the approximate range of 1.330–1.336 Å.

This comparison illustrates that reasonable molecular geometries do not necessarily imply equally accurate reaction enthalpies.

## Execution

Run the calculation using:

```bash
python diels-alder-mopac_01.py
