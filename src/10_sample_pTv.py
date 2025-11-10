import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from CoolProp.CoolProp import PropsSI

# Define T and v grids
T_min, T_max = 220, 360  # K
T_step = 2  # K
T_grid = np.arange(T_min, T_max + T_step, T_step)

v_min, v_max = 0.0015, 0.2  # m³/kg
v_grid = np.logspace(np.log10(v_min), np.log10(v_max), 100)  # log spacing

# Initialize lists for data
data_points = []
sat_liquid = []
sat_vapor = []

# Function to compute p(T, v)
def compute_p(T, v):
    rho = 1 / v  # kg/m³
    try:
        p = PropsSI('P', 'T', T, 'D', rho, 'R134a')  # Pa
        return p
    except:
        return np.nan  # Invalid state

# Sample p(T, v)
for T in T_grid:
    for v in v_grid:
        p = compute_p(T, v)
        if not np.isnan(p):
            data_points.append({'T': T, 'v': v, 'p': p})

# Compute saturation curve
for T in T_grid:
    try:
        p_sat = PropsSI('P', 'T', T, 'Q', 0, 'R134a')  # Sat liquid
        rho_liq = PropsSI('D', 'T', T, 'Q', 0, 'R134a')
        v_liq = 1 / rho_liq
        sat_liquid.append({'T': T, 'v': v_liq, 'p': p_sat})
        
        p_sat_v = PropsSI('P', 'T', T, 'Q', 1, 'R134a')  # Sat vapor
        rho_vap = PropsSI('D', 'T', T, 'Q', 1, 'R134a')
        v_vap = 1 / rho_vap
        sat_vapor.append({'T': T, 'v': v_vap, 'p': p_sat_v})
    except:
        pass

# Save to CSV
df_points = pd.DataFrame(data_points)
df_points.to_csv('data/pTv_points.csv', index=False)

df_sat = pd.DataFrame(sat_liquid + sat_vapor)
df_sat.to_csv('data/sat_curve.csv', index=False)

# Quick QC plot
fig, ax = plt.subplots()
ax.scatter(df_points['v'], df_points['T'], c=df_points['p'], cmap='viridis')
ax.plot(df_sat['v'], df_sat['T'], 'r-', label='Saturation')
ax.set_xlabel('v (m³/kg)')
ax.set_ylabel('T (K)')
ax.set_title('p(T,v) for R134a')
plt.colorbar(ax.collections[0], label='p (Pa)')
plt.legend()
plt.savefig('data/qc_plot.png')
plt.show()