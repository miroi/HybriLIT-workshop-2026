import shutil
import torch
from pathlib import Path
from ase.build import molecule
from ase.optimize import BFGS
from ase.vibrations import Vibrations
from ase.thermochemistry import IdealGasThermo
from ase.units import kJ, mol, invcm
from mace.calculators import mace_mp

# 1. Select device and initialize MACE universal foundation model (e.g., "medium" or "medium-mpa-0")
device = "cuda" if torch.cuda.is_available() else "cpu"
model_variant = "medium"

print("=== MACE Potential Initialization ===")
print(f"Model Variant      : MACE-MP-0 ({model_variant}) + D3 dispersion")
print(f"Compute Device     : {device} (PyTorch {torch.__version__})")
print("Reaction           : CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(g)")
print("Spin Treatment     : Spin-polarized PBE reference (S=1 for triplet O2 in IdealGasThermo)")

calc = mace_mp(
    model=model_variant,
    dispersion=True,
    default_dtype="float64",
    device=device,
)

# 2. Helper function to relax tightly before Hessian evaluation
def relax_molecule(name, fmax=0.0005):
    atoms = molecule(name)
    atoms.center(vacuum=12.0)
    atoms.calc = calc
    opt = BFGS(atoms, logfile=None)
    opt.run(fmax=fmax)
    return atoms, atoms.get_potential_energy(), opt.nsteps

# 3. Helper function to compute harmonic vibrations, ZPE, and 298.15 K enthalpy
def analyze_vibrations(name, atoms, e_pot, geometry, symmetrynumber, spin=0):
    vib_dir = Path(f"vib_mace_{name}")
    if vib_dir.exists():
        shutil.rmtree(vib_dir)

    vib = Vibrations(atoms, name=str(vib_dir), delta=0.01)
    vib.run()
    vib_energies = vib.get_energies()
    zpe = vib.get_zero_point_energy()
    vib.clean()
    if vib_dir.exists():
        shutil.rmtree(vib_dir)

    # Filter out 5 (linear) or 6 (nonlinear) translational/rotational modes
    n_tr = 5 if geometry == "linear" else 6
    internal_energies = vib_energies[n_tr:]
    internal_cm1 = [e.real / invcm for e in internal_energies]

    thermo = IdealGasThermo(
        vib_energies=internal_energies,
        potentialenergy=e_pot,
        atoms=atoms,
        geometry=geometry,
        symmetrynumber=symmetrynumber,
        spin=spin,
    )
    h_298 = thermo.get_enthalpy(temperature=298.15, verbose=False)
    return internal_cm1, zpe, h_298

# 4. Species specification: (geometry, symmetrynumber, total_spin_S)
specs = {
    "CH4": ("nonlinear", 12, 0),
    "O2":  ("linear",     2, 1),
    "CO2": ("linear",     2, 0),
    "H2O": ("nonlinear",  2, 0),
}

print("\n=== Tight Geometry Optimization & Harmonic Vibrations (delta = 0.01 A) ===")
results = {}
for name, (geom, sym, spin) in specs.items():
    atoms, e_opt, steps = relax_molecule(name, fmax=0.0005)
    freqs_cm1, zpe, h_298 = analyze_vibrations(name, atoms, e_opt, geom, sym, spin=spin)
    results[name] = {
        "atoms": atoms,
        "e_opt": e_opt,
        "zpe": zpe,
        "h_298": h_298,
        "freqs": freqs_cm1,
    }
    state_label = "triplet" if spin == 1 else "singlet"
    print(f"\n[{name:<3} ({state_label})] steps={steps:<2} | E_opt={e_opt:11.6f} eV | ZPE={zpe:.4f} eV")
    print("  Internal frequencies (cm^-1):", ", ".join(f"{f:.1f}" for f in freqs_cm1))

# 5. Key relaxed bond lengths
d_ch = results["CH4"]["atoms"].get_distance(0, 1)
d_oo = results["O2"]["atoms"].get_distance(0, 1)
d_co = results["CO2"]["atoms"].get_distance(0, 1)
d_oh = results["H2O"]["atoms"].get_distance(0, 1)

print("\n=== Relaxed Bond Lengths vs. Experiment ===")
print(f"C-H in CH4         : {d_ch:.4f} A  (Expt: 1.087 A)")
print(f"O=O in O2 (triplet): {d_oo:.4f} A  (Expt: 1.208 A)")
print(f"C=O in CO2         : {d_co:.4f} A  (Expt: 1.160 A)")
print(f"O-H in H2O         : {d_oh:.4f} A  (Expt: 0.958 A)")

# 6. Reaction energetics: CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(g)
dE_elec = (results["CO2"]["e_opt"] + 2.0 * results["H2O"]["e_opt"]) - (
    results["CH4"]["e_opt"] + 2.0 * results["O2"]["e_opt"]
)
dZPE = (results["CO2"]["zpe"] + 2.0 * results["H2O"]["zpe"]) - (
    results["CH4"]["zpe"] + 2.0 * results["O2"]["zpe"]
)
dE_0K = dE_elec + dZPE
dH_298 = (results["CO2"]["h_298"] + 2.0 * results["H2O"]["h_298"]) - (
    results["CH4"]["h_298"] + 2.0 * results["O2"]["h_298"]
)

print("\n=== Gas-Phase Methane Combustion Summary (MACE-MP-0): CH4 + 2 O2 -> CO2 + 2 H2O ===")
print(f"Electronic dE_rxn  : {dE_elec:8.4f} eV  ({dE_elec / (kJ / mol):8.2f} kJ/mol)")
print(f"Zero-Point dZPE    : {dZPE:+8.4f} eV  ({dZPE / (kJ / mol):+8.2f} kJ/mol)")
print(f"ZPE-Corr dE_0K     : {dE_0K:8.4f} eV  ({dE_0K / (kJ / mol):8.2f} kJ/mol)")
print(f"Enthalpy dcH_298K  : {dH_298:8.4f} eV  ({dH_298 / (kJ / mol):8.2f} kJ/mol)  [Expt ref: -802.30 kJ/mol]")

