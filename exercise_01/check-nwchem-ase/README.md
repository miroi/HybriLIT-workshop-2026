
# Verification of the NWChem–ASE Interface

## Objective

This directory contains a test calculation designed to verify the installation of **NWChem** and its integration with the **Atomic Simulation Environment (ASE)**.

NWChem is an electronic-structure software package that supports a wide range of quantum-chemical methods, including density functional theory (DFT).

In this exercise, a DFT calculation is performed for an isolated water molecule.

## Computational procedure

The Python script

```text
check_nwchem.py
```

performs the following operations:

1. Checks whether the NWChem executable is accessible.
2. Constructs an isolated H₂O molecule using ASE.
3. Initializes the ASE NWChem calculator.
4. Performs a B3LYP/6-31G* calculation.
5. Requests the molecular energy and atomic forces.
6. Checks whether the calculation has completed successfully.

The calculation uses the singlet electronic state of water.

The NWChem calculation is launched using MPI parallelization.

## Execution

Run the test using:

```bash
python check_nwchem.py
```

The script uses two MPI processes for the calculation.

## Standalone NWChem calculation

The subdirectory

```text
pure_nwchem_calculations/
```

contains a standalone NWChem input file and a saved calculation output.

This example demonstrates how to run NWChem directly, without using the ASE calculator interface.

See the README in that directory for further instructions.

## Expected outcome

A successful calculation confirms that:

- NWChem is correctly installed and accessible.
- ASE can communicate with the NWChem executable.
- The B3LYP calculation completes successfully.
- Molecular energies and atomic forces are returned.

This test provides a basic verification of the NWChem installation before proceeding to the more demanding calculations in subsequent exercises.


