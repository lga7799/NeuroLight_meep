from typing import Optional, Tuple
import numpy as np
from angler.structures import get_grid
import torch
import meep as mp
#from pyutils.compute import gen_gaussian_filter2d_cpu
from itertools import product

eps_sio2 = 1.44 ** 2
eps_si = 3.48 ** 2

class ring_r_w(object):
    def __init__(
        self,
        radius: float = 2.2,
        ring_width: float =  0.4,  # in/out wavelength width, um
        box_size: Tuple[float, float] = (20,20),  # box [length, width], um
        port_len: float = 10,  # length of in/out waveguide from PML to box. um
        border_width: float = 3,  # space between box and PML. um
        grid_step: float = 0.1,  # isotropic grid step um per pixel/grid(inverse of resolution pixels per um)
        NPML: Tuple[int, int] = (20, 20),  # PML pixel width. pixel
        index: float = 3.4,
        eps_r: float = eps_si,  # relative refractive index
        eps_bg: float = eps_sio2,  # background refractive index
    ):
        super().init()
        self.radius=radius
        self.ring_width=ring_width
        self.box_size=box_size
        self.port_len=port_len
        self.border_width=border_width
        self.grid_step=grid_step
        self.NPML=NPML
        self.eps_r=eps_r
        self.eps_bg=eps_bg
        self.index=index



def ring():
    N = 2 #Assume 2 ports: 1 input 1 output
    pad= 4#spacing in um
    r=2.2 #inner radius
    w = np.random.uniform(0.8, 1.1)
    index_si = 3.48
    dpml=2
    sxy= 2*(r+w+pad+dpml)
    #size = (np.random.uniform(40, 50), np.random.uniform(10, 14))
    port_len = 3
    ring = ring_r_w(
        radius=r,
        index=index_si,
        ring_width=w,
        box_size=[sxy,sxy],
        port_len=port_len,
        grid_step=0.05,
        NPML=[dpml,dpml],
        border_width=pad
    )
    #w, h = (size[0] * np.random.uniform(0.7, 0.9), size[1] / N * np.random.uniform(0.4, 0.65))
    return ring