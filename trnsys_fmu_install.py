# -----------------------------------------------------------------
# Copyright (c) 2017-2018, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file TRNSYS_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------

import sys, os, shutil, pickle

def log( *arg ):
    print( ' '.join( map( str, arg ) ) )
    sys.stdout.flush()


def saveTrnsysInstallDir( trnsys_install_dir, trnsys_fmu_root_dir ):
        # Save name of install directory to file (used by script 'trnsys_fmu_create.py').
        output = open( os.path.join( trnsys_fmu_root_dir, 'trnsys_fmu_install.pkl' ), 'wb' )
        pickle.dump( trnsys_install_dir, output )
        output.close()


def installType6139( trnsys_proformas_dir, trnsys_fmu_root_dir, trnsys_install_dir ):
    # Create directory if necessary.
    try:
        os.mkdir( trnsys_proformas_dir )
    except OSError:
        pass
    
    # Copy Type6139 proforma files to TRNSYS installation.
    shutil.copy( os.path.join( trnsys_fmu_root_dir, 'sources', 'proformas', 'Type6139a.tmf' ), trnsys_proformas_dir )
    shutil.copy( os.path.join( trnsys_fmu_root_dir, 'sources', 'proformas', 'Type6139b.tmf' ), trnsys_proformas_dir )
    
    # Copy Type6139 icons to TRNSYS installation.
    shutil.copy( os.path.join( trnsys_fmu_root_dir, 'sources', 'proformas', 'Type6139a.bmp' ), trnsys_proformas_dir )
    shutil.copy( os.path.join( trnsys_fmu_root_dir, 'sources', 'proformas', 'Type6139b.bmp' ), trnsys_proformas_dir )
    
    # Set directory for Type6139 library.
    trnsys_userlib_dir = os.path.join( trnsys_install_dir, 'UserLib', 'ReleaseDLLs' )
    
    # Copy Type6139 library to TRNSYS installation.
    shutil.copy( os.path.join( trnsys_fmu_root_dir, 'binaries', 'Type6139Lib.dll' ), trnsys_userlib_dir )


def main( trnsys_fmu_root_dir, trnsys_install_dir ):
    # Check if directory exists.
    if( False == os.path.isdir( trnsys_install_dir ) ):
        log( '\nERROR:', trnsys_install_dir, 'is not a valid directory' )
        sys.exit(1)
	
    # Set directory for installation of Type6139 proforma files and icons.
    trnsys_proformas_dir = os.path.join( trnsys_install_dir, 'Studio', 'Proformas', 'FMI')

    try:
        # Save name of install directory to file (used by script 'trnsys_fmu_create.py').
        saveTrnsysInstallDir( trnsys_install_dir, trnsys_fmu_root_dir )
    
        # Install Type6139.
        installType6139( trnsys_proformas_dir, trnsys_fmu_root_dir, trnsys_install_dir )
    except Exception as e:
        log( e )
        modules.sys.exit( e.args[0] )
    
    log( "\nFMI++ TRNSYS FMU Export Utility installed successfully!\n" )


if __name__ == "__main__":

    # Check for correct number of input parameters.
    if( 2 != len( sys.argv ) ):
        log( '\nERROR: Wrong number of arguments!\n\n\nusage:\n\n\tpython trnsys_fmu_install.py <trnsys_install_directory>\n' )
        sys.exit()

    # Set TRNSYS installation directory.
    trnsys_install_dir_ = sys.argv[1]

    # Relative or absolute path to TRNSYS FMU Export Utility.
    trnsys_fmu_root_dir_ = os.path.dirname( __file__ )

    main( trnsys_fmu_root_dir_, trnsys_install_dir_ )
