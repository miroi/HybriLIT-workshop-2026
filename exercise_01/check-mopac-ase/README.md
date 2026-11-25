
# Verification of the MOPAC–ASE Interface

## Objective

This directory contains a test calculation designed to verify the installation of **MOPAC** and its integration with the **Atomic Simulation Environment (ASE)**.

MOPAC is a semi-empirical quantum-chemistry program that provides computationally efficient methods for calculating molecular properties.

In this exercise, the PM7 method is used to perform a test calculation on an isolated water molecule.

## Computational procedure

The Python script

```text
check_mopac.py
```

performs the following operations:

1. Checks whether the MOPAC executable is available in the system environment.
2. Constructs an isolated H₂O molecule using ASE.
3. Initializes the ASE MOPAC calculator.
4. Performs a PM7 self-consistent-field calculation.
5. Requests analytical gradients.
6. Retrieves the calculated heat of formation and atomic forces.

The calculation verifies the communication between ASE and the external MOPAC executable.

## Execution

Run the test using:

```bash
python check_mopac.py
```

## Reference calculation

The accompanying standalone MOPAC test is located in:

```text
pure_mopac_test/
```

It contains an input file for an H₂O calculation and a saved MOPAC output file.

The ASE-based and standalone calculations can be compared to verify the consistency of the computational setup.

## Expected outcome

A successful calculation should confirm that:

- The MOPAC executable is accessible.
- ASE can generate and submit the molecular calculation.
- The PM7 calculation completes successfully.
- Molecular energetics and analytical gradients are returned.

The saved output files can also be used for troubleshooting and for examining the details of the MOPAC calculation.

