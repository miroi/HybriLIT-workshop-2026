import shutil
from pathlib import Path
from ase.build import molecule
from ase.optimize import BFGS
from ase.vibrations import Vibrations
from ase.thermochemistry import IdealGasThermo
from ase.units import kJ, mol, invcm
from ase.calculators.nwchem import NWChem

# 1. Configure DFT functional, basis set, and MPI parallelization
xc_func = "b3lyp"           # Try "b3lyp", "pbe0", or "pbe"
basis_set = "6-311++G**"    # Triple-zeta polarized + diffuse functions for accurate thermochemistry
nprocs = 6                  # Default number of MPI ranks
nwchem_cmd = f"mpirun -np {nprocs} nwchem PREFIX.nwi > PREFIX.nwo"

print("=== NWChem DFT Calculator Initialization ===")
print(f"Functional / Basis : {xc_func.upper()} / {basis_set}")
print(f"MPI Launch Command : {nwchem_cmd}")
print("Reaction           : CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(g)")
print("Spin Treatment     : Restricted singlet (mult=1) except open-shell triplet O2 (odft, mult=3)")

def make_nwchem_calc(label, is_triplet=False):
    dft_block = {
        "xc": xc_func,
        "mult": 3 if is_triplet else 1,
        "grid": "fine",
        "convergence": {
            "energy": 1e-8,
            "density": 1e-6,
            "gradient": 5e-6,
        },
    }
    if is_triplet:
        # Enable unrestricted open-shell DFT (ODFT) for triplet O2
        dft_block["odft"] = None

    return NWChem(
        label=label,
        theory="dft",
        basis=basis_set,
        dft=dft_block,
        command=nwchem_cmd,
    )

# 2. Helper function to relax geometry with ASE BFGS
def relax_molecule(name, is_triplet=False, fmax=0.001):
    atoms = molecule(name)
    atoms.pbc = False
    atoms.calc = make_nwchem_calc(f"nwchem_opt_{name}", is_triplet=is_triplet)
    opt = BFGS(atoms, logfile=None)
    opt.run(fmax=fmax)
    return atoms, atoms.get_potential_energy(), opt.nsteps

# 3. Helper function to compute harmonic vibrations, ZPE, and 298.15 K enthalpy
def analyze_vibrations(name, atoms, e_pot, geometry, symmetrynumber, is_triplet=False):
    vib_dir = Path(f"vib_nwchem_{name}")
    if vib_dir.exists():
        shutil.rmtree(vib_dir)

    atoms.calc = make_nwchem_calc(f"nwchem_vib_{name}", is_triplet=is_triplet)
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

    # spin = total electronic spin S (S = 1 for triplet O2, giving multiplicity 2S+1 = 3)
    thermo = IdealGasThermo(
        vib_energies=internal_energies,
        potentialenergy=e_pot,
        atoms=atoms,
        geometry=geometry,
        symmetrynumber=symmetrynumber,
        spin=1 if is_triplet else 0,
    )
    h_298 = thermo.get_enthalpy(temperature=298.15, verbose=False)
    return internal_cm1, zpe, h_298

# 4. Species specification: (geometry, symmetrynumber, is_triplet)
specs = {
    "CH4": ("nonlinear", 12, False),
    "O2":  ("linear",     2, True),
    "CO2": ("linear",     2, False),
    "H2O": ("nonlinear",  2, False),
}

print("\n=== ASE Geometry Optimization & Harmonic Vibrations (delta = 0.01 A) ===")
results = {}
for name, (geom, sym, is_triplet) in specs.items():
    atoms, e_opt, steps = relax_molecule(name, is_triplet=is_triplet, fmax=0.001)
    freqs_cm1, zpe, h_298 = analyze_vibrations(name, atoms, e_opt, geom, sym, is_triplet=is_triplet)
    results[name] = {
        "atoms": atoms,
        "e_opt": e_opt,
        "zpe": zpe,
        "h_298": h_298,
        "freqs": freqs_cm1,
    }
    state_label = "triplet" if is_triplet else "singlet"
    print(f"\n[{name:<3} ({state_label})] steps={steps:<2} | E_opt={e_opt:12.6f} eV | ZPE={zpe:.4f} eV")
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

print(f"\n=== Gas-Phase Methane Combustion Summary (NWChem {xc_func.upper()}/{basis_set}) ===")
print(f"Electronic dE_rxn  : {dE_elec:8.4f} eV  ({dE_elec / (kJ / mol):8.2f} kJ/mol)")
print(f"Zero-Point dZPE    : {dZPE:+8.4f} eV  ({dZPE / (kJ / mol):+8.2f} kJ/mol)")
print(f"ZPE-Corr dE_0K     : {dE_0K:8.4f} eV  ({dE_0K / (kJ / mol):8.2f} kJ/mol)")
print(f"Enthalpy dcH_298K  : {dH_298:8.4f} eV  ({dH_298 / (kJ / mol):8.2f} kJ/mol)  [Expt ref: -802.30 kJ/mol]")

# 7. Clean up NWChem runtime scratch files (.nwi, .nwo, .db, .movecs, etc.)
for pattern in ("nwchem_opt_*", "nwchem_vib_*"):
    for f in Path(".").glob(pattern):
        if f.is_file():
            f.unlink()

