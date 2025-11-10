import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI

# Refrigerant
fluid = 'R134a'

# Temperatures
T_evap = 268  # K (-5 C)
T_cond = 313  # K (40 C)
superheat = 5  # K
subcool = 5  # K

# Pressures
p_evap = PropsSI('P', 'T', T_evap, 'Q', 1, fluid)
p_cond = PropsSI('P', 'T', T_cond, 'Q', 0, fluid)

# State 1: Evaporator exit (superheated vapor)
T1 = T_evap + superheat
p1 = p_evap
h1 = PropsSI('H', 'T', T1, 'P', p1, fluid)
s1 = PropsSI('S', 'T', T1, 'P', p1, fluid)
v1 = 1 / PropsSI('D', 'T', T1, 'P', p1, fluid)

# State 2: Compressor exit (saturated vapor at condenser pressure, assume T_cond)
T2 = T_cond
p2 = p_cond
h2 = PropsSI('H', 'T', T_cond, 'Q', 1, fluid)
s2 = PropsSI('S', 'T', T_cond, 'Q', 1, fluid)
v2 = 1 / PropsSI('D', 'T', T_cond, 'Q', 1, fluid)

# State 3: Condenser exit (subcooled liquid)
T3 = T_cond - subcool
p3 = p_cond
h3 = PropsSI('H', 'T', T3, 'P', p3, fluid)
s3 = PropsSI('S', 'T', T3, 'P', p3, fluid)
v3 = 1 / PropsSI('D', 'T', T3, 'P', p3, fluid)

# State 4: Expansion exit (saturated liquid at evaporator pressure)
T4 = T_evap
p4 = p_evap
h4 = PropsSI('H', 'T', T4, 'Q', 0, fluid)
s4 = PropsSI('S', 'T', T4, 'Q', 0, fluid)
v4 = 1 / PropsSI('D', 'T', T4, 'Q', 0, fluid)

# Debug prints for enthalpies
print(f"h1: {h1}, h2: {h2}, h3: {h3}, h4: {h4}")
print(f"p_evap: {p_evap}, p_cond: {p_cond}")

# Cycle calculations
w_comp = h2 - h1  # Work per kg
q_evap = h1 - h4  # Heat absorbed per kg (since h4 = h3)
q_cond = h2 - h3  # Heat rejected per kg
COP = q_evap / w_comp

print(f"COP: {COP:.2f}")
print(f"Work: {w_comp/1000:.1f} kJ/kg")
print(f"Q_evap: {q_evap/1000:.1f} kJ/kg")

# Exergy analysis
T0 = 298  # K
p0 = 1e5  # Pa
h0 = PropsSI('H', 'T', T0, 'P', p0, fluid)
s0 = PropsSI('S', 'T', T0, 'P', p0, fluid)

def exergy(h, s):
    return (h - h0) - T0 * (s - s0)

ex1 = exergy(h1, s1)
ex2 = exergy(h2, s2)
ex3 = exergy(h3, s3)
ex4 = exergy(h4, s4)

# Exergy destruction
ex_dest_comp = ex1 - ex2 + w_comp  # Since w is exergy input
ex_dest_cond = ex2 - ex3 + (h3 - h2)  # Heat rejected at T_cond
ex_dest_evap = ex4 - ex1 + (h1 - h4)  # Heat absorbed at T_evap
ex_dest_exp = ex3 - ex4  # Throttling

print(f"Exergy destruction comp: {ex_dest_comp/1000:.1f} kJ/kg")
print(f"Exergy destruction cond: {ex_dest_cond/1000:.1f} kJ/kg")
print(f"Exergy destruction evap: {ex_dest_evap/1000:.1f} kJ/kg")
print(f"Exergy destruction exp: {ex_dest_exp/1000:.1f} kJ/kg")

# Plots
# T-s
T_range = np.linspace(240, 350, 100)
s_sat_liq = [PropsSI('S', 'T', T, 'Q', 0, fluid) for T in T_range]
s_sat_vap = [PropsSI('S', 'T', T, 'Q', 1, fluid) for T in T_range]

plt.figure()
plt.plot(s_sat_liq, T_range, 'b-', label='Sat liquid')
plt.plot(s_sat_vap, T_range, 'r-', label='Sat vapor')
plt.plot([s1, s2, s3, s4, s1], [T1, T2, T3, T4, T1], 'k-o', label='Cycle')
plt.xlabel('s (J/kgK)')
plt.ylabel('T (K)')
plt.title('T-s Diagram')
plt.legend()
plt.savefig('docs/figures/Ts_diagram.png')
plt.show()

# p-h
plt.figure()
plt.plot([h1, h2, h3, h4, h1], [p1, p2, p3, p4, p1], 'k-o')
plt.xlabel('h (J/kg)')
plt.ylabel('p (Pa)')
plt.title('p-h Diagram')
plt.savefig('docs/figures/ph_diagram.png')
plt.show()

# Sensitivity
superheats = np.arange(1, 11, 1)
COPs = []
for sh in superheats:
    T1_sh = T_evap + sh
    h1_sh = PropsSI('H', 'T', T1_sh, 'P', p_evap, fluid)
    w_sh = h2 - h1_sh
    q_sh = h1_sh - h3
    COPs.append(q_sh / w_sh)

plt.figure()
plt.plot(superheats, COPs)
plt.xlabel('Superheat (K)')
plt.ylabel('COP')
plt.title('COP vs Superheat')
plt.savefig('docs/figures/COP_superheat.png')
plt.show()