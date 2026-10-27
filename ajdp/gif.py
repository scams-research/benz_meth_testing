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
import shutil                                                # CHANGED: added
from PIL import Image
import glob

start_frames = 0
end_frames = 2000

dt = 4
DATA = '../prod_traj/prod.data'
ATOM = '../prod_traj/production_2000fra_50fs_per_fra.atom'
u = mda.Universe(DATA, ATOM, format="LAMMPSDUMP", topology_format="DATA", dt=dt)

benz = benzene(u)

x = []
time = []
ims = []

trajectory = u.trajectory[start_frames:end_frames]
time = np.arange(start_frames*dt, end_frames*dt, dt)

for ts in trajectory:
    pi_up_vec = benz.gen_pi_up_vector()
    x.append(pi_up_vec[0,0])
    atoms = []
    for i in range(6):
        res = benz.benzene_residues[0].atoms.unwrap()
        c = res[i,:]
        h = res[i+6,:]
        a = Atom('C', c)
        b = Atom('H', h)
        atoms.append(a)
        atoms.append(b)
    vis = Atoms(atoms)
    ims.append(vis)

b, a = signal.butter(2, 0.01, btype='low', analog=False, fs=1/dt)
x_filt = signal.filtfilt(b, a, x)

plt.plot(time, x_filt, label='x (filtered)', color='blue')
plt.plot(time, x, label='x (raw)', color='grey', alpha=0.5)
plt.xlabel('Time (fs)')
plt.ylabel('X component of pi up vector')
plt.legend()
plt.savefig(f'pi_up_vector_x_component_{end_frames} - {start_frames}frames.pdf', bbox_inches='tight')
plt.close()

frames = range(len(trajectory))

# CHANGED: wipe old images and the old GIF at the start of every run
for d in ('image_frames', 'combined'):
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)

if os.path.exists('side_by_side.gif'):
    os.remove('side_by_side.gif')

for f in frames:
    vis = ims[f]
    write(f'image_frames/benzene{f}.png', vis)
    img = imread(f'image_frames/benzene{f}.png')

    fig, (ax_img, ax_plot) = plt.subplots(1, 2, figsize=(10, 4), dpi=100)

    ax_img.imshow(img)
    ax_img.axis('off')

    ax_plot.plot(time, x, color='grey', alpha=0.3)
    ax_plot.plot(time[:f+1], x_filt[:f+1], color='blue', label='x (filtered)')
    ax_plot.plot(time[f], x_filt[f], 'o', color='red')
    ax_plot.set_xlim(time[0], time[-1])
    ax_plot.set_ylim(min(x), max(x))
    ax_plot.set_xlabel('Time (fs)')
    ax_plot.set_ylabel('X component of pi up vector')
    ax_plot.legend()

    fig.tight_layout()
    fig.savefig(f'combined/combined_{f:05d}.png')
    plt.close(fig)

files = sorted(glob.glob('combined/combined_*.png'))
imgs = [Image.open(p).convert('RGB') for p in files]
imgs[0].save(f'side_by_side{start_frames}-{end_frames}.gif', save_all=True, append_images=imgs[1:], duration=2.5, loop=0)
print(len(files), 'frames written')