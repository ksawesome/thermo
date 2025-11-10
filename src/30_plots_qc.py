import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load data
df = pd.read_csv('data/pTv_points.csv')
df_sat = pd.read_csv('data/sat_curve.csv')

# 2D plot
fig, ax = plt.subplots()
ax.scatter(df['v'], df['T'], c=df['p'], cmap='viridis')
ax.plot(df_sat['v'], df_sat['T'], 'r-', label='Saturation')
ax.set_xlabel('v (m³/kg)')
ax.set_ylabel('T (K)')
ax.set_title('p(T,v) for R134a')
plt.colorbar(ax.collections[0], label='p (Pa)')
plt.legend()
plt.savefig('docs/figures/pTv_plot.png')
plt.show()

# 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['v'], df['T'], df['p'], c=df['p'], cmap='viridis')
ax.set_xlabel('v (m³/kg)')
ax.set_ylabel('T (K)')
ax.set_zlabel('p (Pa)')
ax.set_title('3D p(T,v) for R134a')
plt.savefig('docs/figures/pTv_3d.png')
plt.show()