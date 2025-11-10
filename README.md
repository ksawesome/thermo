# ES211 R134a p(T,v) Surface and Vapor-Compression Cycle Analysis

This repository contains the implementation for ES211 project: creating a 3D physical model of the p(T,v) surface for R134a refrigerant and analyzing a vapor-compression refrigerator cycle.

## Project Structure

- `data/`: CSV files with p(T,v) data and saturation curves
- `stl/`: 3D model files
- `src/`: Python scripts for data generation, meshing, and analysis
- `cad/`: CAD files
- `print/`: Slicer settings and print files
- `report/`: Final report PDF
- `docs/`: Figures and receipts

## Setup

1. Create conda environment: `conda env create -f environment.yml`
2. Activate: `conda activate thermo-env`
3. Download `liquidvapor.cti` from Cantera data and place in root directory
4. Run scripts in `src/` in order

## Agents

- Property Agent: `src/10_sample_pTv.py` - Generates p(T,v) data
- Meshing Agent: `src/20_make_mesh.py` - Creates STL mesh
- QC Plots: `src/30_plots_qc.py` - Quality control plots
- Cycle Analysis: `src/40_cycle_analysis.py` - Thermodynamic cycle analysis