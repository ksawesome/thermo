import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from stl import mesh

# Load data
df = pd.read_csv('data/pTv_points.csv')

# Use log v for better visualization
df['log_v'] = np.log10(df['v'])

# Define scales
T_scale = 1.0  # mm/K
v_scale = 50.0  # mm per decade
p_scale = 1.0 / 20000.0  # mm per Pa (1 mm per 0.2 bar)

# Min values for offset
T_min = df['T'].min()
log_v_min = df['log_v'].min()
p_min = df['p'].min()

# Create coordinates
df['x'] = (df['T'] - T_min) * T_scale
df['y'] = (df['log_v'] - log_v_min) * v_scale
df['z'] = (df['p'] - p_min) * p_scale  # offset to positive

# Define regular grid for mesh
x_unique = np.linspace(df['x'].min(), df['x'].max(), 100)
y_unique = np.linspace(df['y'].min(), df['y'].max(), 100)
X, Y = np.meshgrid(x_unique, y_unique)

# Interpolate Z
Z = griddata((df['x'], df['y']), df['z'], (X, Y), method='linear', fill_value=0)

# Create STL mesh
def create_height_field_mesh(X, Y, Z):
    rows, cols = Z.shape
    vertices = []
    faces = []
    
    for i in range(rows - 1):
        for j in range(cols - 1):
            # Four corners
            v1 = [X[i, j], Y[i, j], Z[i, j]]
            v2 = [X[i, j+1], Y[i, j+1], Z[i, j+1]]
            v3 = [X[i+1, j], Y[i+1, j], Z[i+1, j]]
            v4 = [X[i+1, j+1], Y[i+1, j+1], Z[i+1, j+1]]
            
            # Two triangles
            faces.append([v1, v2, v3])
            faces.append([v2, v4, v3])
    
    return faces

faces = create_height_field_mesh(X, Y, Z)

# Flatten to numpy array
faces_array = np.array(faces)

# Create mesh
surface_mesh = mesh.Mesh(np.zeros(faces_array.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces_array):
    for j in range(3):
        surface_mesh.vectors[i][j] = f[j]

# Add base plate
base_height = -5  # mm below
base_faces = []
# Simple base: rectangle
base_v1 = [X.min(), Y.min(), base_height]
base_v2 = [X.max(), Y.min(), base_height]
base_v3 = [X.min(), Y.max(), base_height]
base_v4 = [X.max(), Y.max(), base_height]

base_faces.append([base_v1, base_v2, base_v3])
base_faces.append([base_v2, base_v4, base_v3])

base_array = np.array(base_faces)
base_mesh = mesh.Mesh(np.zeros(base_array.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(base_array):
    for j in range(3):
        base_mesh.vectors[i][j] = f[j]

# Combine meshes
combined = mesh.Mesh(np.concatenate([surface_mesh.data, base_mesh.data]))

# Save
combined.save('stl/pTv_surface.stl')

print("STL saved to stl/pTv_surface.stl")