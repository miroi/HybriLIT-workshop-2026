# Standalone NWChem Calculation

## Objective

This directory demonstrates how to perform an electronic-structure calculation directly with **NWChem**, independently of the ASE interface.

The example considers an isolated water molecule and uses density functional theory (DFT) to calculate its molecular properties.

The calculation also provides a reference for comparison with the ASE-based NWChem test in the parent directory.

## Computational setup

The input file

```text
h2o.dft_singlepoint.nw
```

defines the molecular geometry and computational parameters.

The calculation uses:

- **Molecular system:** H₂O.
- **Electronic state:** Singlet.
- **Exchange-correlation functional:** B3LYP.
- **Basis set:** 6-31G*.
- **Calculation type:** DFT energy and gradient calculation.

The DFT gradient calculation provides the information needed to evaluate the molecular energy and atomic forces.

## Execution

From this directory, execute:

```bash
mpirun -np 4 nwchem h2o.dft_singlepoint.nw > h2o.dft_singlepoint.nw_logfile
```

The command launches NWChem using four MPI processes and redirects the program output to a logfile.

**Important:** The input file contains machine-specific scratch and permanent directory settings. Before running the calculation on another computer, update these paths to directories that exist and are accessible on your system.

The number of MPI processes can also be adjusted according to the available computational resources.

## Reference output

A saved output file from a previous calculation is included in this directory.

It can be used to:

- Inspect the NWChem output format.
- Check the convergence of the calculation.
- Examine the calculated molecular energy and gradients.
- Compare the standalone calculation with the ASE-based implementation.

This example illustrates the basic structure of a standalone NWChem calculation and provides an introduction to preparing input files for more advanced quantum-chemical simulations.

