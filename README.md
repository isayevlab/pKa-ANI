PREREQUISITES:

* miniconda/anaconda
* torch
* torchani
* ase
* pdbfixer (requires OpenMM 6.3 or later)
* joblib
* numpy,scipy

Other libraries: os,math,sys,io,csv,re,getopt,shutil,urllib.request,warnings 


Installation: pip3 install pkaani-0.1.0.tar.gz

Installations of prerequisites: 

1. TORCH and TORCHANI:
	https://aiqm.github.io/torchani/start.html

	prior to the installation of torch and torchani 
	user should make sure miniconda/anaconda is installed


	pip install numpy
	pip install --pre torch torchvision -f https://download.pytorch.org/whl/nightly/cu100/torch_nightly.html
	pip install torchani

2. ASE:
	https://wiki.fysik.dtu.dk/ase/install.html

	pip install --upgrade --user ase

	or

	conda install -c conda-forge ase


3. JOBLIB:
	https://joblib.readthedocs.io/en/latest/installing.html

	pip install joblib

	or

	conda install -c anaconda joblib

4. IF PDB PREPARATION IS GOING TO BE USED : OPENMM and PDBFIXER

        http://docs.openmm.org/latest/userguide/index.html
 
        conda install -c conda-forge openmm
		

        https://github.com/openmm/pdbfixer
		
		conda install -c conda-forge pdbfixer
		
###########################################################################

USAGE

Example usages:

  * If PDB file doesnt exist, it is downloaded and prepared for pKa calculations.

      pkaani -i 1BNZ
      pkaani -i 1BNZ.pdb

  * Multiple files can be given as inputs

      pkaani -i 1BNZ,1E8L

  * If a specific directory is wanted:

      pkaani -i path_to_file/1BNZ
      pkaani -i path_to_file/1BNZ,path_to_file/1E8L

  * If PDB file exist but not prepared for pKa calculations (no H atom added):

      pkaani -i 1BNZ -p T
      pkaani -i 1BNZ,1E8L -p True


  Arguments: -i: Input files. Inputs can be given with or without
                 file extension (.pdb). If PDB file is under a
                 specific directory (or will be downloaded) the path
                 can also be given as path_to_file/PDBFILE.
                 Multiple PDB files can be given
                 by using "," as separator (i.e. pkaani -i 1BNZ,1E8L).

             -p: Prepare for pKa calculations. If value is set to
                 True, heteroatoms (except DNA and RNA)
                 are removed, missing atoms added,
                 and H atoms are added at pH=7 (default ionization states:
                 ASP, GLU, LYS, TYR, HID).
                 If the pdb file is not accessible and will be downloaded
                 from RCSB, its value is not taken into account.
                 Default value is False for accessible PDB files.
				 
###########################################################################

CITATION

Gokcan, H.; Isayev, O. Prediction of Protein p K a with Representation Learning. Chem. Sci. 2022, 13 (8), 2462–2474. https://doi.org/10.1039/D1SC05610G.				 
