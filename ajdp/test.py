from benzene import benzene
from methanol import methanol
import MDAnalysis as mda 
import numpy as np 
import matplotlib.pyplot as plt
import scipy.signal as signal
from ase import Atom, Atoms
from ase.io import write
from matplotlib.image import imread
import os

os.makedirs('combined', exist_ok=True)


dt = 4
DATA = '../prod_traj/prod.data'
ATOM = '../prod_traj/production_2000fra_50fs_per_fra.atom'
u = mda.Universe(DATA, ATOM, format="LAMMPSDUMP", topology_format="DATA", dt=dt)

benz = benzene(u)

n_residues = len(benz.benzene_residues)
n_atoms = len(benz.benzene_residues[0].atoms)

arr = np.zeros((n_residues,n_atoms))

print(f"{n_residues},{n_atoms}")
print(np.shape(arr))