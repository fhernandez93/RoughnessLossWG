import numpy as np
import tidy3d.web as web
import tidy3d as td
from tidy3d.components.data.data_array import SpatialDataArray
import h5py
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import date
import os
from tidy3d.plugins.dispersion import FastDispersionFitter, AdvancedFastFitterParam
from tidy3d.plugins.mode import ModeSolver



class loadAndRunStructure:
   

    def __init__(self, key:str, sim_size:float=6, 
                wg_width:float = 1.5,
                wg_height:float = 1.5,
                wg_permittivity:float = 6,
                lambda0:float=2,
                source_width:float = 0.35,
                runtime:float = 1e-12, 
                resolution:int=20, #grids per wvl
                run:bool=True,
                freqs:int=20,
                num_modes:int = 5
                ):
        if not key:
            raise Exception("No API key was provided")
        else:
            web.configure(key)

        self.Lx,self.Ly,self.Lz = [sim_size]*3
        self.lambda0 = lambda0
        self.freq0 = td.C_0/lambda0
        self.fwidth = self.freq0*source_width
        self.waveguide = td.Structure(
                    geometry=td.Box(size=(wg_height,wg_width, td.inf)),
                    medium=td.Medium(permittivity=wg_permittivity)
                )
        self.resolution = resolution
        self.runtime = runtime
        self.freqs = freqs 
        self.num_modes = num_modes
        self.sim = self.create_sim_obj()
        if run: 
            self.mode_data = (self.create_mode_solver()).solve()
        else: 
            self.mode_data = []
        
    def create_sim_obj(self):
        sim = td.Simulation(
        size=(self.Lx, self.Ly, self.Lz),
        grid_spec=td.GridSpec.auto(min_steps_per_wvl=self.resolution, wavelength=self.lambda0),
        structures=[self.waveguide],
        run_time=self.runtime,
        boundary_spec=td.BoundarySpec.all_sides(boundary=td.Periodic()),
        )
        return sim
    
    def create_mode_solver(self):
        plane = td.Box(center=(0, 0, 0), size=(4, 3.5, 0))
        mode_spec = td.ModeSpec(
            num_modes=self.num_modes
            )
        freqs = np.linspace(self.freq0 - self.fwidth / 2, self.freq0 + self.fwidth / 2, self.freqs)
        mode_solver = ModeSolver(
        simulation=self.sim,
        plane=plane,
        mode_spec=mode_spec,
        freqs=freqs
        )
        return mode_solver






        

       