from typing import Optional, Tuple
import numpy as np
import meep as mp
#from pyutils.compute import gen_gaussian_filter2d_cpu
from itertools import product
from simulation import NL_Si, NL_SiO2, omega

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
        super().__init__()
        self.radius=radius
        self.ring_width=ring_width
        self.center=center
        
    def geo(self):
        r1 = mp.Cylinder(radius=self.radius+self.ring_width, material=NL_Si, center=mp.Vector3(self.center[0],self.center[1],0))
        r2 = mp.Cylinder(radius=self.radius, material=NL_SiO2, center=mp.Vector3(self.center[0],self.center[1],0))
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
        
    def geo(self):
        return mp.Block(mp.Vector3(self.dimensions[0],self.dimensions[1],0),
            center=mp.Vector3(self.center[0],self.center[1],0),
            material=NL_Si)
    
    def source(self, freq, duration):
         return mp.Source(mp.GaussianSource(freq, width=duration),component=mp.Hz,
               center=mp.Vector3(-((self.dimensions[0]-1)/2),self.center[1],0))

def ring():
    r=2.2 #inner radius
    w = np.random.uniform(0.8, 1.1)
    index_si = 3.48
    ring = ring_r_w(
        radius=r,
        index=index_si,
        ring_width=w,
    )
    (r1, r2) = ring.geo()
    return [r1, r2]

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
    return wg.geo()

def ring_doublecoupled():
    r=2.2 #inner radius
    l=12 #length
    w = np.random.uniform(0.8, 1.1)
    x_offset1=0
    y_offset1=-4
    x_offset2=0
    y_offset2=4
    index_si = 3.48
    freq=0.15
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
    (cyl1, cyl2) = ring.geo()
    return ([cyl1, cyl2, wg1.geo(), wg2.geo()], [wg1.source(freq)])

def ring_singlecoupled(radius, width, wg_length, wg_width, wvlen, duration, gap):
    y_center = -(radius+width+wg_width/2+gap)
    freq = omega(wvlen)
    ring = ring_r_w(
        radius=radius,
        ring_width=width,
    )
    wg1 = waveguide_block(
        dimensions=(wg_length,wg_width),
        center=(0,y_center)
    )
    (cyl1, cyl2) = ring.geo()
    ring_coupler=[cyl1,cyl2,wg1.geo()]
    return (ring_coupler, [wg1.source(freq,duration)])

def ring_perp_coupler():
    r=2.2 #inner radius
    l=6 #length
    w = np.random.uniform(0.8, 1.1)
    x_offset1=0
    y_offset1=-4
    x_offset2=4
    y_offset2=0
    index_si = 3.48
    freq=0.15
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
    (cyl1, cyl2) = ring.geo()
    ring_coupler=[cyl1,cyl2,wg1.geo(), wg2.geo()]
    return (ring_coupler, [wg1.source(freq)])

def doublering():
    r1 = 2.2
    r2 = 2
    l = 12
    w = np.random.uniform(0.8, 1.1)
    index_si = 3.48
    freq = 0.15
    ring1 = ring_r_w(
        radius=r1,
        index=index_si,
        ring_width=w,
    )
    ring2 = ring_r_w(
        radius=r2,
        index=index_si,
        ring_width=w,
        center=(0,r1+(2*w)+r2)
    );
    wg1 = waveguide_block(
        dimensions=(l,w),
        index=index_si,
        center=(0,-(r1+w))
    );
    wg2 = waveguide_block(
        dimensions=(l,w),
        index=index_si,
        center=(0,r1+(3*w)+(2*r2))
    );
    (cyl1, cyl2) = ring1.geo()
    (cyl3, cyl4) = ring2.geo()
    return ([cyl1, cyl2, cyl3, cyl4, wg1.geo(), wg2.geo()], [wg1.source(freq)])