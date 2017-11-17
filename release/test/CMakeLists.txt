# -------------------------------------------------------------------
# Copyright (c) 2013-2017, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file FMIPP_LICENSE for details.
# -------------------------------------------------------------------

cmake_minimum_required(VERSION 2.8)

#
# This project builds an FMI wrapper for TRNSYS, including the FMI front end
# component (FMU DLL) and the TRNSYS back end component (Type6139).
#
# ATTENTION: When using Visual Studio, be sure to compile in "Release" mode.
#


# Variables to be defined by the user.
set( TRNSYS17_PATH "D:/Trnsys17" CACHE FILEPATH "TRNSYS 17 root directory" )
set( MODEL_IDENTIFIER_FMI1 "Type6139_FMI1_Test" CACHE STRING "FMI 1.0 model identfier" )
set( MODEL_IDENTIFIER_FMI2 "Type6139_FMI2_Test" CACHE STRING "FMI 2.0 model identfier" )


# Define project.
project( Test_TRNSYS_Wrapper )


# Optional builds.
option( BUILD_TEST "Build test application for FMI++ TRNSYS wrapper." ON )


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

   if ( MINGW )
      add_definitions( -DMINGW -Wall ) # -O1
      if ( CMAKE_CXX_COMPILER_VERSION VERSION_LESS "4.7.0" )
         set( CMAKE_CXX_FLAGS "-std=c++0x" )
      else ()
         set( CMAKE_CXX_FLAGS "-std=c++11" )
      endif ()
   endif ()

   if ( MSVC )
      # disable auto-linking and use cmake's dependency handling
      add_definitions( -DBOOST_ALL_NO_LIB /W3 )

      # Add reminder to compile in "Release" mode when using Visual Studio.
      message( "ATTENTION: The TRNSYS wrapper has to be compiled in RELEASE mode!!!" )

   endif ()

endif ()

# Compiler flags.
add_definitions(-DFMU_BIN_DIR="${FMU_BIN_DIR}")
add_definitions(-DFMU_BIN_EXT="${FMU_BIN_EXT}")
add_definitions( -DBUILD_FMI_DLL )
add_definitions( -DBOOST_ALL_NO_LIB )


# Boost dependencies here
if ( MSVC )
   set( Boost_USE_STATIC_LIBS OFF ) # OFF when using shared Boost libs.
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
   ${PROJECT_SOURCE_DIR}/../../sources/type6139/Type6139.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/FMIComponentBackEnd.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/IPCLogger.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/IPCSlaveLogger.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/SHMSlave.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/SHMManager.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/HelperFunctions.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/ScalarVariable.cpp
   )

   
# FMU DLL (FMI 1.0)
add_library( ${MODEL_IDENTIFIER_FMI1} SHARED
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/functions/fmi_v1.0/fmiFunctions.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/FMIComponentFrontEndBase.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/FMIComponentFrontEnd.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/IPCLogger.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/IPCMasterLogger.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/SHMMaster.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/SHMManager.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/HelperFunctions.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/ScalarVariable.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/import/base/src/ModelDescription.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/import/base/src/PathFromUrl.cpp
   )

target_compile_definitions( ${MODEL_IDENTIFIER_FMI1} PRIVATE
   MODEL_IDENTIFIER=${MODEL_IDENTIFIER_FMI1}
   FRONT_END_TYPE=FMIComponentFrontEnd
   FRONT_END_TYPE_INCLUDE="FMIComponentFrontEnd.h"
   )

# FMU DLL (FMI 2.0)
add_library( ${MODEL_IDENTIFIER_FMI2} SHARED
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/functions/fmi_v2.0/fmi2Functions.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/FMIComponentFrontEndBase.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/FMIComponentFrontEnd.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/IPCLogger.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/IPCMasterLogger.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/SHMMaster.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/SHMManager.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/HelperFunctions.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/src/ScalarVariable.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/import/base/src/ModelDescription.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/import/base/src/PathFromUrl.cpp
   )

target_compile_definitions( ${MODEL_IDENTIFIER_FMI2} PRIVATE
   MODEL_IDENTIFIER=${MODEL_IDENTIFIER_FMI2}
   FRONT_END_TYPE=FMIComponentFrontEnd
   FRONT_END_TYPE_INCLUDE="FMIComponentFrontEnd.h"
   )

# Include directories.
include_directories( ${PROJECT_SOURCE_DIR}/../../sources/type6139 )
include_directories( ${PROJECT_SOURCE_DIR}/../../sources/fmipp )
include_directories( ${PROJECT_SOURCE_DIR}/../../sources/fmipp/export/include )


# Link libraries.
target_link_libraries( ${MODEL_IDENTIFIER_FMI1}
   shlwapi
   ${CMAKE_DL_LIBS}
   ${Boost_LIBRARIES}
   )

target_link_libraries( ${MODEL_IDENTIFIER_FMI2}
   shlwapi
   ${CMAKE_DL_LIBS}
   ${Boost_LIBRARIES}
   )

target_link_libraries( Type6139Lib
   shlwapi
   ${Boost_LIBRARIES}
   ${TRNSYS17_PATH}/Exe/TRNDll.lib
   )


# Install Type6139 for TRNSYS.
add_custom_command( TARGET Type6139Lib POST_BUILD
   COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:Type6139Lib> "${TRNSYS17_PATH}/UserLib/ReleaseDLLs"
   COMMAND ${CMAKE_COMMAND} -E make_directory "${TRNSYS17_PATH}/Studio/Proformas/My Components"
   COMMAND ${CMAKE_COMMAND} -E copy ${PROJECT_SOURCE_DIR}/../../proformas/Type6139a.tmf "${TRNSYS17_PATH}/Studio/Proformas/My Components"
   COMMAND ${CMAKE_COMMAND} -E copy ${PROJECT_SOURCE_DIR}/../../proformas/Type6139a.bmp "${TRNSYS17_PATH}/Studio/Proformas/My Components"
   COMMAND ${CMAKE_COMMAND} -E copy ${PROJECT_SOURCE_DIR}/../../proformas/Type6139b.tmf "${TRNSYS17_PATH}/Studio/Proformas/My Components"
   COMMAND ${CMAKE_COMMAND} -E copy ${PROJECT_SOURCE_DIR}/../../proformas/Type6139b.bmp "${TRNSYS17_PATH}/Studio/Proformas/My Components"
   )


if ( WIN32 )
   message( "Adding test: Make sure TRNExe.exe and the Boost libraries have been included in your PATH variable BEFORE you run CMake!!!" )
endif ()

# Find packages needed for unit test framework.
find_package( Boost COMPONENTS system filesystem unit_test_framework REQUIRED )

# Path to XML model description and additional files.
set( FMU_URI_FMI1 "file://${PROJECT_SOURCE_DIR}/Type6139_FMI1_Test" CACHE INTERNAL "" )
set( FMU_RESOURCES_URI_FMI2 "file://${PROJECT_SOURCE_DIR}/Type6139_FMI2_Test/resources" CACHE INTERNAL "" )

# Add executables.
add_executable( testTrnsysFMI1 WIN32
   ${PROJECT_SOURCE_DIR}/testTrnsysFMI1.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/import/base/src/CallbackFunctions.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/import/base/src/LogBuffer.cpp
   )

add_executable( testTrnsysFMI2 WIN32
   ${PROJECT_SOURCE_DIR}/testTrnsysFMI2.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/import/base/src/CallbackFunctions.cpp
   ${PROJECT_SOURCE_DIR}/../../sources/fmipp/import/base/src/LogBuffer.cpp
   )

# Define compiler flags.
target_compile_definitions( testTrnsysFMI1 PRIVATE
    MODEL_IDENTIFIER=${MODEL_IDENTIFIER_FMI1}
    FMU_URI="${FMU_URI_FMI1}"
    )

target_compile_definitions( testTrnsysFMI2 PRIVATE
    MODEL_IDENTIFIER=${MODEL_IDENTIFIER_FMI2}
    FMU_RESOURCES_URI="${FMU_RESOURCES_URI_FMI2}"
    )

# Link executables.
target_link_libraries( testTrnsysFMI1
   ${MODEL_IDENTIFIER_FMI1}
   ${Boost_FILESYSTEM_LIBRARY}
   ${Boost_SYSTEM_LIBRARY}
   ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY}
   )

target_link_libraries( testTrnsysFMI2
   ${MODEL_IDENTIFIER_FMI2}
   ${Boost_FILESYSTEM_LIBRARY}
   ${Boost_SYSTEM_LIBRARY}
   ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY}
   )

# Post build action: copy executables to new subdirectory test.
add_custom_command( TARGET testTrnsysFMI1 POST_BUILD
   COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/test
   COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:testTrnsysFMI1> ${CMAKE_BINARY_DIR}/test
   )

add_custom_command( TARGET testTrnsysFMI2 POST_BUILD
   COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/test
   COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:testTrnsysFMI2> ${CMAKE_BINARY_DIR}/test
   )

# Add test.
enable_testing()
include( CMakeAddTests.txt )
add_test_fmipp( testTrnsysFMI1 )
add_test_fmipp( testTrnsysFMI2 )
