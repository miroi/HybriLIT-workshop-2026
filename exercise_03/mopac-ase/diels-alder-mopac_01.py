from pathlib import Path
from ase import Atoms
from ase.build import molecule
from ase.collections import g2
from ase.optimize import BFGS
from ase.units import kJ, mol
from ase.calculators.mopac import MOPAC
from ase.io import read, write

method = "PM7"

# Output directory for optimization trajectories and final geometries
out_dir = Path("geometries")
out_dir.mkdir(exist_ok=True)

print("=== MOPAC Calculator Initialization ===")
print(f"Method             : {method} (Semi-Empirical NDDO Hamiltonian)")
print("Reaction           : C4H6(g, 1,3-butadiene) + C2H4(g) -> C6H10(g, cyclohexene)")
print("Energy Definition  : FINAL HEAT OF FORMATION dHf(298.15 K)")


def make_mopac_calc(label):
    return MOPAC(
        label=label,
        method=method,
        task="1SCF GRADIENTS PRECISE",
        command="mopac PREFIX.mop > /dev/null 2>&1",
    )


def build_species(name):
    if name == "C4H6":
        return molecule("butadiene")
    elif name == "C2H4":
        return molecule("C2H4")
    elif name == "C6H10":
        if "cyclohexene" in g2.names:
            return molecule("cyclohexene")
        # Half-chair cyclohexene (C6H10) starting coordinates (in Angstroms)
        symbols = ["C"] * 6 + ["H"] * 10
        positions = [
            [ 0.000,  0.668,  1.258],
            [ 0.000, -0.668,  1.258],
            [-0.145, -1.495, -0.002],
            [ 0.258, -0.748, -1.275],
            [-0.258,  0.748, -1.275],
            [ 0.145,  1.495, -0.002],
            [ 0.032,  1.225,  2.193],
            [ 0.032, -1.225,  2.193],
            [ 0.453, -2.411,  0.088],
            [-1.193, -1.825, -0.082],
            [ 1.351, -0.822, -1.352],
            [-0.145, -1.262, -2.155],
            [-1.351,  0.822, -1.352],
            [ 0.145,  1.262, -2.155],
            [ 1.193,  1.825, -0.082],
            [-0.453,  2.411,  0.088],
        ]
        return Atoms(symbols=symbols, positions=positions)
    raise ValueError(f"Unknown species: {name}")


def relax_and_get_dhf(label, display_name, fmax=0.001):
    atoms = build_species(label)
    atoms.pbc = False

    # Geometry optimization; MOPAC's FINAL HEAT OF FORMATION (298.15 K) is
    # already the formation enthalpy, so no vibrational analysis is needed.
    calc = make_mopac_calc(f"mopac_opt_{label}")
    atoms.calc = calc
    traj_file = out_dir / f"{label}_opt.traj"
    opt = BFGS(atoms, logfile=None, trajectory=str(traj_file))
    opt.run(fmax=fmax)
    dhf_ev = calc.get_final_heat_of_formation()

    # Optimization trajectory (all BFGS steps, incl. the starting geometry) as multi-frame extxyz
    frames = read(str(traj_file), index=":")
    write(out_dir / f"{label}_opt_traj.xyz", frames, format="extxyz")

    # Final converged geometry as plain xyz (comment line holds the PM7 heat of formation)
    write(
        out_dir / f"{label}_final.xyz",
        atoms,
        format="xyz",
        comment=f"{display_name} PM7 dHf(298.15 K) = {dhf_ev / (kJ / mol):.2f} kJ/mol",
    )

    print(
        f"[{label:<5} ({display_name:<14})] steps={opt.nsteps:<3} | "
        f"dHf_298K={dhf_ev / (kJ / mol):+8.2f} kJ/mol"
    )
    return atoms, dhf_ev


print("\n=== Tight Geometry Optimization & MOPAC Heat of Formation ===")
species_list = [
    ("C4H6",  "1,3-butadiene"),
    ("C2H4",  "ethene"),
    ("C6H10", "cyclohexene"),
]

results = {}
for label, disp in species_list:
    atoms, dhf_ev = relax_and_get_dhf(label, disp, fmax=0.001)
    results[label] = {"atoms": atoms, "dhf_ev": dhf_ev}

# Key double-bond lengths check
d_cc_diene = results["C4H6"]["atoms"].get_distance(0, 1)
d_cc_ene   = results["C2H4"]["atoms"].get_distance(0, 1)
d_cc_cyhex = results["C6H10"]["atoms"].get_distance(0, 1)

print("\n=== Relaxed C=C Double Bond Lengths ===")
print(f"C=C in 1,3-butadiene : {d_cc_diene:.4f} A  (Expt: 1.341 A)")
print(f"C=C in ethene        : {d_cc_ene:.4f} A  (Expt: 1.339 A)")
print(f"C=C in cyclohexene   : {d_cc_cyhex:.4f} A  (Expt: 1.335 A)")

# Reaction enthalpy at 298.15 K
dh_c4h6  = results["C4H6"]["dhf_ev"] / (kJ / mol)
dh_c2h4  = results["C2H4"]["dhf_ev"] / (kJ / mol)
dh_c6h10 = results["C6H10"]["dhf_ev"] / (kJ / mol)

dr_H_298 = dh_c6h10 - (dh_c4h6 + dh_c2h4)

print("\n=== Diels-Alder Reaction Enthalpy Summary (PM7): C4H6 + C2H4 -> C6H10 ===")
print(f"dHf(1,3-butadiene) : {dh_c4h6:+8.2f} kJ/mol  (Expt ref: +110.00 kJ/mol)")
print(f"dHf(ethene)        : {dh_c2h4:+8.2f} kJ/mol  (Expt ref:  +52.40 kJ/mol)")
print(f"dHf(cyclohexene)   : {dh_c6h10:+8.2f} kJ/mol  (Expt ref:   -4.30 kJ/mol)")
print(f"Reaction drH_298K  : {dr_H_298:+8.2f} kJ/mol  ({dr_H_298 * (kJ / mol):+.4f} eV)  [Expt ref: -166.70 kJ/mol]")

# Clean up temporary MOPAC files
for ext in ("*.mop", "*.out", "*.arc", "*.aux"):
    for f in Path(".").glob(ext):
        f.unlink()
