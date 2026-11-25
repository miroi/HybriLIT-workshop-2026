## Physical Breakdown of the MACE-OFF23 Diels–Alder Results

MACE-OFF23 (medium) achieves a reaction enthalpy of

`ΔrH°(298.15 K) = -173.35 kJ/mol`

landing within **6.65 kJ/mol (0.069 eV)** of the NIST experimental value (**−166.70 kJ/mol**).

Because all three hydrocarbons (**C₄H₆**, **C₂H₄**, and **C₆H₁₀**) are closed-shell singlets well inside its organic training domain (SPICE / QM7-X at the **ωB97M-D3(BJ)/def2-TZVPPD** level), MACE avoids the diatomic H₂ edge-case error seen in `exercise_03` and captures the physics of pericyclic ring formation.

### Balanced π → σ Bond Conversion

`ΔE_elec = -192.17 kJ/mol`

- Converting two C=C π bonds (one in *trans-1,3-butadiene* and one in *ethene*) into two new C-C σ bonds in half-chair *cyclohexene* is strongly exothermic.

- Because MACE-OFF23 is trained on range-separated hybrid DFT with dispersion (**ωB97M-D3(BJ)**), it avoids the systematic minimal-basis σ-overbinding of GFN2-xTB:

  `ΔE_elec = -282.18 kJ/mol`

  and accurately accounts for conjugation stabilization in *1,3-butadiene* versus ring strain in *cyclohexene*.

### Zero-Point Energy Penalty

**ΔZPE = +26.97 kJ/mol**

- Associating two nonlinear reactant molecules (36 internal vibrational modes + 12 translational/rotational degrees of freedom) into a single nonlinear product (42 internal modes + 6 translational/rotational degrees of freedom) converts six soft external translations/rotations into stiff internal ring-deformation and C-H bending modes.

- This raises the zero-point energy by **+26.97 kJ/mol** (closely matching the approximately **+22 to +25 kJ/mol** DFT/experimental zero-point shift), bringing the 0 K reaction energy to

  `ΔE₀K = -165.20 kJ/mol`

### Thermal Enthalpy Contribution

`ΔH_thermal(0 → 298.15 K) = -8.15 kJ/mol`

- Because two independent ideal-gas molecules (**2 × 4RT**) condense into one ideal-gas molecule (**1 × 4RT**), the reaction loses

  `4RT ≈ 9.9 kJ/mol`

  of translational/rotational enthalpy at 298.15 K.

- This loss is partially offset by low-frequency ring-puckering modes in *cyclohexene*, shifting

  `ΔE₀K`

  from **−165.20 kJ/mol** to

  `ΔrH°(298.15 K) = -173.35 kJ/mol`

### Conjugation Trend in C=C Bond Lengths

- Relaxed C=C distances reproduce the subtle electronic delocalization ordering:

  - **1,3-butadiene:** 1.3278 Å (elongated by π-conjugation across the central C-C single bond)
  - **cyclohexene:** 1.3268 Å
  - **ethene:** 1.3222 Å (localized double bond)

`1,3-butadiene (1.3278 Å) > cyclohexene (1.3268 Å) > ethene (1.3222 Å)`

This trend is consistent with increasing localization of the π bond.
