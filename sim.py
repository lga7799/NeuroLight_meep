# Generate data set
import meep as mp
from simulation import Simulation
from visualization import export_video
import ring_devices as device
import numpy as np
import torch

def save_data(simulation, box_height, box_length, sim_num):
  fields = {}
  eps_list = []
  fields_list = []
  eps_data = simulation.get_epsilon().T;

  fields["Ex"] = simulation.get_array(center=mp.Vector3(), size=mp.Vector3(box_length, box_height), component=mp.Ex);
  fields["Ey"] = simulation.get_array(center=mp.Vector3(), size=mp.Vector3(box_length, box_height), component=mp.Ey);
  fields["Hz"] = simulation.get_array(center=mp.Vector3(), size=mp.Vector3(box_length, box_height), component=mp.Hz);

  eps_list.append(np.stack(eps_data, axis=0))
  fields_list.append(np.stack([fields["Ex"], fields["Ey"], fields["Hz"]], axis=0))

  epsilon_list = torch.from_numpy(np.stack(eps_list, axis=0).astype(np.complex64)[:, :, np.newaxis, :]).transpose(-1, -2)
  field_list = torch.from_numpy(np.stack(fields_list, axis=0).astype(np.complex64)).transpose(-1, -2)

  import os
  if not os.path.isdir("./raw"):
    os.mkdir("./raw")
  torch.save(
    {
      "eps": epsilon_list,
      "fields": field_list
    },
    f"./raw/sim_{sim_num}.pt"
  )
  

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
    sim_num = 0

    radius_list = []
    width_list = []
    wg_len_list = []
    wg_wid_list = []
    gap_list = []
    wavelength_list = []

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
                                save_data(sim, box_height, box_length, sim_num)
                                sim_num += 1
                                
                                radius_list.append(r)
                                width_list.append(w)
                                wg_len_list.append(wl)
                                wg_wid_list.append(ww)
                                gap_list.append(g)
                                wavelength_list.append(wave)
                                #export_video(sim, export_path="example.mp4", scale=3)
    torch.save(
      {
        "radius": radius_list,
        "width": width_list,
        "wg_length": wg_len_list,
        "wg_width": wg_wid_list,
        "gap": gap_list,
        "wavelength": wavelength_list,
      },
      f"./raw/params.pt"
    )
