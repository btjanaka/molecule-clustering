#!/usr/bin/env python

#=============================================================================================
# MODULE DOCSTRING
#=============================================================================================

"""
calc_improper.py

Find and calculate improper dihedral angles in a given molecule.
Code loosely follows OpenMM: https://tinyurl.com/y8mhwxlv

Let's say we have j as central atom and call addTorsion(j, i, k, l).
Then we compute the following vectors:

  v0 = j-i
  v1 = k-i
  v2 = k-l
  w0 = v0 x v1
  w1 = v1 x v2

The final improper angle is computed as the angle between w0 and w1.

By: Victoria Lim <limvt@uci.edu>

"""

#=============================================================================================
# GLOBAL IMPORTS
#=============================================================================================

import numpy as np
import openeye.oechem as oechem
from openeye import oequacpac
#=============================================================================================
# PRIVATE SUBROUTINES
#=============================================================================================

def angle_between(v1, v2):
    """
    Calculate the angle in degrees between vectors 'v1' and 'v2'.
    Modified from: https://tinyurl.com/yb89sstz

    Parameters
    ----------
    v1 : tuple, list, or numpy array
    v2 : tuple, list, or numpy array

    Returns
    -------
    float
        Angle in degrees.

    """
    v1_u = v1/np.linalg.norm(v1)
    v2_u = v2/np.linalg.norm(v2)
    return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

def calc_valence_angle(atom0, atom1, atom2):
    """
    Calculate the valence angle of three atoms.

    Parameters
    ----------
    atom0 : numpy array
        CENTRAL atom coordinates
    atom1 : numpy array
        outer atom coordinates
    atom2 : numpy array
        outer atom coordinates

    Returns
    -------
    float
        Angle in degrees.
    """
    v1 = atom1-atom0
    v2 = atom2-atom0
    return(angle_between(v1, v2))

def calc_improper_angle(atom0, atom1, atom2, atom3, translate=False):
    """
    Calculate the improper dihedral angle of a set of given four atoms.

    Parameters
    ----------
    atom0 : numpy array
        CENTRAL atom coordinates
    atom1 : numpy array
        outer atom coordinates
    atom2 : numpy array
        outer atom coordinates
    atom3 : numpy array
        outer atom coordinates
    translate : bool
        True to translate central atom to origin, False to keep as is.
        This should not affect the results of the calculation.

    Returns
    -------
    float
        Angle in degrees.
    """
    if translate:
        atom1 = atom1 - atom0
        atom2 = atom2 - atom0
        atom3 = atom3 - atom0
        atom0 = atom0 - atom0 # central must be moved last

    # calculate vectors
    v0 = atom0-atom1
    v1 = atom2-atom1
    v2 = atom2-atom3
    w1 = np.cross(v0, v1)
    w2 = np.cross(v1, v2)
    angle = angle_between(w1,w2) # this angle should be in range [0,90]

    # compute distance from plane to central atom
    # eq 6 from http://mathworld.wolfram.com/Point-PlaneDistance.html
    # here I'm using atom1 for (x,y,z), but could also use atom2 or atom3
    numer = w2[0]*(atom0[0]-atom1[0]) + w2[1]*(atom0[1]-atom1[1]) + w2[2]*(atom0[2]-atom1[2])
    denom = np.sqrt(w2[0]**2 + w2[1]**2 + w2[2]**2)
    dist = numer/denom
    # set reference so that if central atom is above plane, angle -> [90,180]
    #print("this is the distance:" + str(dist))
    if dist < 0:
        angle = angle*-1
    #angle = abs(angle)
    return angle

def find_improper_angles(mol):
    """
    Find the improper dihedral angles in some molecule. Currently supports
    those with a central trivalent nitrogen atom.

    Parameters
    ----------
    mol : OpenEye oemol
        oemol in which to look for improper angles

    Returns
    -------
    list
        Each element in the list is a 4-tuple of the coordinates for the
        atoms involved in the improper. The central atom is listed first
        in the tuple. Each member of the tuple is a numpy array.
    list
        List of strings for atoms in the improper, central atom is first.
    """

    mol_coords = mol.GetCoords()
    crdlist = []
    Idxlist = []
    for atom in mol.GetAtoms(oechem.OEIsInvertibleNitrogen()):
        # central atom
        aidx = atom.GetIdx()
        crd0 = np.asarray(mol_coords[aidx])
        # sort the neighbors
        nbors = sorted(list(atom.GetAtoms()))
        #check if there are 3 atoms connected to central atom in improper
        if len(nbors) != 3:
            return crdlist, namelist
        crd1 = np.asarray(mol_coords[nbors[0].GetIdx()])
        crd2 = np.asarray(mol_coords[nbors[1].GetIdx()])
        crd3 = np.asarray(mol_coords[nbors[2].GetIdx()])
        # store coordinates
        crdlist.append([crd0, crd1, crd2, crd3])
        Idxlist.append([atom.GetIdx(), nbors[0].GetIdx(), nbors[1].GetIdx(),nbors[2].GetIdx()])


    return crdlist, Idxlist



def get_atomTypes(mol):
    """
    """

    mol_coords = mol.GetCoords()
    typelist = []
    for atom in mol.GetAtoms(oechem.OEIsInvertibleNitrogen()):
        # central atom
        aidx = atom.GetIdx()
        crd0 = np.asarray(mol_coords[aidx])
        # sort the neighbors
        nbors = sorted(list(atom.GetAtoms()))
        #check if there are 3 atoms connected to central atom in improper
        if len(nbors) != 3:
            return crdlist, namelist
        # store coordinates
        print(atom.GetName())
        typelist.append([nbors[0].GetAtomicNum(), nbors[1].GetAtomicNum(),nbors[2].GetAtomicNum()])
    return typelist


def get_aromatic(mol):
    """
    """

    mol_coords = mol.GetCoords()
    typelist = []
    for atom in mol.GetAtoms(oechem.OEIsInvertibleNitrogen()):
        # central atom
        aidx = atom.GetIdx()
        crd0 = np.asarray(mol_coords[aidx])
        # sort the neighbors
        nbors = sorted(list(atom.GetAtoms()))
        #check if there are 3 atoms connected to central atom in improper
        if len(nbors) != 3:
            return crdlist, namelist
        # store coordinates
        print(atom.GetName())
        typelist.append([nbors[0].IsAromatic(), nbors[1].IsAromatic(),nbors[2].IsAromatic()])
    return typelist



def get_aroInd(mol, index):
    """
    """

    mol_coords = mol.GetCoords()
    typelist = []
    for atom in mol.GetAtoms():
        # central atom
        aidx = atom.GetIdx()
        if aidx == index:
            aro=atom.IsAromatic()
    return aro



def get_atomInd(mol, index):
    """
    """

    mol_coords = mol.GetCoords()
    typelist = []
    for atom in mol.GetAtoms():
        # central atom
        aidx = atom.GetIdx()
        if aidx == index:
            atomnum=atom.GetAtomicNum()
    return atomnum



AM1 = oequacpac.OEAM1()


def BO(mol):
    """
    """

    mol_coords = mol.GetCoords()
    BOList = []
    for atom in mol.GetAtoms(oechem.OEIsInvertibleNitrogen()):
        # central atom
        aidx = atom.GetIdx()
        crd0 = np.asarray(mol_coords[aidx])
        # sort the neighbors
        nbors = sorted(list(atom.GetAtoms()))
        #check if there are 3 atoms connected to central atom in improper
        if len(nbors) != 3:
            return crdlist, namelist
        results = oequacpac.OEAM1Results()
        AM1.CalcAM1(results, mol)
        bond1=results.GetBondOrder(atom.GetIdx(), nbors[0].GetIdx())
        bond2=results.GetBondOrder(atom.GetIdx(), nbors[1].GetIdx())
        bond3=results.GetBondOrder(atom.GetIdx(), nbors[2].GetIdx())
        BOList=[bond1, bond2, bond3]
        total=bond1+bond2+bond3
    return BOList,total





