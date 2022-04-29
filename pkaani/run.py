import sys
import os
import getopt
import shutil
import numpy as np

from urllib.request import urlopen
from io import StringIO
from pkaani.pkaani import calculate_pka
from pkaani.prep_pdb import prep_pdb

def usage_pkaani():
    """
    Show how to use this program!
    """
    print("""
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
""")

def handle_arguments_pkaani():
    inp_file = None
    prep_files = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:p:", ["help", "prep=","inp="])
    except getopt.GetoptError:
        usage_pkaani()
		
    for opt, arg in opts:
	

        if opt in ('-h', "--help"):
            usage_pkaani()
            sys.exit(-1)
			
        elif opt in ("-p", "--prep"):
            prep_files = arg
			
        elif opt in ("-i", "--inp"):
            inp_file=[x.strip() for x in arg.split(',')]
			
        else:
            assert False, usage_pkaani()

    # Input PDB file is mandatory!
    if len(inp_file)==0: # is None:
        print("@> ERROR: A PDB file is mandatory!")
        usage_pkaani()
        sys.exit(-1)

    # The user may already prepared the PDB file for calculation.
    if prep_files is None:
        prep_files = False
	
    return inp_file, prep_files
        
def main():

    input_files, prep_files = handle_arguments_pkaani()    
    pdbfiles=np.array(input_files)
  
    #first check if PDB files are accessible 
    for inputpdb in pdbfiles:
        pdbid=inputpdb.rsplit('.', 1)[0]
        pdbfile=pdbid+".pdb"

        if os.path.exists(pdbfile):
           if(prep_files):
              os.rename(pdbfile,pdbid+"_0.pdb")
              prep_pdb(pdbid+"_0.pdb")

        else:
            base=os.path.basename(pdbfile)
            dpdbid=base.rsplit('.', 1)[0]

            print("File %s is not accessible" % pdbfile)
            print("Downloading : http://www.rcsb.org/pdb/files/%s.pdb" % dpdbid)
        
            url = 'http://www.rcsb.org/pdb/files/%s.pdb' % dpdbid
            
            file = urlopen(url)
            contents = file.read().decode('utf-8')
            file.close()
            file = StringIO(contents)

            outfile=pdbid+"_RCSB.pdb"
            
            with open(outfile, 'w') as f2:
              for line in contents:
                f2.write(line)
                
            prep_pdb(outfile)
        
    #CALCULATER PKA
    pkadict=calculate_pka(pdbfiles,writefile=True)

    #RENAME FILES PROPERLY
    for inputpdb in pdbfiles:
        pdbid=inputpdb.rsplit('.', 1)[0]
        pdbfile=pdbid+".pdb"

        if os.path.exists(pdbfile):
           if(prep_files):
              oldf=pdbfile
              newf=pdbid+"_prep.pdb"
              os.rename(oldf,newf)
              oldf=pdbid+"_0.pdb"
              newf=pdbfile
              os.rename(pdbid+"_0.pdb",pdbfile)

        dpdbfile=pdbid+"_RCSB.pdb"
        if os.path.exists(dpdbfile):
           os.rename(pdbfile,pdbid+"_prep.pdb")


if __name__ == "__main__":
    main()
    
    
