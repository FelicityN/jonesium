#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Module for comparing enthalpies between different stacking sequences. 
"""
#from __future__ import print_function
import quippy
import numpy as np
from numpy import sqrt
from math import tan, pi
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


LJ=quippy.Potential("IP LJ", param_filename="LJ.xml")
# Use sig=1, (atom #14, type 1)


def aparray(sqnc):
    """Returns atom numpy array.
   
    Args:
        sqnc (string): polytype stacking sequence to be made into an array
          For example, 'abc' or 'abcabcacbacb'.

    Returns:
        numpy array
    """
    z=sqrt(2./3)
    b=sqrt(3)/6
    c=1-b
    
    atoms=[]
    for i, st in enumerate(sqnc):
        if st == 'a' or st == 'A':
            atoms.append([0., 0., i*z])
        elif st == 'b' or st == 'B':
            atoms.append([0.5, b, i*z])
        elif st == 'c' or st == 'C':
            atoms.append([0., c, i*z])
        else:
            raise ValueError("polytype stack sequence must only contain 'a', 'b', or 'c' orders")
    return np.array(atoms)
    


def enthalpy(sqnc, p=None):
    """Returns Helmholtz enthalpy, h=E+PV per atom of the polytype stack sequence

    Args:
        sqnc (string): polytype stacking sequence
          For example, 'abc' or 'abcabcacbacb'.
        p (float): hydrostatic pressure in epsilon per sigma cubed units; default None.

    Returns:
       float
    """

    apos=aparray(sqnc)
    N=len(apos)
    lat=[[1., 0., 0.],
         [0.5, sqrt(3)/2., 0.], 
         [0., 0., N*sqrt(2./3)]]

    numbers=[]
    for i in range(0,N):
        numbers.append(14)

    plyt=quippy.Atoms(n=N,
                      lattice=lat,
                      positions=apos,
                      numbers=numbers)

    plyt.set_cutoff(LJ.cutoff())
    plyt.calc_connect()
    LJ.calc(plyt, energy=True)
    e1=plyt.energy
    v=plyt.get_volume()
    print("Initial energy: ", e1)
    print("Initial volume: ", v)
    plyt.calc_connect()

    pressure=[[p, 0., 0.],
              [0., p, 0.],
              [0., 0., p]]
    
    LJ.minim(plyt, 'cg', 1e-12, 100, do_pos=True, do_lat=True, external_pressure=pressure)
    LJ.calc(plyt, energy=True)
    e2=plyt.energy
    v=plyt.get_volume()
    print("Energy for {} after relaxing: ".format(sqnc), e2)
    print("Volume after relaxing: ", v, " per ", N, " atoms.")
    #plyt.write("{}.xyz".format(sqnc))

    if p==None:
        p=0
    h=(e2+p*v)/N
    #hd=(hf-h)/N
    return h

def hdif(sqnclst, plst=[None]):
    """Returns the enthalpy difference of fcc and a list of polytype stacking 
sequences at various pressures.
    
    Args:
        sqnclst (list): list of polytype stacking sequences as a string.
        p (list): list of hydrostatic pressure as a float.

    Returns:
        list
    """
   # hf=enthalpy('abc',plst)
    hf=[]
    for p in plst:
        hf.append(enthalpy('abc',p))
    plytlst=[]
    
    for s in sqnclst:
        plist=[]
        for i, p in enumerate(plst):
            h=enthalpy(s, p)
            hd=(hf[i]-h)
            plist.append(hd)
        plytlst.append(plist)
    return plytlst

def plthdif(sqnclst, plst=[None]):
   """Plots the difference of the enthalpy of fcc versus other polytype stack 
sequences as a function of hydrostatic pressure. Returns a nested list of each 
polytype enthalpy difference at each specified pressure.

    Args:
       sqnclst (list): List of polytype stacking sequences.
         Example: ['abc','ab','abcbac'].
       plst (list): List of hydrostatic pressures. For p=0, use p=None.
   
   Returns:
      nested list 
    """
   plytlst=hdif(sqnclst, plst)
   plt.figure()
   plt.title("Polytype stacking sequence enthalpy difference")
   plt.ylabel('Enthalpy difference per atom')
   plt.xlabel('Pressure')
   for i, t in enumerate(plytlst):
       plt.plot(plst, t, label=sqnclst[i])
   plt.legend(loc=4)
   plt.savefig('hdifplt.pdf')
   return plytlst
