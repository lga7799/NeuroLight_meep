import meep as mp
import numpy as np

eps_sio2 = 1.44 ** 2
eps_si = 3.48 ** 2

NL_Si = mp.Medium(epsilon=eps_si)
NL_SiO2 = mp.Medium(epsilon=eps_sio2)

def omega(wavelength):
    return 2e6 * np.pi/wavelength

class Simulation(mp.Simulation):
    def __init__(self, grid_size, grid_resolution, geometry, sources, PML_thickness=1.5, **kwargs):
        super().__init__(
            cell_size=mp.Vector3(grid_size[0], grid_size[1]),
            geometry=geometry,
            sources=sources,
            resolution=grid_resolution,
            boundary_layers=[mp.PML(PML_thickness)],
            dimensions=2,
            default_material=NL_SiO2,
            **kwargs
            )
        
    def run(self,**kwargs):
        si = kwargs.pop("sample_interval",None)

        self.output = []
        if si is not None:
            super().run(
                mp.at_every(si, lambda x: self.output.append(x.get_hfield_z())),
                **kwargs)
        else:
            super().run(**kwargs)


