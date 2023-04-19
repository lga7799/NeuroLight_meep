# Generate data set
import meep as mp
from simulation import Simulation
from visualization import export_video
import ring_devices as device

if __name__ == "__main__":
    dpml = 1.5 # thickness of PML
    radius = [2, 4] #[2, 4, 6, 8, 10]
    width = [0.4] #, 0.5, 0.6, 0.7, 0.8]
    wg_len = [4.8, 9.6] #, 14.4, 19.2, 24]
    wg_wid = [0.4] #, 0.5, 0.6, 0.7, 0.8]
    gap = [0.1] #, 0.2, 0.3, 0.4]
    wavelength = [1.53] #, 3, 4.5, 6]
    box_height = 30
    box_length = 30
    duration=1e-9

    for r in radius:
        for w in width:
            for wl in wg_len:
                if wl >= 2*r+w:
                    for ww in wg_wid:
                        for wave in wavelength:
                            for g in gap:
                                (geo, src) = device.ring_singlecoupled(radius[radius.index(r)], width[width.index(w)], wg_len[wg_len.index(wl)], wg_wid[wg_wid.index(ww)], wavelength[wavelength.index(wave)], duration, gap[gap.index(g)])

                                sim = Simulation(
                                    grid_size=(box_length,box_height),
                                    grid_resolution=10,
                                    geometry=geo, 
                                    sources=src,
                                    PML_thickness=dpml
                                )

                                sim.run(until_after_sources=200, sample_interval=0.1)

                                export_video(sim, export_path="example.mp4", scale=3)
