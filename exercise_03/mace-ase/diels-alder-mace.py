import shutil
import torch
from pathlib import Path
from ase import Atoms
from ase.build import molecule
from ase.collections import g2
from ase.optimize import BFGS
from ase.vibrations import Vibrations
from ase.thermochemistry import IdealGasThermo
from ase.units import kJ, mol
from mace.calculators import mace_off

device = "cuda" if torch.cuda.is_available() else "cpu"
model_variant = "medium"

print("=== MACE-OFF23 Potential Initialization ===")
print(f"Model Variant      : MACE-OFF23 ({model_variant})")
print(f"Compute Device     : {device} (PyTorch {torch.__version__})")
print("Reference Level    : wB97M-D3(BJ)/def2-TZVPPD")
print("Reaction           : C4H6(g, 1,3-butadiene) + C2H4(g) -> C6H10(g, cyclohexene)")

calc = mace_off(model=model_variant, device=device, default_dtype="float64")

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

def relax_and_analyze(label, display_name, symmetrynumber, fmax=0.001):
    atoms = build_species(label)
    atoms.center(vacuum=12.0)
    atoms.calc = calc

    # 1. Geometry optimization
    opt = BFGS(atoms, logfile=None)
    opt.run(fmax=fmax)
    e_opt = atoms.get_potential_energy()

    # 2. Harmonic vibrational frequencies & ZPE
    vib_dir = Path(f"vib_mace_{label}")
    if vib_dir.exists():
        shutil.rmtree(vib_dir)

    vib = Vibrations(atoms, name=str(vib_dir), delta=0.01)
    vib.run()
    vib_energies = vib.get_energies()
    zpe_ev = vib.get_zero_point_energy()
    vib.clean()
    if vib_dir.exists():
        shutil.rmtree(vib_dir)

    # All three species are nonlinear (6 translational/rotational modes)
    internal_energies = vib_energies[6:]
    thermo = IdealGasThermo(
        vib_energies=internal_energies,
        potentialenergy=e_opt,
        atoms=atoms,
        geometry="nonlinear",
        symmetrynumber=symmetrynumber,
        spin=0,
    )
    h_298 = thermo.get_enthalpy(temperature=298.15, verbose=False)

    print(
        f"[{label:<5} ({display_name:<14})] steps={opt.nsteps:<3} | "
        f"E_opt={e_opt:12.6f} eV | ZPE={zpe_ev:.4f} eV"
    )
    return atoms, e_opt, zpe_ev, h_298

print("\n=== Tight Geometry Optimization & Harmonic Vibrations (delta = 0.01 A) ===")
species_list = [
    ("C4H6",  "1,3-butadiene", 2),
    ("C2H4",  "ethene",        4),
    ("C6H10", "cyclohexene",   2),
]

results = {}
for label, disp, sym in species_list:
    atoms, e_opt, zpe_ev, h_298 = relax_and_analyze(label, disp, sym, fmax=0.001)
    results[label] = {
        "atoms": atoms,
        "e_opt": e_opt,
        "zpe_ev": zpe_ev,
        "h_298": h_298,
    }

# Key double-bond lengths check
d_cc_diene = results["C4H6"]["atoms"].get_distance(0, 1)
d_cc_ene   = results["C2H4"]["atoms"].get_distance(0, 1)
d_cc_cyhex = results["C6H10"]["atoms"].get_distance(0, 1)

print("\n=== Relaxed C=C Double Bond Lengths ===")
print(f"C=C in 1,3-butadiene : {d_cc_diene:.4f} A  (Expt: 1.341 A)")
print(f"C=C in ethene        : {d_cc_ene:.4f} A  (Expt: 1.339 A)")
print(f"C=C in cyclohexene   : {d_cc_cyhex:.4f} A  (Expt: 1.335 A)")

# Reaction energetics: C4H6(g) + C2H4(g) -> C6H10(g)
dE_elec = results["C6H10"]["e_opt"] - (results["C4H6"]["e_opt"] + results["C2H4"]["e_opt"])
dZPE    = results["C6H10"]["zpe_ev"] - (results["C4H6"]["zpe_ev"] + results["C2H4"]["zpe_ev"])
dE_0K   = dE_elec + dZPE
dH_298  = results["C6H10"]["h_298"] - (results["C4H6"]["h_298"] + results["C2H4"]["h_298"])

print("\n=== Diels-Alder Reaction Enthalpy Summary (MACE-OFF23): C4H6 + C2H4 -> C6H10 ===")
print(f"Electronic dE_rxn  : {dE_elec:8.4f} eV  ({dE_elec / (kJ / mol):8.2f} kJ/mol)")
print(f"Zero-Point dZPE    : {dZPE:+8.4f} eV  ({dZPE / (kJ / mol):+8.2f} kJ/mol)")
print(f"ZPE-Corr dE_0K     : {dE_0K:8.4f} eV  ({dE_0K / (kJ / mol):8.2f} kJ/mol)")
print(f"Reaction drH_298K  : {dH_298:8.4f} eV  ({dH_298 / (kJ / mol):8.2f} kJ/mol)  [Expt ref: -166.70 kJ/mol]")

