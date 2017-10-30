# --------------------------------------------------------------
# Copyright (c) 2015, AIT Austrian Institute of Technology GmbH.
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
set( User_FMIPP_SOURCE_DIR "D:/Development/fmipp" CACHE PATH "FMI++ source directory" )
set( User_TRNSYS17_PATH "D:/Trnsys17" CACHE FILEPATH "TRNSYS 17 root directory" )

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

find_package( Boost COMPONENTS date_time system filesystem REQUIRED )

if ( Boost_FOUND )
   include_directories( ${Boost_INCLUDE_DIRS} )
   link_directories( ${Boost_LIBRARY_DIRS} )
endif ()


# FMI back end component (TRNSYS type Type6139).
add_library( Type6139Lib SHARED
             ${User_FMIPP_SOURCE_DIR}/export/tools/trnsys17/Type6139/Type6139.cpp
             ${User_FMIPP_SOURCE_DIR}/export/src/FMIComponentBackEnd.cpp
             ${User_FMIPP_SOURCE_DIR}/export/src/IPCLogger.cpp
             ${User_FMIPP_SOURCE_DIR}/export/src/IPCSlaveLogger.cpp
             ${User_FMIPP_SOURCE_DIR}/export/src/SHMSlave.cpp
             ${User_FMIPP_SOURCE_DIR}/export/src/SHMManager.cpp
             ${User_FMIPP_SOURCE_DIR}/export/src/HelperFunctions.cpp
             ${User_FMIPP_SOURCE_DIR}/export/src/ScalarVariable.cpp )

# FMI front end component library (for FMU DLL).
add_library( libfmipp_fmu_frontend STATIC
             ${User_FMIPP_SOURCE_DIR}/export/src/FMIComponentFrontEndBase.cpp
             ${User_FMIPP_SOURCE_DIR}/export/src/FMIComponentFrontEnd.cpp
             ${User_FMIPP_SOURCE_DIR}/export/src/IPCLogger.cpp
             ${User_FMIPP_SOURCE_DIR}/export/src/IPCMasterLogger.cpp
             ${User_FMIPP_SOURCE_DIR}/export/src/SHMMaster.cpp
             ${User_FMIPP_SOURCE_DIR}/export/src/SHMManager.cpp
             ${User_FMIPP_SOURCE_DIR}/export/src/HelperFunctions.cpp
             ${User_FMIPP_SOURCE_DIR}/export/src/ScalarVariable.cpp
             ${User_FMIPP_SOURCE_DIR}/import/base/src/ModelDescription.cpp
             ${User_FMIPP_SOURCE_DIR}/import/base/src/PathFromUrl.cpp )


# Include directories.
include_directories( ${User_FMIPP_SOURCE_DIR}/export/tools/trnsys17/Type6139 )
include_directories( ${User_FMIPP_SOURCE_DIR} )
include_directories( ${User_FMIPP_SOURCE_DIR}/export/include )

# Link libraries.
target_link_libraries( Type6139Lib
                       Shlwapi
					   ${Boost_LIBRARIES}
                       ${User_TRNSYS17_PATH}/Exe/TRNDll.lib )
