#determine complex SBU with 4, 6, 12 connection points#

from scipy.spatial.transform import Rotation as R
from scipy.optimize import minimize
import numpy as np
from scipy.linalg import svd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse


# Define the ideal geometries:
perfect_tetrahedron = np.array([[1, 1, 1], [-1, 1, -1], [1, -1, -1], [-1, -1, 1]])#0
perfect_square = np.array([[1, 1, 0], [-1, 1, 0], [-1, -1, 0], [1, -1, 0]])#1

perfect_hex_planar = np.array([
    [1, np.sqrt(3), 0], 
    [1, -np.sqrt(3), 0], 
    [-1, -np.sqrt(3), 0], 
    [-1, np.sqrt(3), 0],
    [0, 2*np.sqrt(3), 0],
    [0, -2*np.sqrt(3), 0]
]) #2
perfect_octahedron = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]])#3
perfect_trp = np.array([
    [np.sqrt(3)/2, 0.5, 0.5],  # Top triangle vertex 1
    [-np.sqrt(3)/2, 0.5, 0.5], # Top triangle vertex 2
    [0, -1, 0.5],              # Top triangle vertex 3
    [np.sqrt(3)/2, 0.5, -0.5], # Bottom triangle vertex 1 (directly below top vertex 1)
    [-np.sqrt(3)/2, 0.5, -0.5],# Bottom triangle vertex 2 (directly below top vertex 2)
    [0, -1, -0.5]              # Bottom triangle vertex 3 (directly below top vertex 3)
])

golden_ratio = (1 + np.sqrt(5)) / 2
perfect_cuo = np.array([
    [1, 0, 1], [-1, 0, 1], [1, 0, -1], [-1, 0, -1],
    [0, 1, 1], [0, -1, 1], [0, 1, -1], [0, -1, -1],
    [1, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, -1, 0]
]) / np.sqrt(2)  # Cuboctahedron 5
perfect_ico = np.array([
    [-1, golden_ratio, 0], [1, golden_ratio, 0], [-1, -golden_ratio, 0], [1, -golden_ratio, 0],
    [0, -1, golden_ratio], [0, 1, golden_ratio], [0, -1, -golden_ratio], [0, 1, -golden_ratio],
    [golden_ratio, 0, -1], [golden_ratio, 0, 1], [-golden_ratio, 0, -1], [-golden_ratio, 0, 1]
]) # Icosahedron 6
perfect_hpr = np.array([
    [np.cos(theta), np.sin(theta), 0.5] for theta in np.linspace(0, 2*np.pi, 6, endpoint=False)
] + [
    [np.cos(theta), np.sin(theta), -0.5] for theta in np.linspace(0, 2*np.pi, 6, endpoint=False)
])  # Hexagonal Prism 7 
perfect_tte = np.array([
    [1, 1, 1], [-1, 1, 1], [1, -1, 1], [-1, -1, 1],
    [0, 1, -np.sqrt(2)], [0, -1, -np.sqrt(2)], [1, np.sqrt(2), 0], [-1, np.sqrt(2), 0],
    [-np.sqrt(2), 0, 1], [np.sqrt(2), 0, -1], [1, -np.sqrt(2), 0], [-1, -np.sqrt(2), 0]
]) # Truncated Tetrahedron 8

# Create a list of all perfect geometries and their names
perfect_geometries = [
    (perfect_tetrahedron, "tet"), 
    (perfect_square, "square"), 
    (perfect_hex_planar, "hexagon"), 
    (perfect_octahedron, "oct"),
    (perfect_trp, "trp"),
    (perfect_cuo, "cuo"), 
    (perfect_ico, "ico"), 
    (perfect_hpr, "hpr"), 
    (perfect_tte, "tte")
]

def fit_model(X, perfect_geometry):
    def RMSD(params):
        """Compute the RMSD between X and the perfect geometry."""
        r = R.from_rotvec(params[0:3] * params[3])
        X_rot = r.apply(X - np.mean(X, axis=0))
        return np.sqrt(((X_rot - perfect_geometry)**2).mean())

    result = minimize(RMSD, x0=np.array([1, 0, 0, 0]))
    return result.fun

def read_xyz(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    atom_lines = lines[2:]

    X = []

    for line in atom_lines:
        parts = line.split()
        if parts[0].upper() == 'X':
            coords = list(map(float, parts[1:4]))
            X.append(coords)

    return np.array(X)


def is_planar(points, tol=5e-1):
    
    """Check if a set of points is planar."""
    points = points - np.mean(points, axis=0)  # subtract centroid
    U, s, V = svd(points)  # singular value decomposition
    return s[-1] < tol  # if last singular value is small, the points are coplanar

    
def plot_shape(points, title):
    hull = ConvexHull(points)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    
    for s in hull.simplices:
        s = np.append(s, s[0])  # Here we cycle back to the first coordinate
        ax.plot(points[s, 0], points[s, 1], points[s, 2], "r-")
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title(title)
    plt.show()

def determin_geo(filename):
    
    X = read_xyz(filename)

    if len(X) == 4:
        if is_planar(X):
            geometries_to_check = [perfect_geometries[i] for i in [1]]  # Square
        else:
            geometries_to_check = [perfect_geometries[i] for i in [0]]  # Tetrahedron
    elif len(X) == 6:
        if is_planar(X):
            geometries_to_check = [perfect_geometries[i] for i in [2]]  # Hexagonal 
        else:
            geometries_to_check = [perfect_geometries[i] for i in [3, 4]]  # Octahedron
    elif len(X) == 12:
        geometries_to_check = [perfect_geometries[i] for i in [5, 6, 7, 8]]  # Cuboctahedron, Icosahedron, and Truncated Tetrahedron
    else:
        print("No known geometry corresponds to this number of atoms")
        exit()

    min_rmsd = np.inf
    min_geometry_name = ""
    for perfect_geometry, geometry_name in geometries_to_check:
        rmsd = fit_model(X, perfect_geometry)
        print(f"RMSD for {geometry_name}: {rmsd}")
        if rmsd < min_rmsd:
            min_rmsd = rmsd
            min_geometry_name = geometry_name

    print(f"\nThe shape of the molecule most closely resembles a {min_geometry_name} with an RMSD of {min_rmsd}")
    
#    plot_shape(X, filename)
    return filename.split('.xyz')[0]+'_'+min_geometry_name

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Determine the geometry of a molecule from .xyz file')
    parser.add_argument('filename', type=str, help='Path to the .xyz file')
    args = parser.parse_args()

    determin_geo(args.filename)
