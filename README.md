
# HybriLIT Workshop 2026 — Computational Molecular Physics (Computational Chemistry) Exercises

This repository contains a collection of hands-on exercises developed for the **HybriLIT Workshop 2026**. The exercises introduce computational approaches to molecular modelling, thermochemistry, chemical reactions, and molecular magnetic properties.

The practical examples combine the **Atomic Simulation Environment (ASE)** with electronic-structure codes and machine-learning interatomic potentials. They are designed to demonstrate how different computational methods can be applied to molecular systems and how their predictions can be compared with experimental reference data.

## Exercises

| Exercise | Scientific topic | Main computational tools |
|---|---|---|
| [Exercise 01](exercise_01/README.md) | Verification of the computational environment | ASE, MACE, MOPAC, NWChem |
| [Exercise 02](exercise_02/README.md) | Gas-phase combustion enthalpy of methane | MACE, MOPAC/PM7, NWChem/DFT |
| [Exercise 03](exercise_03/README.md) | Diels–Alder [4+2] cycloaddition | MACE-OFF23, MOPAC/PM7 |
| [Exercise 04](exercise_04/README.md) | Molecular magnetizability of H₂ | ASE, PySCF, GIAO-DFT |

## Repository organization

Each exercise is contained in a separate directory:

- `exercise_01/` — Installation and verification of the computational software.
- `exercise_02/` — Calculation of methane combustion enthalpy using different computational approaches.
- `exercise_03/` — Investigation of the Diels–Alder cycloaddition reaction.
- `exercise_04/` — Calculation of the magnetic-response properties of molecular hydrogen.

Where applicable, individual exercise directories contain separate implementations using different computational methods. Python scripts perform the calculations, while saved output and log files provide reference results.

## Getting started

1. Set up the required Python environment and install the computational software.
2. Start with Exercise 01 to verify the installation.
3. Proceed through the exercises in numerical order.
4. Follow the instructions in the corresponding README file before running each calculation.
5. Compare your results with the reference calculations and experimental values provided.

The numerical results documented in this repository correspond to specific computational settings and software versions. Small differences may occur when calculations are repeated using different software versions, model checkpoints, or computational environments.

The exercises are intended for educational purposes and provide practical examples of the strengths and limitations of different computational approaches to molecular modelling.


