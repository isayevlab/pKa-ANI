## INSTALLATION

To install pKa-ANI, navigate to the directory of the source that you've downloaded and ;
   
```bash     
python setup.py install
```

### **PREREQUISITES:**

* miniconda/anaconda
* python >=3.6
* pytorch
* torchani
* ase
* pdbfixer (requires OpenMM 6.3 or later)
* joblib
* numpy,scipy

Other libraries: os,math,sys,io,csv,re,getopt,shutil,urllib.request,warnings 

#### Installations of prerequisites: 

##### **1. PYTORCH and TORCHANI:**

Prior to the installation of torch and torchani user should make sure miniconda/anaconda is installed

Install Pytorch for your system from: https://pytorch.org/get-started/locally/

Torchani: https://github.com/aiqm/torchani

```bash
conda install -c conda-forge torchani=2.2.0 cudatoolkit=11.2
```

##### **2. ASE:**

https://wiki.fysik.dtu.dk/ase/install.html

```bash
pip install --upgrade --user ase
```

or

```bash
conda install -c conda-forge ase
```

##### **3. JOBLIB:**

https://joblib.readthedocs.io/en/latest/installing.html

```bash
pip install joblib
```

or

```bash
conda install -c anaconda joblib
```

##### **4. IF PDB PREPARATION IS GOING TO BE USED : OPENMM and PDBFIXER**

OPENMM: http://docs.openmm.org/latest/userguide/index.html

```bash
conda install -c conda-forge openmm
```		

PDBFIXER: https://github.com/openmm/pdbfixer

```bash
conda install -c conda-forge pdbfixer
```
		
## **USAGE**

pKa-ANI requires PDB files to have H atoms that are added with default ionization states of residues: ASP, GLU, LYS, TYR, HID. 

If the PDB file does not involve H atoms, preparation utilty of pKa-ANI can be used (see below). 


### Example command line usages:

* If PDB file doesnt exist, it is downloaded and prepared for pKa calculations (default ionization states and H atoms are added).

```bash
pkaani -i 1BNZ
      
pkaani -i 1BNZ.pdb
```

* Multiple files can be given as inputs

```bash
pkaani -i 1BNZ,1E8L
```

* If a specific directory is wanted:

```bash
pkaani -i path_to_file/1BNZ
      
pkaani -i path_to_file/1BNZ,path_to_file/1E8L
```

* If PDB file exist but not prepared for pKa calculations (no H atom added):

```bash
pkaani -i 1BNZ -p T
      
pkaani -i 1BNZ,1E8L -p True
```

### Arguments: 

```bash
-h: Help

-i: Input files. Inputs can be given with or without file extension (.pdb). 
    If PDB file is under a specific directory (or will be downloaded) the path                 
    can also be given as path_to_file/PDBFILE. Multiple PDB files can be given 
    by using "," as separator (i.e. pkaani -i 1BNZ,1E8L).

-p: Prepare pdb for pKa calculations. If value is set to True, heteroatoms (except DNA and RNA) 
    are removed, missing atoms added, and H atoms are added at pH=7 
    (default ionization states: ASP, GLU, LYS, TYR, HID). 
    If the pdb file is not accessible and will be downloaded from RCSB, its value is not taken 
    into account. 
    Default value is False for accessible PDB files.
```				 

## **CITATION**

Gokcan, H.; Isayev, O. Prediction of Protein p K a with Representation Learning. Chem. Sci. 2022, 13 (8), 2462–2474. https://doi.org/10.1039/D1SC05610G.				 
## **LICENSING**

Please read LICENSE file.
