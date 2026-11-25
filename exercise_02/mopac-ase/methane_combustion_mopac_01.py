import argparse
import shutil
from pathlib import Path

from ase.build import molecule
from ase.optimize import BFGS
from ase.vibrations import Vibrations
from ase.units import kJ, mol, invcm
from ase.calculators.mopac import MOPAC

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
METHOD = "PM7"

SPECS = {
    # name: (geometry, is_triplet)
    "CH4": ("nonlinear", False),
    "O2":  ("linear",    True),
    "CO2": ("linear",    False),
    "H2O": ("nonlinear", False),
}

# Experimental 298.15 K formation enthalpies (kJ/mol), for comparison only
EXPT_DHF = {
    "CH4": -74.87,
    "O2":    0.00,
    "CO2": -393.51,
    "H2O": -241.83,
}
EXPT_DC_H = -802.30  # kJ/mol, gas-phase CH4 + 2 O2 -> CO2 + 2 H2O


# ---------------------------------------------------------------------------
# MOPAC helpers
# ---------------------------------------------------------------------------
def make_mopac_calc(label: str, is_triplet: bool = False) -> MOPAC:
    """Return a MOPAC calculator; O2 ground state is a triplet."""
    spin_kw = " TRIPLET UHF" if is_triplet else ""
    return MOPAC(
        label=label,
        method=METHOD,
        task=f"1SCF GRADIENTS PRECISE{spin_kw}",
        command="mopac PREFIX.mop > /dev/null 2>&1",
    )


def relax_and_get_dhf(name: str, is_triplet: bool = False, fmax: float = 5e-4):
    """Optimize a molecule and return (atoms, dHf in eV, n_steps)."""
    atoms = molecule(name)
    atoms.pbc = False
    calc = make_mopac_calc(f"mopac_opt_{name}", is_triplet=is_triplet)
    atoms.calc = calc
    opt = BFGS(atoms, logfile=None)
    opt.run(fmax=fmax)
    dhf_ev = calc.get_final_heat_of_formation()  # eV
    return atoms, dhf_ev, opt.nsteps


def analyze_vibrations(name: str, atoms, geometry: str, is_triplet: bool = False):
    """Optional: harmonic frequencies and ZPE. Not needed for dHf-based dcH."""
    vib_dir = Path(f"vib_mopac_{name}")
    if vib_dir.exists():
        shutil.rmtree(vib_dir)

    atoms.calc = make_mopac_calc(f"mopac_vib_{name}", is_triplet=is_triplet)
    vib = Vibrations(atoms, name=str(vib_dir), delta=0.01)
    vib.run()
    vib_energies = vib.get_energies()
    zpe = vib.get_zero_point_energy()
    vib.clean()
    if vib_dir.exists():
        shutil.rmtree(vib_dir)

    n_tr = 5 if geometry == "linear" else 6
    internal_cm1 = [e.real / invcm for e in vib_energies[n_tr:]]
    return internal_cm1, zpe


# ---------------------------------------------------------------------------
# Core: combustion enthalpy from dHf(298.15 K) only
# ---------------------------------------------------------------------------
def combustion_enthalpy_from_dhf(dhf_ev: dict) -> dict:
    """
    Compute the gas-phase combustion enthalpy of methane at 298.15 K purely
    from MOPAC's FINAL HEAT OF FORMATION values.

    Reaction: CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(g)

    MOPAC's dHf is a true 298.15 K formation enthalpy in the sense that the
    semi-empirical parameterization was fitted to reproduce formation enthalpies
    directly. Therefore no ZPE and no thermal correction are added here: doing
    so would double-count.

    Returns a dict with:
      - dc_h_raw_kj    : using PM7's own dHf(O2) (non-zero)
      - dc_h_ref_kj    : with dHf(O2) forced to 0 (elemental reference)
      - dc_h_raw_ev    : same as dc_h_raw_kj but in eV
      - dc_h_ref_ev    : same as dc_h_ref_kj but in eV
    """
    to_kj = lambda e: e / (kJ / mol)

    d_ch4 = to_kj(dhf_ev["CH4"])
    d_o2  = to_kj(dhf_ev["O2"])
    d_co2 = to_kj(dhf_ev["CO2"])
    d_h2o = to_kj(dhf_ev["H2O"])

    dc_raw = (d_co2 + 2.0 * d_h2o) - (d_ch4 + 2.0 * d_o2)
    dc_ref = (d_co2 + 2.0 * d_h2o) - (d_ch4 + 2.0 * 0.0)

    return {
        "dhf_kj": {"CH4": d_ch4, "O2": d_o2, "CO2": d_co2, "H2O": d_h2o},
        "dc_h_raw_kj": dc_raw,
        "dc_h_ref_kj": dc_ref,
        "dc_h_raw_ev": dc_raw * (kJ / mol),
        "dc_h_ref_ev": dc_ref * (kJ / mol),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(with_vibrations: bool = False) -> None:
    print("=== MOPAC Calculator Initialization ===")
    print(f"Method             : {METHOD} (Semi-Empirical NDDO Hamiltonian)")
    print("Reaction           : CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(g)")
    print("Energy Definition  : FINAL HEAT OF FORMATION dHf(298.15 K)")
    print("Note               : dHf from MOPAC is already a 298.15 K enthalpy;")
    print("                     no ZPE / thermal corrections are added for dcH.")
    if with_vibrations:
        print("Vibrations         : ENABLED (informational only, not used for dcH)")

    print("\n=== Tight Geometry Optimization ===")
    dhf_ev = {}
    results = {}
    for name, (geom, is_triplet) in SPECS.items():
        atoms, dhf, steps = relax_and_get_dhf(name, is_triplet=is_triplet, fmax=5e-4)
        dhf_ev[name] = dhf
        results[name] = {"atoms": atoms, "dhf_ev": dhf}
        state = "triplet" if is_triplet else "singlet"
        print(f"[{name:<3} ({state:<7})] steps={steps:<2} | "
              f"dHf_298K={dhf / (kJ / mol):+8.2f} kJ/mol")

    # --- Core calculation: pure dHf-based combustion enthalpy ---
    comb = combustion_enthalpy_from_dhf(dhf_ev)
    d = comb["dhf_kj"]

    print("\n=== Gas-Phase Methane Combustion: dHf(298.15 K) ONLY ===")
    print(f"{'Species':<6}{'PM7 dHf (kJ/mol)':>20}{'Expt dHf (kJ/mol)':>22}")
    for sp in ("CH4", "O2", "CO2", "H2O"):
        print(f"{sp:<6}{d[sp]:>20.2f}{EXPT_DHF[sp]:>22.2f}")

    print()
    print(f"dcH_298K (PM7 dHf, raw O2)     = {comb['dc_h_raw_kj']:+8.2f} kJ/mol"
          f"  ({comb['dc_h_raw_ev']:+.4f} eV)")
    print(f"dcH_298K (PM7 dHf, dHf(O2)=0)  = {comb['dc_h_ref_kj']:+8.2f} kJ/mol"
          f"  ({comb['dc_h_ref_ev']:+.4f} eV)")
    print(f"Experimental reference         = {EXPT_DC_H:+8.2f} kJ/mol")
    print(f"Error vs. expt (ref)           = "
          f"{comb['dc_h_ref_kj'] - EXPT_DC_H:+8.2f} kJ/mol")

    # --- Optional vibrations (do NOT feed into dcH) ---
    if with_vibrations:
        print("\n=== Harmonic Vibrations (informational only) ===")
        for name, (geom, is_triplet) in SPECS.items():
            atoms = results[name]["atoms"]
            freqs, zpe = analyze_vibrations(name, atoms, geom, is_triplet=is_triplet)
            results[name]["freqs"] = freqs
            results[name]["zpe"] = zpe
            print(f"[{name:<3}] ZPE = {zpe:.4f} eV | "
                  f"n_modes(internal) = {len(freqs)}")

        print("\nNOTE: ZPE values above are reported for completeness only.")
        print("      They are NOT added to dHf when forming dcH, because")
        print("      MOPAC's dHf is already a 298.15 K formation enthalpy.")

    # --- Relaxed bond lengths ---
    d_ch  = results["CH4"]["atoms"].get_distance(0, 1)
    d_oo  = results["O2"]["atoms"].get_distance(0, 1)
    d_co  = results["CO2"]["atoms"].get_distance(0, 1)
    d_oh  = results["H2O"]["atoms"].get_distance(0, 1)

    print("\n=== Relaxed Bond Lengths vs. Experiment ===")
    print(f"C-H in CH4         : {d_ch:.4f} A  (Expt: 1.087 A)")
    print(f"O=O in O2 (triplet): {d_oo:.4f} A  (Expt: 1.208 A)")
    print(f"C=O in CO2         : {d_co:.4f} A  (Expt: 1.160 A)")
    print(f"O-H in H2O         : {d_oh:.4f} A  (Expt: 0.958 A)")

    # --- Cleanup ---
    for ext in ("*.mop", "*.out", "*.arc"):
        for f in Path(".").glob(ext):
            f.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vib",
        action="store_true",
        help="Also run harmonic vibrations (ZPE); not used for dcH.",
    )
    args = parser.parse_args()
    main(with_vibrations=args.vib)
