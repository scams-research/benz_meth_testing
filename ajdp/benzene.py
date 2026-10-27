import MDAnalysis as mda
import numpy as np

class benzene:
    def __init__(self, universe):
        self.universe = universe
        self.benzene_atoms = self.universe.select_atoms('type 1 2 3 4 5 6 7 8 9 10 11 12')
        self.benzene_residues = self.benzene_atoms.residues
        self.carbon_atoms = self.universe.select_atoms('type 1 2 3 4 5 6')
        self.hydrogen_atoms = self.universe.select_atoms('type 7 8 9 10 11 12')
         
    def get_unwrapped_positons(self):
        n_residues = len(self.benzene_residues)
        n_atoms = len(self.benzene_residues[0].atoms)
        residue = range(n_atoms)
        residues = range(n_residues)
        arr = np.empty((n_residues, n_atoms), dtype=object)
        for res in residues:
            unwrapped_res = self.benzene_residues[res].atoms.unwrap()
            for atom in residue:
                arr[res:atom] = unwrapped_res[atom,:]
        return arr
        
    def gen_pi_up_vector(self):
        # calulating the  direction propgation of one side of the pi sytem
        # this done by defing a vectors with in the plane and then taking their the cross products tobtain a vector normal to the plane of the benzene ring
        res = self.benzene_residues[0].atoms.unwrap()
        self.center = self.benzene_residues[0].atoms.center_of_geometry(compound='residues', unwrap=True)
        carbon_1 = res[0,:]
        carbon_2 = res[1,:]
        vector1 = self.center - carbon_1
        vector2 = self.center - carbon_2
        pi_up_vector = np.cross(vector1, vector2)
        return pi_up_vector 

    def gen_center_to_carbon_vector(self):
        # calculating the vector from the center of the benzene ring to the center of the carbon atoms
        self.center = self.benzene_residues.center_of_geometry(compound='residues', unwrap=True)
        center_to_carbon_vector = self.center - self.carbon_atoms.select_atoms('type 1').unwrap()
        return center_to_carbon_vector
