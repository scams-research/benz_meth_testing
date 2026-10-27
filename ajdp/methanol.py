import MDAnalysis as mda
import numpy as np

class methanol:
    def __init__(self, universe):
        self.universe = universe
        self.methanol_atoms = self.universe.select_atoms('type 13 14 15 16 17 18 ')
        self.methanol_fragments = self.methanol_atoms.fragments
        self.oxygen_atoms = self.universe.select_atoms('type 14')
        self.hydrogen_OH__atoms = self.universe.select_atoms('type 18') # the hydrogens in the hydroxyl group
        self.carbon_atoms = self.universe.select_atoms('type 13')
        self.hydrogen_atoms = self.universe.select_atoms('type 15 16 17') # the hydrogens attached to the carbon

    def dipole_vector(self):
        # Calculate the dipole vector for each methanol molecule
        dipole_vectosrs = self.hydrogen_OH__atoms.positions - self.oxygen_atoms.positions
        return dipole_vectosrs
        
    