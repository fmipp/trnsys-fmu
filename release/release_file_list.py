# ----------------------------------------------------------------------
# Copyright (c) 2015, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file TRNSYS_FMU_LICENSE.txt for details.
# ----------------------------------------------------------------------

########################################################################
#
# This script provides the list of files included into a release of 
# the FMI++ TRNSYS Export Utility.
#
########################################################################

# List of source files (including relative path) that are originally from FMI++.
files_from_fmipp = [
    'sources\\common\\FMIPPConfig.h',
    'sources\\common\\FMIType.h',
    'sources\\common\\fmi_v1.0\\fmi_cs.h',
    'sources\\common\\fmi_v1.0\\fmiModelTypes.h',
    'sources\\export\\functions\\fmiFunctions.cpp',
    'sources\\export\\functions\\fmiFunctions.h',
    'sources\\export\\include\\FMIComponentFrontEnd.h',
    'sources\\export\\include\\FMIComponentFrontEndBase.h'
]

# Additional list of files (including relative path) from the repository that are part of the release.
additional_files = [
    'trnsys_fmu_install.py', # installation script
    'trnsys_fmu_create.py', # script for creating a TRNSYS FMU
    'build.bat', # batch script for FMU compilation
    'license\\BOOST_SOFTWARE_LICENSE.txt',
    'license\\FMIPP_LICENSE.txt',
    'license\\TRNSYS_FMU_LICENSE.txt',
    'proformas\\Type6139a.bmp',
    'proformas\\Type6139a.tmf',
    'proformas\\Type6139b.bmp',
    'proformas\\Type6139b.tmf',
    'test\\plant_room_model.dck',
    'test\\plant_room_model.tpf',
    'test\\README.md',
    'test\\trnsys_closed_loop_control_example.mo'
]

# List of files (without binaries and docs) that are part of the release.
files_for_release = files_from_fmipp + additional_files


# List of binaries that are not provided by the repository (see also README in 'binaries' subfolder).
required_binaries = [
    'binaries\\libboost_date_time-vc100-mt-1_58.lib', # static BOOST date-time library
    'binaries\\libboost_filesystem-vc100-mt-1_58.lib', # static BOOST Filesystem library
    'binaries\\libboost_system-vc100-mt-1_58.lib', # static BOOST System libarary
    'binaries\\libfmipp_fmu_frontend.lib', # static library containing pre-compiled parts of the front end
    'binaries\\Type6139Lib.dll', # implementation of Type6139
]

# The compiled documentation in PDF format (not part of the repository).
doc_file = 'doc\\trnsys-fmu-doc.pdf'

