# -----------------------------------------------------------------
# Copyright (c) 2017, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file TRNSYS_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------

#
# This file is used to create FMUs for CoSimulation from TRNSYS deck files.
# 
# By default, it should be used with Python 3. By uncommenting lines 14 & 15
# and commenting lines 18 & 20, it can also be used with Python 2.
#

### Python 2
# import sys, os, shutil, time, getpass, uuid, getopt, pickle, subprocess, glob, argparse, urlparse, urllib, collections
# def log( *arg ): print ' '.join( map( str, arg ) )

### Python 3
import sys, os, shutil, time, getpass, uuid, getopt, pickle, subprocess, glob, argparse, urllib.parse as urlparse, urllib.request as urllib, collections
def log( *arg ): print( ' '.join( map( str, arg ) ), flush = True )

from scripts.utils import *
from scripts.generate_fmu import *

def main( trnsys_fmu_root_dir = os.path.dirname( __file__ ), parser = None ):

    Modules = collections.namedtuple( 'Modules', [ 'sys', 'os', 'shutil', 'time', 'getpass', 'uuid', 'urlparse', 'urllib', 'getopt', 'pickle', 'subprocess', 'glob', 'argparse', 'log' ] )
    modules = Modules( sys, os, shutil, time, getpass, uuid, urlparse, urllib, getopt, pickle, subprocess, glob, argparse, log )

    # Retrieve parsed command line arguments.
    cmd_line_args = parseCommandLineArguments( modules ) if ( parser == None ) else parser()

    # FMI model identifier.
    fmi_model_identifier = cmd_line_args.model_id

    # TRNSYS deck file.
    deck_file_name = cmd_line_args.deck_file

    # Set TRNSYS install dir.
    trnsys_install_dir = cmd_line_args.trnsys_install_dir

    # Verbose flag.
    verbose = cmd_line_args.verbose

    # Litter flag.
    litter = cmd_line_args.litter

    # FMI version
    fmi_version = cmd_line_args.fmi_version
    if ( True == verbose ): modules.log( '[DEBUG] Using FMI version', fmi_version )

    # Check if specified TRNSYS deck file exists.
    if ( False == os.path.isfile( deck_file_name ) ):
        modules.log( '\n[ERROR] Invalid TRNSYS deck file: ', deck_file_name )
        sys.exit(4)

    # Retrieve start values and additional files from command line arguments.
    ( optional_files, start_values ) = parseAdditionalInputs( cmd_line_args.extra_arguments, verbose, modules  )

    # Parse TRNSYS deck file to retrieve FMI input and output variable names.
    ( fmi_input_vars, fmi_output_vars, found_type_6139a, found_type_6139b ) = \
        parseDeckFile( deck_file_name, verbose, modules )

    # No TRNSYS install directory provided -> read from file (created by script 'trnsys_fmu_install.py').
    if ( None == trnsys_install_dir ):
        pkl_file_name = modules.os.path.join( trnsys_fmu_root_dir, 'trnsys_fmu_install.pkl' )
        if ( True == modules.os.path.isfile( pkl_file_name ) ):
            pkl_file = open( pkl_file_name, 'rb' )
            trnsys_install_dir = modules.pickle.load( pkl_file )
            pkl_file.close()
        else:
            modules.log( '\n[ERROR] Please run \'trnsys_fmu_install.exe\' or provide the TRNSYS installation directory as optional argument!' )
            modules.sys.exit(5)

    # Check if specified TRNSYS install directory exists.
    if ( False == modules.os.path.isdir( trnsys_install_dir ) ):
        modules.log( '\n[WARNING] TRNSYS install directory does not exist: ', trnsys_install_dir )

    if ( True == verbose ):
        modules.log( '[DEBUG] FMI model identifier: ', fmi_model_identifier )
        modules.log( '[DEBUG] TRNSYS deck file: ', deck_file_name )
        modules.log( '[DEBUG] TRNSYS install directory: ', trnsys_install_dir )
        modules.log( '[DEBUG] Aditional files: ' )
        for file_name in optional_files:
            modules.log( '\t', file_name )

    if ( found_type_6139a == False ): modules.log( '\n[WARNING] No instance of Type6139a found.\n' )
    if ( found_type_6139b == False ): modules.log( '\n[WARNING] No instance of Type6139b found.\n' )

    try:
        fmu_name = generateTrnsysFMU(
            fmi_version,
            fmi_model_identifier,
            deck_file_name,
            trnsys_install_dir,
            fmi_input_vars,
            fmi_output_vars,
            start_values,
            optional_files,
            trnsys_fmu_root_dir,
            verbose,
            litter,
            modules )

        if ( True == verbose ): modules.log( "[DEBUG] FMU created successfully:", fmu_name )

    except Exception as e:
        modules.log( e )
        modules.sys.exit( e.args[0] )

# Main function
if __name__ == "__main__":
    main()
