# -----------------------------------------------------------------
# Copyright (c) 2015, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file TRNSYS_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------

import sys, os, shutil, pickle


def saveTrnsysInstallDir( trnsys_install_dir ):
        # Save name of install directory to file (used by script 'trnsys_fmu_create.py').
        output = open( 'trnsys_fmu_install.pkl', 'wb' )
        pickle.dump( trnsys_install_dir, output )
        output.close()


def installType6139( trnsys_proformas_dir ):
        # Create directory if necessary.
        try:
                os.mkdir( trnsys_proformas_dir )
        except OSError:
                pass
        
        # Copy Type6139 proforma files to TRNSYS installation.
        shutil.copy( os.path.join( 'proformas', 'Type6139a.tmf' ), trnsys_proformas_dir )
        shutil.copy( os.path.join( 'proformas', 'Type6139b.tmf' ), trnsys_proformas_dir )
        
        # Copy Type6139 icons to TRNSYS installation.
        shutil.copy( os.path.join( 'proformas', 'Type6139a.bmp' ), trnsys_proformas_dir )
        shutil.copy( os.path.join( 'proformas', 'Type6139b.bmp' ), trnsys_proformas_dir )
        
        # Set directory for Type6139 library.
        trnsys_userlib_dir = os.path.join( trnsys_install_dir, 'UserLib', 'ReleaseDLLs' )
        
        # Copy Type6139 library to TRNSYS installation.
        shutil.copy( os.path.join( 'binaries', 'Type6139Lib.dll' ), trnsys_userlib_dir )


if __name__ == "__main__":
        
        # Check for correct number of input parameters.
        if( 2 != len( sys.argv ) ):
                print '\nERROR: Wrong number of arguments!\n\n\nUsage:\n\n\tpython trnsys_fmu_install.py <trnsys_install_directory>\n'
                sys.exit()

        # Set TRNSYS installation directory.
        trnsys_install_dir = sys.argv[1]
        
        # Check if directory exists.
        if( False == os.path.isdir( trnsys_install_dir ) ):
                print '\nERROR:', trnsys_install_dir, 'is not a valid directory'
	
        # Set directory for installation of Type6139 proforma files and icons.
        trnsys_proformas_dir = os.path.join( trnsys_install_dir, 'Studio', 'Proformas', 'FMI')

        # Save name of install directory to file (used by script 'trnsys_fmu_create.py').
        saveTrnsysInstallDir( trnsys_install_dir )
        
        # Install Type6139.
        installType6139( trnsys_proformas_dir )
