import shutil
from pathlib import Path
import numpy as np
from ase.build import molecule
from ase.calculators.nwchem import NWChem

nprocs = 2
print(f"=== NWChem (B3LYP/6-31G*, np={nprocs}) Smoke Test ===")
assert shutil.which("nwchem"), "nwchem binary not found in PATH"

atoms = molecule("H2O")
atoms.pbc = False
atoms.calc = NWChem(
    label="check_nwchem_h2o",
    theory="dft",
    basis="6-31G*",
    dft={"xc": "b3lyp", "mult": 1},
    command=f"mpirun -np {nprocs} nwchem PREFIX.nwi > PREFIX.nwo",
)

try:
    energy = atoms.get_potential_energy()
    forces = atoms.get_forces()
    print(f"Status             : PASS")
    print(f"Total Energy (H2O) : {energy:.6f} eV")
    print(f"Max Force Component: {np.abs(forces).max():.6f} eV/A")
finally:
    print(f"Keeping NWChem working files")
#    for p in Path(".").glob("check_nwchem_h2o*"):
#        if p.is_file():
#            p.unlink()

