from simulation import Simulation, omega, NL_Si, mp
from visualization import export_video

def generate_IO(n_ports, box_width, box_height, port_width):
    ports_height = box_height*(n_ports-1)/(n_ports**2)
    v_step = (box_height-ports_height*n_ports)/(n_ports+1)
    h_step = (box_width+port_width)/2

    inputs = []
    outputs = []

    v_offset = -box_height/2 + v_step + ports_height/2

    for i in range(n_ports):
        inputs.append(mp.Block(mp.Vector3(port_width,ports_height,1),
                     center=mp.Vector3(-h_step,v_offset),
                     material=NL_Si))
        
        outputs.append(mp.Block(mp.Vector3(port_width,ports_height,1),
                     center=mp.Vector3(h_step,v_offset),
                     material=NL_Si))
        
        v_offset += v_step+ports_height

    return inputs, outputs

if __name__ == "__main__":

    width = 20
    height = 5

    box_width = width*0.8
    box_height = height*0.9

    block = mp.Block(mp.Vector3(box_width, box_height,1), material=NL_Si)

    I,O = generate_IO(2, box_width, box_height, box_width/10.0)

    freq = omega(1.53)
    duration = 1e-9

    sources = [mp.Source(mp.GaussianSource(freq, width=duration), mp.Hz, center=i.center) for i in I]

    sim = Simulation(
        grid_size=(width,height),
        grid_resolution=20,
        geometry=[block]+I+O,
        sources=sources
    )

    sim.run(until_after_sources=200, sample_interval=0.1)

    export_video(sim, export_path="example.mp4", scale=3)

