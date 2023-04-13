from tqdm.contrib.concurrent import process_map
from functools import partial
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import cv2

def norm(x):
    return ((x-x.min())/x.max())

color_map = plt.get_cmap("magma")

def worker(data, shape):
    data = norm(abs(data.T))
    return (color_map(data)[:,:,[2,1,0]] * 204 + shape).astype(np.uint8) # 204 = .8 * 255

def export_video(simulation, export_path, scale=1):
    if len(simulation.output) == 0:
        print("Error: no data sample. Make sure to specify sample_interval= during run()")
        return 

    eps_data = simulation.get_epsilon().T
    eps_mask = eps_data==eps_data.min()

    shape = np.zeros_like(eps_data)
    shape[eps_mask] = 30 # 0.2 * 255

    frames = process_map(partial(worker,shape=shape[:,:,None]), simulation.output, desc="Generating Frames")

    frames_to_video(frames, export_path, scale=scale)


def frames_to_video(frames, export_path, scale=1, fps=60):
    h,w = frames[0].shape[:-1]
    size = (int(w*scale), int(h*scale))

    out_writer = cv2.VideoWriter(export_path,cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),fps, size)

    for frame in tqdm(frames,desc="Exporting {}".format(export_path)):
        out_writer.write(cv2.resize(frame, dsize=size))
    out_writer.release()