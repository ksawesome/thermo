# ES211 Report: R134a p(T,v) Surface and Vapor-Compression Refrigerator Analysis

## Title
3D Physical Model of Pressure-Temperature-Specific Volume Surface for R134a Refrigerant and Thermodynamic Analysis of Vapor-Compression Cycle

## Abstract
This report presents the development of a 3D physical model representing the p(T,v) thermodynamic surface for R134a refrigerant, including the saturation dome, and its application to understanding vapor-compression refrigeration cycles. The model was generated using computational property calculations, meshed into an STL file, and analyzed thermodynamically. Key results include COP of 10.64 for a domestic refrigerator cycle with specified conditions.

## 1. Introduction
### 1.1 Problem Statement
The assignment requires creating a 3D model of the p(T,v) surface for R134a across the saturation dome and analyzing a vapor-compression refrigerator cycle.

### 1.2 Objectives
- Generate accurate p(T,v) data grid
- Create manufacturable 3D mesh
- Perform cycle analysis with COP, exergy
- Produce professional report

## 2. Background
### 2.1 R134a Properties
R134a (1,1,1,2-tetrafluoroethane) is a hydrofluorocarbon refrigerant with GWP 1430, phase-out in progress.

### 2.2 Thermodynamic Surfaces
The p(T,v) surface shows pressure as function of temperature and specific volume, with saturation dome separating phases.

## 3. Methodology
### 3.1 Property Data Generation
Used CoolProp for R134a properties over T=220-360 K, v=0.0015-0.2 m³/kg.

### 3.2 Meshing
Interpolated data to regular grid, scaled to printer dimensions, exported STL.

### 3.3 Cycle Analysis
Modeled 4-state cycle with superheat/subcooling, calculated COP=10.64.

## 4. Results
### 4.1 Data and Plots
Figures: pTv_plot.png, pTv_3d.png, Ts_diagram.png, ph_diagram.png, COP_superheat.png

### 4.2 Cycle Performance
COP: 10.64
Work: 19.4 kJ/kg
Q_evap: 206.8 kJ/kg

### 4.3 3D Model
STL file ready for printing.

## 5. Discussion
The dome shape illustrates phase changes and cycle operation.

## 6. Conclusion
The 3D surface aids intuition for cycle design.

## References
1. CoolProp documentation
2. Thermodynamics textbooks

## Appendices
- Code: src/
- Data: data/
- STL: stl/
- Figures: docs/figures/