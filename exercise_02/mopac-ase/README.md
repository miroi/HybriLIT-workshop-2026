# Methane Burning Enthalpy Calculation with MOPAC

## Why `TRIPLET UHF` Is Essential for $\text{O}_2$

- **Spin multiplicity:** Ground-state $\text{O}_2$ requires `TRIPLET UHF` to avoid forcing an inaccurate, high-energy closed-shell singlet state.
- **Diatomic reference check:** Comparing raw and adjusted $\text{O}_2$ values lets students check for homonuclear diatomic offsets in PM7.

## Physical Breakdown of the MOPAC PM7 Results

- **Accurate Geometries & $\text{H}_2\text{O}$:** PM7 closely matches experimental formation enthalpy for $\text{H}_2\text{O}$ and bond lengths for $\text{CH}_4$, $\text{CO}_2$, and $\text{H}_2\text{O}$.
- **$\text{O}_2$ Diatomic Offset:** Overbinding in triplet $\text{O}_2$ introduces a systematic enthalpy shift across the combustion stoichiometry.
- **Remaining Enthalpy Difference:** Arises from minor PM7 underbinding in $\text{CO}_2$ and $\text{CH}_4$.

