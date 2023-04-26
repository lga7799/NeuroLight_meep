from typing import Optional, Tuple
import numpy as np
import meep as mp
#from pyutils.compute import gen_gaussian_filter2d_cpu
from itertools import product
from simulation import NL_Si, NL_SiO2
        
class ring_r_w(object):
    def __init__(
        self,
        radius: float = 2.2,
        ring_width: float =  0.4,  # in/out wavelength width, um
        center:Tuple[float,float] = (0,0)
    ):
        super().__init__()
        self.radius=radius
        self.ring_width=ring_width
        self.center=center
        
    def geo(self):
        r1 = mp.Cylinder(radius=self.radius+self.ring_width, material=NL_Si, center=mp.Vector3(self.center[0],self.center[1],0))
        r2 = mp.Cylinder(radius=self.radius, material=NL_SiO2,center=mp.Vector3(self.center[0],self.center[1],0))
        return (r1, r2) 
    
class waveguide_block(object):
    def __init__(
        self,
        dimensions: Tuple[float,float] = (0,0),
        center: Tuple[float,float] = (0,0),  # in/out wavelength width, um
        index: float = 3.4,
    ):
        super().__init__()
        self.dimensions=dimensions
        self.center=center
        self.index=index
        
    def geo(self):
        return mp.Block(mp.Vector3(self.dimensions[0],self.dimensions[1],0),
            center=mp.Vector3(self.center[0],self.center[1],0),
            material=mp.Medium(index=self.index))
    
    def source(self, freq):
        return mp.Source(mp.GaussianSource(frequency=freq, width=1e-6),component=mp.Hz,
               center=mp.Vector3(-((self.dimensions[0]-2)/2),self.center[1],0))

def ring():
    r = 2 #inner radius
    w = 0.5 # np.random.uniform(0.8, 1.1)
    ring = ring_r_w(
        radius=r,
        ring_width=w
    )
    (r1, r2) = ring.geo()
    return [r1, r2]

def waveguide():
    l=4 #length
    w = np.random.uniform(0.8, 1.1)
    x_offset=0
    y_offset=0
    wg = waveguide_block(
        dimensions=(l,w),
        center=(x_offset,y_offset),
    )
    return wg.geo()

def ring_doublecoupled():
    r=2.8 #inner radius
    l=12 #length
    w = np.random.uniform(0.8, 1.1)
    x_offset1=0
    y_offset1=-4
    x_offset2=0
    y_offset2=4
    freq=0.15
    ring = ring_r_w(
        radius=r,
        ring_width=w,
    )
    wg1 = waveguide_block(
        dimensions=(l,w),
        center=(x_offset1,y_offset1),
    )
    wg2 = waveguide_block(
        dimensions=(l,w),
        center=(x_offset2,y_offset2),
    )
    (cyl1, cyl2) = ring.geo()
    return ([cyl1, cyl2, wg1.geo(), wg2.geo()], [wg1.source(freq)])

def ring_singlecoupled():
    r=2.2 #inner radius
    l=10 #length
    w = np.random.uniform(0.8, 1.1)
    x_offset1=0
    y_offset1=-3.4
    freq=0.15
    ring = ring_r_w(
        radius=r,
        ring_width=w,
    )
    wg1 = waveguide_block(
        dimensions=(l,w),
        center=(x_offset1,y_offset1)
    )
    (cyl1, cyl2) = ring.geo()
    ring_coupler=[cyl1,cyl2,wg1.geo()]
    return (ring_coupler, [wg1.source(freq)])

def ring_perp_coupler():
    r=2.5 #inner radius
    l=6 #length
    w = np.random.uniform(0.8, 1.1)
    x_offset1=0
    y_offset1=-4
    x_offset2=4
    y_offset2=0
    freq=0.15
    ring = ring_r_w(
        radius=r,
        ring_width=w,
    )
    wg1 = waveguide_block(
        dimensions=(l,w),
        center=(x_offset1,y_offset1),
    )
    wg2 = waveguide_block(
        dimensions=(w,l),
        center=(x_offset2,y_offset2),
    )
    (cyl1, cyl2) = ring.geo()
    ring_coupler=[cyl1,cyl2,wg1.geo(), wg2.geo()]
    return (ring_coupler, [wg1.source(freq)])

def doublering():
    r1 = 2.2
    r2 = 2
    l = 12
    w = np.random.uniform(0.8, 1.1)
    freq = 0.15
    h = 3
    ring1 = ring_r_w(
        radius=r1,
        ring_width=w,
        center=(0,-h)
    )
    ring2 = ring_r_w(
        radius=r2,
        ring_width=w,
        center=(0,r1+(2*w)+r2-h)
    );
    wg1 = waveguide_block(
        dimensions=(l,w),
        center=(0,-(r1+w)-h)
    );
    wg2 = waveguide_block(
        dimensions=(l,w),
        center=(0,r1+(3*w)+(2*r2)-h)
    );
    (cyl1, cyl2) = ring1.geo()
    (cyl3, cyl4) = ring2.geo()
    return ([cyl1, cyl2, cyl3, cyl4, wg1.geo(), wg2.geo()], [wg1.source(freq)])