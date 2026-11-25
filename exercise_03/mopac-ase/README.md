# Diels–Alder Reaction Enthalpy Calculation with MOPAC

The standalone `diels-alder-mopac.py` run completed cleanly without any diatomic artifacts, predicting $\Delta_r H^\circ(298.15\text{ K}) = -185.70\text{ kJ/mol}$ (vs. $-166.70\text{ kJ/mol}$ NIST experimental reference).

## Physical Breakdown of the MOPAC PM7 Diels–Alder Results

- **Individual Heats of Formation:**
  - **1,3-Butadiene:** $+113.67\text{ kJ/mol}$ vs. $+110.00\text{ kJ/mol}$ expt ($+3.67\text{ kJ/mol}$).
  - **Ethene:** $+57.97\text{ kJ/mol}$ vs. $+52.40\text{ kJ/mol}$ expt ($+5.57\text{ kJ/mol}$).
  - **Cyclohexene:** $-14.06\text{ kJ/mol}$ vs. $-4.30\text{ kJ/mol}$ expt ($-9.76\text{ kJ/mol}$).
- **Source of the $-19.0\text{ kJ/mol}$ Error:** All three individual $\Delta_f H^\circ$ values sit within $4\text{–}10\text{ kJ/mol}$ of NIST experiment, and the slight additive accumulation of errors across reactants ($+9.24\text{ kJ/mol}$) and product ($-9.76\text{ kJ/mol}$) yields the $-185.70\text{ kJ/mol}$ reaction enthalpy alongside near-exact $\text{C=C}$ bond lengths ($1.330\text{–}1.336\text{ \AA}$).

