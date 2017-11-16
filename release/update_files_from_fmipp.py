# ------------------------------------------------------------------------
# Copyright (c) 2015-2017, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file TRNSYS_FMU_LICENSE.txt for details.
# ------------------------------------------------------------------------

##########################################################################
#
# This script copies the source files from a checked-out FMI++ repository.
#
##########################################################################

import sys, os, shutil

def _print( *arg ): print( ' '.join( map( str, arg ) ) )

# Import module with lists of files for release.
from release_file_list import *


def checkFilesExist( file_name_list ):
    # Check if files exist.
    for file_name in file_name_list:
        if ( False == os.path.isfile( file_name ) ):
            _print( file_name, 'not found' )
            return False
    
    return True


if __name__ == "__main__":

    if len( sys.argv ) != 3:
        _print( '\nUsage:\n\n   python update_files_from_fmipp.py <fmipp_repo_dir> <fmipp_revision_id>\n' )
        _print( 'Attention: Be sure to execute this script from subfolder \'release\'\n' )
        sys.exit()
    
    # Path to checked-out FMI++ repository.
    fmipp_repository_dir = sys.argv[1]

    # FMI++ revision ID.
    fmipp_revision_id = sys.argv[2]

    # List of files to be copied.
    file_list = []
    for file_name in files_from_fmipp:
        # Construct list of names.
        file_list.append( fmipp_repository_dir + '\\' + file_name[14:] )

    # Check if files exist.
    if ( False == checkFilesExist( file_list ) ): sys.exit(1)

    # Copy files.
    for file_src, file_dst in zip( file_list, files_from_fmipp ):
        _print( file_src + '\n\t--> ..\\' + file_dst )
        shutil.copyfile( file_src, '..\\' + file_dst )

    fmipp_readme_txt = 'This folder contains a subset of the source code provided by the [FMI++ Library](http://fmipp.sourceforge.net "Link to FMI++ Library") (Git revision ID {0}).'
    fmipp_readme_file = open( '..\\sources\\fmipp\\README.md', 'w' )
    fmipp_readme_file.write( fmipp_readme_txt.format( fmipp_revision_id ) )