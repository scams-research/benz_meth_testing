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
from mdanalysis.

start_frames = 0
end_frames = 2000

dt = 4
DATA = '../prod_traj/prod.data'
ATOM = '../prod_traj/production_2000fra_50fs_per_fra.atom'
u = mda.Universe(DATA, ATOM, format="LAMMPSDUMP", topology_format="DATA", dt=dt, )
unwrap_form = mda.transformations.unwrap(u.atoms)
u.trajectory.add_transformations(unwrap_form)

benz = benzene(u)

trajectory = u.trajectory[start_frames:end_frames]
time = np.arange(start_frames*dt, end_frames*dt, dt)

x = []
for ts in trajectory:
    pi_up_vec = benz.gen_pi_up_vector()
    x.append(pi_up_vec[0,0])

b, a = signal.butter(2, 0.01, btype='low', analog=False, fs=1/dt)
x_filt = signal.filtfilt(b, a, x)

plt.plot(time, x_filt, label='x (filtered)', color='blue')
plt.plot(time, x, label='x (raw)', color='grey', alpha=0.5)
plt.xlabel('Time (fs)')
plt.ylabel('X component of pi up vector')
plt.legend()
plt.savefig(f'pi_up_vector_x_component_{start_frames} - {end_frames}frames_uniunwrap.pdf', bbox_inches='tight')

frames = range(len(trajectory))
