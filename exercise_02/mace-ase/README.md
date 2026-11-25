# Methane Combustion Enthalpy Using MACE and ASE

## Objective

This exercise calculates the gas-phase combustion enthalpy of methane using the MACE-MP-0 machine-learning interatomic potential and the Atomic Simulation Environment (ASE).

The main objective is to evaluate how a machine-learning potential trained on density-functional-theory reference data describes a chemical reaction involving both closed-shell molecules and open-shell molecular oxygen.

## Choice of MACE model

The calculation uses the `mace_mp` model rather than MACE-OFF23.

This choice is important because molecular oxygen has a triplet ground state:

$$
\mathrm{O_2}:\ {}^3\Sigma_g^-
$$

Standard MACE-OFF23 is designed for closed-shell organic molecules and does not provide the spin-state treatment required for this oxygen reference.

MACE-MP-0, in contrast, is based on spin-polarized PBE/PBE+U calculations from the Materials Project dataset. The triplet state of O₂ is therefore more appropriately represented within the model's underlying training framework.

The calculation also specifies the appropriate spin multiplicity for O₂ when using ASE's `IdealGasThermo` thermochemistry implementation.

## Computational workflow

The Python script `methane_combustion_mace.py` performs the calculations required to evaluate the combustion reaction.

The thermochemical analysis considers:

- Molecular energies of the reactants and products.
- Equilibrium molecular geometries.
- Vibrational frequencies.
- Zero-point energy corrections.
- Thermal contributions to the enthalpy.

The calculated reaction enthalpy is compared with the experimental gas-phase reference value.

## Reference result

The included MACE-MP-0 (medium) calculation gives:

$$
\Delta_c H^\circ(298.15\ \mathrm{K}) = -743.24\ \mathrm{kJ\,mol^{-1}}
$$

The experimental reference is:

$$
\Delta_c H^\circ_{\mathrm{exp}} = -802.30\ \mathrm{kJ\,mol^{-1}}
$$

The difference is approximately 59 kJ mol⁻¹, corresponding to about 7.4% of the experimental value.

## Interpretation of the results

An important contribution to this discrepancy is the known tendency of the underlying PBE approximation to overbind molecular oxygen.

Because two O₂ molecules occur on the reactant side of the combustion reaction, errors in the oxygen reference energy can have a substantial effect on the calculated reaction enthalpy.

The included analysis discusses the relationship between the MACE-MP-0 prediction and the corresponding PBE electronic-structure description.

The harmonic zero-point energy correction reported in the calculation is:

$$
\Delta\mathrm{ZPE} = +8.83\ \mathrm{kJ\,mol^{-1}}
$$

The vibrational analysis also provides an opportunity to examine molecular symmetry and the degeneracy of vibrational modes in CO₂ and CH₄.

## Execution

Run the calculation using:

```bash
python methane_combustion_mace.py
