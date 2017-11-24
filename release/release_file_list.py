# ----------------------------------------------------------------------
# Copyright (c) 2015-2017, AIT Austrian Institute of Technology GmbH.
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
    'sources\\fmipp\\common\\FMIPPConfig.h',
    'sources\\fmipp\\common\\FMIVariableType.h',
    'sources\\fmipp\\common\\FMUType.h',
    'sources\\fmipp\\common\\fmi_v1.0\\fmiModelTypes.h',
    'sources\\fmipp\\common\\fmi_v1.0\\fmi_cs.h',
    'sources\\fmipp\\common\\fmi_v1.0\\fmi_me.h',
    'sources\\fmipp\\common\\fmi_v2.0\\fmi2ModelTypes.h',
    'sources\\fmipp\\common\\fmi_v2.0\\fmi_2.h',
    'sources\\fmipp\\export\\functions\\fmi_v1.0\\fmiFunctions.cpp',
    'sources\\fmipp\\export\\functions\\fmi_v1.0\\fmiFunctions.h',
    'sources\\fmipp\\export\\functions\\fmi_v2.0\\fmi2Functions.cpp',
    'sources\\fmipp\\export\\functions\\fmi_v2.0\\fmi2Functions.h',
    'sources\\fmipp\\export\\include\\BackEndApplicationBase.h',
    'sources\\fmipp\\export\\include\\FMIComponentBackEnd.h',
    'sources\\fmipp\\export\\include\\FMIComponentFrontEnd.h',
    'sources\\fmipp\\export\\include\\FMIComponentFrontEndBase.h',
    'sources\\fmipp\\export\\include\\HelperFunctions.h',
    'sources\\fmipp\\export\\include\\IPCLogger.h',
    'sources\\fmipp\\export\\include\\IPCMaster.h',
    'sources\\fmipp\\export\\include\\IPCMasterLogger.h',
    'sources\\fmipp\\export\\include\\IPCSlave.h',
    'sources\\fmipp\\export\\include\\IPCSlaveLogger.h',
    'sources\\fmipp\\export\\include\\SHMManager.h',
    'sources\\fmipp\\export\\include\\SHMMaster.h',
    'sources\\fmipp\\export\\include\\SHMSlave.h',
    'sources\\fmipp\\export\\include\\ScalarVariable.h',
    'sources\\fmipp\\export\\src\\BackEndApplicationBase.cpp',
    'sources\\fmipp\\export\\src\\FMIComponentBackEnd.cpp',
    'sources\\fmipp\\export\\src\\FMIComponentFrontEnd.cpp',
    'sources\\fmipp\\export\\src\\FMIComponentFrontEndBase.cpp',
    'sources\\fmipp\\export\\src\\HelperFunctions.cpp',
    'sources\\fmipp\\export\\src\\IPCLogger.cpp',
    'sources\\fmipp\\export\\src\\IPCMasterLogger.cpp',
    'sources\\fmipp\\export\\src\\IPCSlaveLogger.cpp',
    'sources\\fmipp\\export\\src\\SHMManager.cpp',
    'sources\\fmipp\\export\\src\\SHMMaster.cpp',
    'sources\\fmipp\\export\\src\\SHMSlave.cpp',
    'sources\\fmipp\\export\\src\\ScalarVariable.cpp',
    'sources\\fmipp\\import\\base\\include\\ModelDescription.h',
    'sources\\fmipp\\import\\base\\include\\PathFromUrl.h',
    'sources\\fmipp\\import\\base\\src\\ModelDescription.cpp',
    'sources\\fmipp\\import\\base\\src\\PathFromUrl.cpp',
    "sources\\fmipp\\import\\base\\include\\CallbackFunctions.h", # only for testing
    "sources\\fmipp\\import\\base\\include\\LogBuffer.h", # only for testing
    "sources\\fmipp\\import\\base\\src\\CallbackFunctions.cpp", # only for testing
    "sources\\fmipp\\import\\base\\src\\LogBuffer.cpp", # only for testing
]

# Source code for the FM++ TRNSYS Export Utility.
source_code = [
    'sources\\type6139\\Type6139.cpp',
    'sources\\type6139\\TRNSYS.h',
]

# Additional list of files (including relative path) from the repository that are part of the release.
additional_files = [
    'trnsys_fmu_install.exe', # installation program
    'trnsys_fmu_install.py', # installation script
    'trnsys_fmu_create.exe', # program for creating a TRNSYS FMU
    'trnsys_fmu_create.py', # script for creating a TRNSYS FMU
    'binaries\\README.md',
    'examples\\extra_file.dat',
    'examples\\plant_room_model.dck',
    'examples\\plant_room_model.tpf',
    'examples\\README.md',
    'examples\\trnsys_closed_loop_control_example.mo',
    'license\\BOOST_SOFTWARE_LICENSE.txt',
    'license\\FMIPP_LICENSE.txt',
    'license\\TRNSYS_FMU_LICENSE.txt',
    'scripts\\fmi1.py',
    'scripts\\fmi1_build.bat',
    'scripts\\fmi2.py',
    'scripts\\generate_fmu.py',
    'scripts\\utils.py',
    'sources\\proformas\\Type6139a.bmp',
    'sources\\proformas\\Type6139a.tmf',
    'sources\\proformas\\Type6139b.bmp',
    'sources\\proformas\\Type6139b.tmf',
]

# List of files (without binaries and docs) that are part of the release.
files_for_release = files_from_fmipp + source_code + additional_files


# List of binaries that are not provided by the repository (see also README in 'binaries' subfolder).
required_binaries = [
    'binaries\\fmi2.dll', # pre-compiled shared library (for FMI 2.0 only)
    'binaries\\libboost_date_time-vc120-mt-1_58.lib', # static BOOST date-time library
    'binaries\\libboost_filesystem-vc120-mt-1_58.lib', # static BOOST Filesystem library
    'binaries\\libboost_system-vc120-mt-1_58.lib', # static BOOST System libarary
    'binaries\\libfmipp_fmu_frontend.lib', # static library containing pre-compiled parts of the front end (for FMI 1.0 only)
    'binaries\\Type6139Lib.dll', # implementation of Type6139
]

# The compiled documentation in PDF format (not part of the repository).
doc_file = 'doc\\trnsys-fmu-doc.pdf'

