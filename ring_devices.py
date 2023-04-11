from typing import Optional, Tuple
import numpy as np
#from angler.structures import get_grid
#import torch
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
        index: float = 3.4,
        center:Tuple[float,float] = (0,0),
    ):
        super().init()
        self.radius=radius
        self.ring_width=ring_width
        self.index=index
        self.center=center

class waveguide_block(object):
    def __init__(
        self,
        dimensions: Tuple[float,float] = (0,0),
        center: Tuple[float,float] = (0,0),  # in/out wavelength width, um
        index: float = 3.4,
    ):
        super().init()
        self.dimensions=dimensions
        self.center=center
        self.index=index

def ring():
    r=2.2 #inner radius
    w = np.random.uniform(0.8, 1.1)
    index_si = 3.48
    ring = ring_r_w(
        radius=r,
        index=index_si,
        ring_width=w,
    )
    return ring

def waveguide():
    l=2.2 #inner radius
    w = np.random.uniform(0.8, 1.1)
    x_offset=0
    y_offset=0
    index_si = 3.48
    wg = waveguide_block(
        dimensions=(l,w),
        index=index_si,
        center=(x_offset,y_offset),
    )
    return wg
