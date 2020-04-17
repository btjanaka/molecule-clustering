# Molecule Clustering

Here, we seek to automatically create improper angle parameters from the
trivalent nitrogen dataset generated in
[DANCE](https://github.com/btjanaka/dance-old). To do this, we run grid
optimization calculations on each molecule, where we calculate the energy of the
molecule as we vary the improper angle at its trivalent nitrogen. We hypothesize
that molecules which share similar energy profiles (AKA 1D scans) will share
similar chemical properties, particularly Wiberg bond order. To check for this
similarity, we cluster the molecules by various properties of their 1D scan.
Thus far, we have not found any significant evidence of a relationship between
1D scans and chemical properties.

## Instructions

Set up the conda environment with:

```
conda env create -f environment.yml
```

Run notebooks with

```
jupyter notebook
```
