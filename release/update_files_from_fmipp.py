# ------------------------------------------------------------------------
# Copyright (c) 2015, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file TRNSYS_FMU_LICENSE.txt for details.
# ------------------------------------------------------------------------

##########################################################################
#
# This script copies the source files from a checked-out FMI++ repository.
#
##########################################################################

import sys, os, shutil


# Import module with lists of files for release.
from release_file_list import *


def checkFilesExist( file_name_list ):
    # Check if files exist.
    for file_name in file_name_list:
        if ( False == os.path.isfile( file_name ) ):
            print file_name, 'not found'
            return False
    
    return True


if __name__ == "__main__":

    if len( sys.argv ) != 2:
        print 'Usage:\n\tpython update_files_from_fmipp.py <fmipp_repository_dir>\n'
        print 'Attention: Be sure to execute this script from subfolder \'release\'\n'
        sys.exit()
    
    # Path to checked-out FMI++ repository.
    fmipp_repository_dir = sys.argv[1]

    # List of files to be copied.
    file_list = []
    for file_name in files_from_fmipp:
        # Construct list of names.
        file_list.append( fmipp_repository_dir + '\\' + file_name[8:] )

    # Check if files exist.
    if ( False == checkFilesExist( file_list ) ): sys.exit(1)

    # Copy files.
    for file_src, file_dst in zip( file_list, files_from_fmipp ):
        print file_src + '\n\t--> ..\\' + file_dst
        shutil.copyfile( file_src, '..\\' + file_dst )
        

    
