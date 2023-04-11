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
    l=4 #length
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

def ring_doublecoupled():
    r=2.2 #inner radius
    l=4 #length
    w = np.random.uniform(0.8, 1.1)
    x_offset1=0
    y_offset1=-4
    x_offset2=0
    y_offset2=4
    index_si = 3.48
    ring = ring_r_w(
        radius=r,
        index=index_si,
        ring_width=w,
    )
    wg1 = waveguide_block(
        dimensions=(l,w),
        index=index_si,
        center=(x_offset1,y_offset1),
    )
    wg2 = waveguide_block(
        dimensions=(l,w),
        index=index_si,
        center=(x_offset2,y_offset2),
    )
    cyl1=mp.Cylinder(radius=ring.radius+ring.ring_width, material=mp.Medium(index=index_si))
    cyl2=mp.Cylinder(radius=ring.radius)
    block1 = mp.Block(mp.Vector3(wg1.dimensions[0],wg1.dimensions[1],0),
                     center=mp.Vector3(wg1.center[0],wg1.center[1],0),
                     material=mp.Medium(index=wg1.index))
    
    block2 = mp.Block(mp.Vector3(wg2.dimensions[0],wg2.dimensions[1],0),
                     center=mp.Vector3(wg2.center[0],wg2.center[1],0),
                     material=mp.Medium(index=wg2.index))
    ring_coupler=[cyl1,cyl2,block2, block1]
    return ring_coupler

def ring_singlecoupled():
    r=2.2 #inner radius
    l=4 #length
    w = np.random.uniform(0.8, 1.1)
    x_offset1=0
    y_offset1=-4
    index_si = 3.48
    ring = ring_r_w(
        radius=r,
        index=index_si,
        ring_width=w,
    )
    wg1 = waveguide_block(
        dimensions=(l,w),
        index=index_si,
        center=(x_offset1,y_offset1),
    )
    
    cyl1=mp.Cylinder(radius=ring.radius+ring.ring_width, material=mp.Medium(index=index_si))
    cyl2=mp.Cylinder(radius=ring.radius)
    block1 = mp.Block(mp.Vector3(wg1.dimensions[0],wg1.dimensions[1],0),
                     center=mp.Vector3(wg1.center[0],wg1.center[1],0),
                     material=mp.Medium(index=wg1.index))
    ring_coupter=[cyl1,cyl2,block1]
    return ring_coupter

def ring_perp_coupler():
    r=2.2 #inner radius
    l=6 #length
    w = np.random.uniform(0.8, 1.1)
    x_offset1=0
    y_offset1=-4
    x_offset2=4
    y_offset2=0
    index_si = 3.48
    ring = ring_r_w(
        radius=r,
        index=index_si,
        ring_width=w,
    )
    wg1 = waveguide_block(
        dimensions=(l,w),
        index=index_si,
        center=(x_offset1,y_offset1),
    )
    wg2 = waveguide_block(
        dimensions=(w,l),
        index=index_si,
        center=(x_offset2,y_offset2),
    )
    cyl1=mp.Cylinder(radius=ring.radius+ring.ring_width, material=mp.Medium(index=index_si))
    cyl2=mp.Cylinder(radius=ring.radius)
    block1 = mp.Block(mp.Vector3(wg1.dimensions[0],wg1.dimensions[1],0),
                     center=mp.Vector3(wg1.center[0],wg1.center[1],0),
                     material=mp.Medium(index=wg1.index))
    
    block2 = mp.Block(mp.Vector3(wg2.dimensions[0],wg2.dimensions[1],0),
                     center=mp.Vector3(wg2.center[0],wg2.center[1],0),
                     material=mp.Medium(index=wg2.index))
    ring_coupler=[cyl1,cyl2,block2, block1]
    return ring_coupler
