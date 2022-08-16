import sys
from sys import stdout
import os
import numpy as np
import re

#from urllib.request import urlopen
#from io import StringIO

#pdbfixer, uses openmm Modeller
from pdbfixer import PDBFixer

#pdb fixer doesnt have force field option
#so we will use Modeller, and ForceField 
#to write PDBFile
from openmm.app import PDBFile,Modeller 
from openmm.app import ForceField



def rem_altloc(pdbin,pdbout):
    #REMOVE ALTERNATE LOCATIONS

    swords = ['ATOM', 'HETATM','TER','END']
    altlocs= [' ','A']
    regex = f"^({'|'.join(swords)})"
    contentsall=[]
    
    with open(pdbin, 'r+') as fd:
         contents = fd.readlines()
         for line in contents:
             result=re.search(regex,line)
             #get lines starts with swords
             if(result):
                #do not get alternate location B
                if(('ATOM' in line or 'HETATM' in line) and line[16] in altlocs): 
                   result2 = line[0:16] + " " + line[16+1: ]
                   line=result2
                   contentsall.append(line)   
                if('TER' in line or 'END' in line):
                   contentsall.append(line)
                             
    with open(pdbout, 'w') as f:
      for line in contentsall:
        f.write(line)
    
    
def fixer_func(pdbin,pdbout):

    forcefield = ForceField('amber99sb.xml', 'tip3p.xml')
    ph=7.0 #default ionization state
    
    fixer = PDBFixer(filename=pdbin)
    pdbcode=pdbin.rsplit('temp.', 1)[0]
    fmname=pdbcode      

    fixer.findMissingResidues()
    fixer.findMissingAtoms()
    fixer.findNonstandardResidues()
    fixer.removeHeterogens(keepWater=False)
    
    fixer.addMissingAtoms() 

    modeller=Modeller(fixer.topology,fixer.positions) 

    residues = [residue.name for residue in modeller.topology.residues()]
    rvariants = [None]*len(residues)
    for i,res in enumerate(residues):
        if(res=='HIS'):
          rvariants[i]='HIE'

    modeller.addHydrogens(forcefield=forcefield,variants=rvariants)

    with open(pdbout, 'w') as outfile:
         PDBFile.writeFile(modeller.topology, modeller.positions, file=outfile, keepIds=True)


def prep_pdb(inputpdb):

    pdbid=inputpdb.rsplit('_', 1)[0]
    print('Preparing %s for pKa calculations' % pdbid)
 
    pdbid=inputpdb.rsplit('.', 1)[0]
    
    '''
       1st remove remarks,alternate locations, etc.
       if alternate location exists
       only get location A of atom
       need to perform since fixer doesnt recognize altloc
       
       For example
       
            ATOM      8  CE ALYS A   1      -0.975   8.165  10.101  0.67 16.48           C
            ANISOU    8  CE ALYS A   1     2499   2053   1555    411   -278     73       C
            ATOM      9  CE BLYS A   1      -0.963   8.369  10.347  0.33 11.01           C
            ANISOU    9  CE BLYS A   1     1373   1733    974   -247    329    166       C
    
       will be replaced as
       
            ATOM      8  CE  LYS A   1      -0.975   8.165  10.101  0.67 16.48           C
       
       
    '''
    
    
    fin=pdbid+".pdb" #"_RCSB.pdb"
    fout=pdbid+"temp.pdb"    
    rem_altloc(fin,fout)
    
    fin=fout
    
    fout=pdbid.rsplit('_', 1)[0]+'.pdb'
    fixer_func(fin,fout)
    
    #clean files   
    if os.path.exists(pdbid+"temp.pdb"):
       os.remove(pdbid+"temp.pdb")   
    


