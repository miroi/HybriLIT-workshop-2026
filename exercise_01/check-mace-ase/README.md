# Verification of the MACE–ASE Installation

## Objective

This directory contains a test calculation designed to verify the installation of **MACE** and its integration with the **Atomic Simulation Environment (ASE)**.

MACE is a machine-learning interatomic-potential framework that provides efficient predictions of molecular and materials properties using models trained on quantum-mechanical reference data.

The purpose of this test is to confirm that the required models can be initialized and used to calculate molecular energies and atomic forces.

## Computational procedure

The Python script

```text
check_mace_01.py
```

performs a test calculation on an isolated water molecule (H₂O).

The test includes:

1. Checking the availability of CUDA and selecting the appropriate computational device.
2. Inspecting the locally available MACE model files.
3. Loading the MACE-OFF23 and MACE-MP-0 models.
4. Creating an ASE molecular structure.
5. Initializing the corresponding ASE calculators.
6. Evaluating the potential energy and atomic forces.

The calculations provide a basic check that the models and ASE interface are functioning correctly.

## Execution

Run the test using:

```bash
python check_mace_01.py
```

The script may require access to the model checkpoints if they are not already available locally.

## Expected outcome

A successful execution should demonstrate that:

- The MACE package can be imported.
- The selected model checkpoints can be loaded.
- ASE can initialize the corresponding calculators.
- Molecular energies and atomic forces can be evaluated.

The output includes the calculated energy and maximum absolute force component.

This calculation is intended as an installation and functionality test rather than a quantitative benchmark of MACE model accuracy.


