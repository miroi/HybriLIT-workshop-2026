import os
import numpy as np
import torch
from ase.build import molecule
from mace.calculators import mace_off, mace_mp

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"=== MACE Smoke Test (device={device}) ===")

# Directory where MACE stores cached checkpoints
CACHE_DIR = os.path.expanduser("~/.cache/mace")


def list_cache_models(cache_dir=CACHE_DIR):
    """Print all .model files found in the MACE cache directory."""
    print(f"--- Models found in {cache_dir} ---")
    if not os.path.isdir(cache_dir):
        print("  (cache directory does not exist)")
        return
    files = sorted(
        f for f in os.listdir(cache_dir)
        if f.endswith(".model") or "model" in f.lower()
    )
    if not files:
        print("  (no model files found)")
    for f in files:
        full = os.path.join(cache_dir, f)
        size_mb = os.path.getsize(full) / 1e6
        print(f"  {f:<45} {size_mb:8.2f} MB")


def find_cached_model(keywords, cache_dir=CACHE_DIR):
    """Return the path of a cached model file whose name contains all keywords."""
    if not os.path.isdir(cache_dir):
        return None
    for f in sorted(os.listdir(cache_dir)):
        full = os.path.join(cache_dir, f)
        if not os.path.isfile(full):
            continue
        lname = f.lower()
        if all(k.lower() in lname for k in keywords):
            return full
    return None


list_cache_models()

# Model configurations to test
models_to_test = [
    ("MACE-OFF23 (medium)", "off", "medium", {"dispersion": False},
     ["off23", "medium"]),
    ("MACE-MP-0 (med+D3)",  "mp",  "medium", {"dispersion": True},
     ["mp", "medium"]),
]

for label, model_type, model_size, extra_kwargs, cache_keywords in models_to_test:
    # Locate the cached checkpoint corresponding to this model
    cached_path = find_cached_model(cache_keywords)
    if cached_path:
        print(f"[{label:<19}] Cached model: {cached_path}")
    else:
        print(f"[{label:<19}] Cached model: not found (will be downloaded on first use)")

    # Get the raw model object (for saving)
    if model_type == "off":
        raw_model = mace_off(
            model=model_size,
            device=device,
            default_dtype="float64",
            return_raw_model=True,
            **extra_kwargs,
        )
    else:
        raw_model = mace_mp(
            model=model_size,
            device=device,
            default_dtype="float64",
            return_raw_model=True,
            **extra_kwargs,
        )

    # Save the model file to the current directory
    save_name = (
        label.replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("+", "plus")
        + ".model"
    )
    torch.save(raw_model, save_name)
    print(f"[{label:<19}] Model saved to: {save_name}")

    # Build a calculator and run the smoke test
    if model_type == "off":
        calc = mace_off(model=model_size, device=device, default_dtype="float64", **extra_kwargs)
    else:
        calc = mace_mp(model=model_size, device=device, default_dtype="float64", **extra_kwargs)

    atoms = molecule("H2O")
    atoms.center(vacuum=10.0)
    atoms.calc = calc
    energy = atoms.get_potential_energy()
    forces = atoms.get_forces()
    print(
        f"[{label:<19}] PASS | E = {energy:11.6f} eV | "
        f"max|F| = {np.abs(forces).max():.6f} eV/A"
    )
