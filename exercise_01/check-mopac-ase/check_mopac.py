import shutil
from pathlib import Path
import numpy as np
from ase.build import molecule
from ase.calculators.mopac import MOPAC

print("=== MOPAC (PM7) Smoke Test ===")
assert shutil.which("mopac"), "mopac binary not found in PATH"

atoms = molecule("H2O")
atoms.pbc = False
calc = MOPAC(
    label="check_mopac_h2o",
    method="PM7",
    task="1SCF GRADIENTS",
    command="mopac PREFIX.mop > /dev/null 2>&1",
)
atoms.calc = calc

try:
    # Trigger calculation first so calc.results['final_hof'] is populated
    _ = atoms.get_potential_energy()
    forces = atoms.get_forces()
    dhf_ev = calc.get_final_heat_of_formation()
    print("Status             : PASS")
    print(f"dHf(H2O, 298K)     : {dhf_ev:.6f} eV")
    print(f"Max Force Component: {np.abs(forces).max():.6f} eV/A")
finally:
    print ("keeping working files")
#    for p in Path(".").glob("check_mopac_h2o.*"):
#        p.unlink()

