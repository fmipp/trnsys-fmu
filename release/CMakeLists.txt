# --------------------------------------------------------------
# Copyright (c) 2015-2017, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file TRNSYS_FMU_LICENSE for details.
# --------------------------------------------------------------

cmake_minimum_required(VERSION 2.8)

#
# This project builds an FMI wrapper for TRNSYS, including the FMI front end
# component library (for the FMU DLL) and the TRNSYS back end component (Type6139).
#
# ATTENTION: When using Visual Studio, be sure to compile in "Release" mode.
#


# Variables to be defined by the user.
set( User_TRNSYS17_PATH "C:/Trnsys17" CACHE FILEPATH "TRNSYS 17 root directory" )


# Define project.
project( FMIPP_TRNSYS_FMU_EXPORT )


# OS- and compiler-specific settings.
if ( NOT DEFINED WIN32 )
   message( FATAL_ERROR "This project requires Windows." )
else ()
   if (CMAKE_SIZEOF_VOID_P EQUAL 8)
      set(FMU_BIN_DIR "win64")
   else ()
      set(FMU_BIN_DIR "win32")
   endif ()
   set(FMU_BIN_EXT ".dll")

   set( PATH_SEPARATOR ";" )
   set( CMAKE_SHARED_LIBRARY_PREFIX "" )
   set( CMAKE_SHARED_MODULE_PREFIX "" )
   add_definitions( -DWIN32 )

   # if ( MINGW )
      # add_definitions( -DMINGW -Wall ) # -O1
      # if ( CMAKE_CXX_COMPILER_VERSION VERSION_LESS "4.7.0" )
         # set( CMAKE_CXX_FLAGS "-std=c++0x" )
      # else ()
         # set( CMAKE_CXX_FLAGS "-std=c++11" )
      # endif ()

      # # Define target output directory.
      # set( CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/../binaries )
      # set( CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/../binaries )
      # set( CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/../binaries )

   # endif ()

   if ( MSVC )
      # disable auto-linking and use cmake's dependency handling
      add_definitions( -DBOOST_ALL_NO_LIB /W3 )

      # Define target output directory.
      foreach( OUTPUTCONFIG ${CMAKE_CONFIGURATION_TYPES} )
         string( TOUPPER ${OUTPUTCONFIG} OUTPUTCONFIG )
         set( CMAKE_RUNTIME_OUTPUT_DIRECTORY_${OUTPUTCONFIG} ${PROJECT_SOURCE_DIR}/../binaries )
         set( CMAKE_LIBRARY_OUTPUT_DIRECTORY_${OUTPUTCONFIG} ${PROJECT_SOURCE_DIR}/../binaries )
         set( CMAKE_ARCHIVE_OUTPUT_DIRECTORY_${OUTPUTCONFIG} ${PROJECT_SOURCE_DIR}/../binaries )
      endforeach( OUTPUTCONFIG CMAKE_CONFIGURATION_TYPES )

      # Add reminder to compile in "Release" mode when using Visual Studio.
      message( "ATTENTION: The TRNSYS wrapper has to be compiled in RELEASE mode!!!" )

   endif ()

endif ()


# Compiler flags.
add_definitions( -DBUILD_FMI_DLL )
add_definitions( -DBOOST_ALL_NO_LIB )


# Boost dependencies here
if ( MSVC )
   set( Boost_USE_STATIC_LIBS ON ) # OFF when using shared Boost libs.
   set( Boost_USE_MULTITHREADED ON )
   set( Boost_USE_STATIC_RUNTIME OFF )
endif ()

find_package( Boost COMPONENTS date_time system filesystem system REQUIRED )

if ( Boost_FOUND )
   include_directories( ${Boost_INCLUDE_DIRS} )
   link_directories( ${Boost_LIBRARY_DIRS} )
endif ()


# FMI back end component (TRNSYS type Type6139).
add_library( Type6139Lib SHARED
   ${PROJECT_SOURCE_DIR}/../sources/type6139/Type6139.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/FMIComponentBackEnd.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/IPCLogger.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/IPCSlaveLogger.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/SHMSlave.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/SHMManager.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/HelperFunctions.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/ScalarVariable.cpp )

# FMI 1.0: front end component library (pre-stage for compiling an FMU DLL according to FMI 1.0).
add_library( libfmipp_fmu_frontend STATIC
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/FMIComponentFrontEndBase.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/FMIComponentFrontEnd.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/IPCLogger.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/IPCMasterLogger.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/SHMMaster.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/SHMManager.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/HelperFunctions.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/ScalarVariable.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/import/base/src/ModelDescription.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/import/base/src/PathFromUrl.cpp
   )

# FMI 2.0: complete FMU DLL.
add_library( fmi2 SHARED
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/functions/fmi_v2.0/fmi2Functions.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/ScalarVariable.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/FMIComponentFrontEndBase.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/FMIComponentFrontEnd.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/IPCLogger.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/IPCMasterLogger.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/SHMMaster.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/SHMManager.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/src/HelperFunctions.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/import/base/src/ModelDescription.cpp
   ${PROJECT_SOURCE_DIR}/../sources/fmipp/import/base/src/PathFromUrl.cpp
   )

# Define compiler flags.
target_compile_definitions( fmi2 PRIVATE
   FRONT_END_TYPE=FMIComponentFrontEnd
   FRONT_END_TYPE_INCLUDE="export/include/FMIComponentFrontEnd.h"
   )

# Include directories.
include_directories( ${PROJECT_SOURCE_DIR}/../sources/type6139 )
include_directories( ${PROJECT_SOURCE_DIR}/../sources/fmipp )
include_directories( ${PROJECT_SOURCE_DIR}/../sources/fmipp/export/functions/fmi_v2.0 )

# Link libraries.
target_link_libraries( Type6139Lib
   Shlwapi
   ${Boost_LIBRARIES}
   ${User_TRNSYS17_PATH}/Exe/TRNDll.lib
   )

target_link_libraries( fmi2
   Shlwapi
   ${Boost_LIBRARIES}
   )
