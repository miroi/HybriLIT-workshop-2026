
# Exercise 01 — Verification of the Computational Environment

## Objective

Before performing molecular simulations, it is important to verify that the computational environment is correctly configured and that all required software packages are accessible.

In this exercise, the installation and functionality of three computational chemistry tools are tested:

- **MACE** — machine-learning interatomic potentials.
- **MOPAC** — semi-empirical quantum-chemical calculations.
- **NWChem** — electronic-structure calculations based on density functional theory (DFT).

The calculations are performed through the **Atomic Simulation Environment (ASE)**, which provides a common Python interface for the different computational methods.

## Tasks

First, activate the workshop conda environment before running the checks.

Conda management system:

```bash
conda create -n mace_env
conda activate mace_env
conda install -c conda-forge ase mopac nwchem pyscf
pip install torch mace-torch


### 1. MACE–ASE

Verify that the MACE models can be imported and initialized through ASE. Perform a test calculation on a water molecule and check that the potential energy and atomic forces are returned successfully.

See [`check-mace-ase/`](check-mace-ase/README.md).

### 2. MOPAC–ASE

Verify that the MOPAC executable is accessible and that ASE can communicate with it.

Perform a PM7 calculation for an isolated water molecule and inspect the resulting heat of formation and analytical gradients.

See [`check-mopac-ase/`](check-mopac-ase/README.md).

### 3. NWChem–ASE

Verify that the NWChem executable is accessible and that ASE can launch an electronic-structure calculation.

Perform a DFT calculation for an isolated water molecule and check the calculated energy and atomic forces.

See [`check-nwchem-ase/`](check-nwchem-ase/README.md).

## Execution

Activate the workshop conda environment before running the checks.

The general procedure is:

1. Check the Python environment.
2. Verify that the external computational executables are available.
3. Run the corresponding Python test scripts.
4. Inspect the calculation outputs and check for successful completion.

The main environment-check script is:

```bash
python check_env.py
```

The individual checks are performed from their respective directories:

```bash
python check_mace_01.py
python check_mopac.py
python check_nwchem.py
```

## Expected outcome

At the end of this exercise, the participant should have verified that:

- The Python environment is functional.
- MACE models can be loaded and used through ASE.
- MOPAC can perform semi-empirical calculations through ASE.
- NWChem can perform DFT calculations through ASE.
- Molecular energies and forces can be retrieved from the different calculators.

Successful completion of these tests provides the computational foundation for the subsequent exercises.

