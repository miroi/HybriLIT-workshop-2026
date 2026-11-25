import shutil
import numpy as np
import scipy
import ase
import torch

print("=== Core Python, GPU & External Binaries Check ===")
print(f"ASE version        : {ase.__version__}")
print(f"NumPy version      : {np.__version__}")
print(f"SciPy version      : {scipy.__version__}")
print(f"PyTorch version    : {torch.__version__}")
print(f"CUDA available     : {torch.cuda.is_available()}", end="")
if torch.cuda.is_available():
    print(f" ({torch.cuda.get_device_name(0)})")
else:
    print(" (running on CPU)")

print("\nExternal Executables in PATH:")
for binary in ["mopac", "nwchem", "pw.x", "mpirun", "gap_fit", "quip"]:
    path = shutil.which(binary)
    print(f"  {binary:<10} : {'[OK] ' + path if path else '[MISSING]'}")

