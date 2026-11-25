# Diels–Alder Reaction Enthalpy Using MACE-OFF23

## Objective

This exercise investigates the gas-phase Diels–Alder reaction between 1,3-butadiene and ethene using the MACE-OFF23 machine-learning interatomic potential.

The purpose is to evaluate the performance of a machine-learning potential in describing a chemical reaction involving the formation of new carbon–carbon bonds and the transformation of two reactant molecules into a cyclic product.

All three molecules involved are closed-shell hydrocarbons:

- 1,3-Butadiene: C₄H₆.
- Ethene: C₂H₄.
- Cyclohexene: C₆H₁₀.

## Reference reaction enthalpy

The reaction is:

$$
\mathrm{C_4H_6(g)} + \mathrm{C_2H_4(g)} \rightarrow \mathrm{C_6H_{10}(g)}
$$

The experimental gas-phase reaction enthalpy at 298.15 K is:

$$
\Delta_r H^\circ_{\mathrm{exp}} = -166.70\ \mathrm{kJ\,mol^{-1}}
$$

The included MACE-OFF23 (medium) calculation predicts:

$$
\Delta_r H^\circ_{\mathrm{MACE}} = -173.35\ \mathrm{kJ\,mol^{-1}}
$$

The deviation from the experimental reference is:

$$
\left|\Delta_r H^\circ_{\mathrm{MACE}} - \Delta_r H^\circ_{\mathrm{exp}}\right| = 6.65\ \mathrm{kJ\,mol^{-1}}
$$

This corresponds to approximately 4.0% of the experimental reaction enthalpy.

## Electronic energy contribution

The calculated electronic reaction energy is:

$$
\Delta E_{\mathrm{elec}} = -192.17\ \mathrm{kJ\,mol^{-1}}
$$

This contribution reflects the energetic changes associated with the reorganization of the π-bond system and formation of two new C–C σ bonds.

The MACE-OFF23 model is based on a high-level organic-molecule training domain that includes reference calculations using ωB97M-D3(BJ)/def2-TZVPPD.

The exercise also compares this result with the electronic energy obtained using GFN2-xTB:

$$
\Delta E_{\mathrm{elec}}^{\mathrm{xTB}} = -282.18\ \mathrm{kJ\,mol^{-1}}
$$

This comparison illustrates how different computational approximations can produce substantially different electronic reaction energies.

## Zero-point energy contribution

The zero-point energy correction is:

$$
\Delta\mathrm{ZPE} = +26.97\ \mathrm{kJ\,mol^{-1}}
$$

The correction reflects the change in vibrational zero-point energy when two reactant molecules form a single cyclic product.

The formation of the ring changes the number and character of the vibrational modes, particularly the low-frequency molecular motions associated with translation, rotation, and ring deformation.

After the zero-point energy correction, the calculated reaction energy at 0 K is:

$$
\Delta E_{0K} = -165.20\ \mathrm{kJ\,mol^{-1}}
$$

## Thermal enthalpy contribution

The thermal contribution between 0 and 298.15 K is:

$$
\Delta H_{\mathrm{thermal}} = -8.15\ \mathrm{kJ\,mol^{-1}}
$$

This contribution includes the changes in translational, rotational, and vibrational enthalpy associated with the conversion of two gas-phase molecules into one product molecule.

Combining the electronic, zero-point, and thermal contributions gives:

$$
\Delta_r H^\circ(298.15\ \mathrm{K}) = \Delta E_{\mathrm{elec}} + \Delta\mathrm{ZPE} + \Delta H_{\mathrm{thermal}} = -192.17 + 26.97 - 8.15 = -173.35\ \mathrm{kJ\,mol^{-1}}
$$

## Structural analysis: C=C bond lengths

The optimized molecular structures provide additional information about the electronic structure of the reactants and product.

The calculated C=C bond lengths are:

| Molecule | C=C bond length (Å) |
| --- | --- |
| 1,3-Butadiene | 1.3278 |
| Cyclohexene | 1.3268 |
| Ethene | 1.3222 |

The slightly elongated C=C bond in 1,3-butadiene is associated with π-electron conjugation across the carbon framework.

The comparison illustrates how molecular geometry reflects differences in electronic delocalization.

## Execution

Run the calculation using:

```bash
python diels-alder-mace.py

