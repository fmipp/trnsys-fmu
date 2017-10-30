@ECHO OFF

REM -----------------------------------------------------------------
REM Copyright (c) 2015, AIT Austrian Institute of Technology GmbH.
REM All rights reserved. See file TRNSYS_FMU_LICENSE.txt for details.
REM -----------------------------------------------------------------

REM Check number of input arguments.
SET ARG_COUNT=0
FOR %%I IN (%*) DO SET /A ARG_COUNT+=1
IF %ARG_COUNT% NEQ 1 (
  ECHO USAGE: build.bat ^<fmi-model-identifier^>
  GOTO:EOF
)

REM Define FMU model identifier.
SET MODEL_IDENTFIER=%1

REM Define log file name.
SET LOG_FILE=build.log

REM Delete debug file if it already exists.
IF EXIST %LOG_FILE% del /F %LOG_FILE%

REM Setup command line tools from Visual Studio 2010.
CALL "%VS100COMNTOOLS%vsvars32.bat" >> %LOG_FILE%

REM Define FMI export functions implementation file.
SET FMI_FUNCTIONS_IMPLEMENTATION="%~DP0\sources\export\functions\fmiFunctions.cpp"

REM Define include flags for CL.
SET INCLUDE_FLAGS=/I"%~DP0\sources" /I"%~DP0\sources\export\include"

REM Define library path for CL.
SET LIBRARY_PATH="%~DP0\binaries"

REM Compile FMI front end component with correct model identifier.
CL /c %INCLUDE_FLAGS% /nologo /W3 /WX- /O2 /Ob2 /Oy- /D WIN32 /D _WINDOWS /D NDEBUG /D MODEL_IDENTIFIER=%MODEL_IDENTFIER% /D FRONT_END_TYPE=FMIComponentFrontEnd /D "FRONT_END_TYPE_INCLUDE=\"FMIComponentFrontEnd.h\"" /D _WINDLL /D _MBCS /Gm- /EHsc /MD /GS /fp:precise /Zc:wchar_t /Zc:forScope /GR /Gd /TP /analyze- /errorReport:queue %FMI_FUNCTIONS_IMPLEMENTATION% >> %LOG_FILE%

REM Link final DLL for FMU.
LINK /ERRORREPORT:QUEUE /OUT:"%MODEL_IDENTFIER%.dll" /INCREMENTAL:NO /NOLOGO /LIBPATH:%LIBRARY_PATH% kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib Shlwapi.lib libboost_date_time-vc100-mt-1_58.lib libboost_filesystem-vc100-mt-1_58.lib libboost_system-vc100-mt-1_58.lib libfmipp_fmu_frontend.lib /SUBSYSTEM:CONSOLE /TLBID:1 /DYNAMICBASE /NXCOMPAT /IMPLIB:"%MODEL_IDENTFIER%.lib" /MACHINE:X86 /DLL fmiFunctions.obj /machine:X86 >> %LOG_FILE%
