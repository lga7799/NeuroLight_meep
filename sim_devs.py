from simulation import Simulation, omega, NL_Si, mp
from visualization import export_video


from ring_devices import *

if __name__ == "__main__":

    width = 15
    height = 15

    geo,srcs = doublering()
    #srcs = [mp.Source(mp.GaussianSource(0.15, width=1e-6), mp.Hz, center=mp.Vector3(2.25,0,0))]

    sim = Simulation(
        grid_size=(width,height),
        grid_resolution=40,
        geometry=geo,
        sources=srcs
    )

    sim.run(until_after_sources=200, sample_interval=0.2)

    export_video(sim, export_path="double_ring.mp4", scale=2)

