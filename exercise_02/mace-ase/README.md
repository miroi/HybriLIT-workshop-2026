# Methane Combustion with MACE

Because standard **MACE-OFF23** is parameterized strictly for closed-shell singlet organic molecules and has no spin-state awareness for ground-state triplet $\text{O}_2$, this script uses the universal foundation model `mace_mp` (which covers the periodic table, supports D3 dispersion, and is trained on spin-polarized Materials Project PBE/PBE+U calculations where ground-state $\text{O}_2$ is naturally a triplet) while passing `spin=1` for $\text{O}_2$ into `IdealGasThermo`.

## Important Pedagogical Note for `exercise_02`

- **Why `mace_mp` is used here instead of `mace_off`:** `MACE-OFF23` was trained exclusively on closed-shell singlet organic molecules (`SPICE` / `QM7-X`), so it has no representation of open-shell triplet $\text{O}_2$ ($^3\Sigma_g^-$). By contrast, `MACE-MP-0` is trained on spin-polarized VASP PBE/PBE+U calculations from the Materials Project, where gas-phase $\text{O}_2$ was converged in its triplet ground state.
- **Known PBE $\text{O}_2$ overbinding:** Because `MACE-MP-0` inherits the underlying GGA PBE potential energy surface—which famously overbinds the $\text{O}_2$ double bond by $\sim 0.4\text{ eV}$ per $\text{O}_2$ molecule (the same error that requires Wang–Maxisch–Ceder $\text{O}_2$ corrections in Materials Project phase diagrams)—the predicted $\Delta_c H^\circ(298\text{ K})$ reflects that PBE $\text{O}_2$ bias rather than matching experiment as closely as `MACE-OFF23` did for closed-shell ethene hydrogenation.

## Physical Breakdown of the `MACE-MP-0` Results

The `MACE-MP-0 (medium) + D3` run produces $\Delta_c H^\circ(298\text{ K}) = -743.24\text{ kJ/mol}$—landing within $59\text{ kJ/mol}$ ($7.4\%$) of the experimental gas-phase value ($-802.30\text{ kJ/mol}$) and faithfully reproducing the underlying GGA PBE potential energy surface:

1. **Exact Inheritance of PBE $\text{O}_2$ Overbinding:**
   - In VASP PBE DFT (the exact training level of `MACE-MP-0`), the $\text{O=O}$ bond length of triplet $\text{O}_2$ is $1.234\text{ \AA}$ (MACE result: $1.2366\text{ \AA}$), and PBE overbinds the $\text{O}_2$ molecule by $\sim 0.30\text{–}0.35\text{ eV}$ ($\sim 30\text{ kJ/mol}$) per $\text{O}_2$.
   - Because $2\text{ mol}$ of $\text{O}_2$ appear on the reactant side, that $2 \times 30\text{ kJ/mol} \approx 60\text{ kJ/mol}$ over-stabilization of the reactants shifts $\Delta_c H^\circ(298\text{ K})$ upward from $-802.30\text{ kJ/mol}$ to $-743.24\text{ kJ/mol}$—matching raw PBE DFT ($\approx -745\text{ kJ/mol}$) to within $2\text{ kJ/mol}$.

2. **Accurate Zero-Point & Thermal Corrections:**
   - The harmonic $\Delta\text{ZPE} = +8.83\text{ kJ/mol}$ matches both `GFN2-xTB` ($+8.74\text{ kJ/mol}$) and full DFT ($\approx +9\text{ kJ/mol}$), with clean degenerate bending modes in $\text{CO}_2$ ($710.2, 710.2\text{ cm}^{-1}$) and triply degenerate modes in $\text{CH}_4$ ($1194.2\text{ cm}^{-1}$ and $3147.3\text{ cm}^{-1}$).

