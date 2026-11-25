# Exercise 01 — Verification of the Computational Environment

## Objective

Before performing molecular simulations, it is important to verify that the computational environment is correctly configured and that all required software packages are accessible.

In this exercise, the installation and functionality of three computational chemistry tools are tested:

- MACE — machine-learning interatomic potentials.
- MOPAC — semi-empirical quantum-chemical calculations.
- NWChem — electronic-structure calculations based on density functional theory (DFT).

The calculations are performed through the Atomic Simulation Environment (ASE), which provides a common Python interface for the different computational methods.

## Tasks

Repeat the installation checks demonstrated in the workshop recording.

### 1. MACE–ASE

Verify that the MACE models can be imported and initialized through ASE. Perform a test calculation on a water molecule and check that the potential energy and atomic forces are returned successfully.

### 2. MOPAC–ASE

Verify that the MOPAC executable is accessible and that ASE can communicate with it.

Perform a PM7 calculation for an isolated water molecule and inspect the resulting heat of formation and analytical gradients.

### 3. NWChem–ASE

Verify that the NWChem executable is accessible and that ASE can launch an electronic-structure calculation.

Perform a DFT calculation for an isolated water molecule and check the calculated energy and atomic forces.

## Execution

Activate the workshop conda environment before running the checks.

Conda management system:

```bash
conda activate molmatmodel
conda install -c conda-forge ase mopac nwchem pyscf
pip install torch mace-torch
