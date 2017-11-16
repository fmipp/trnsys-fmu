# -----------------------------------------------------------------
# -----------------------------------------------------------------
# Copyright (c) 2017, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file TRNSYS_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------

### Python 2
import sys, os, shutil, time, getpass, uuid, urlparse, urllib, getopt, pickle, subprocess, glob
def _print( *arg ): print ' '.join( map( str, arg ) )

### Python 3
# import sys, os, shutil, time, getpass, uuid, urllib.parse, urllib, getopt, pickle, subprocess, glob
# def _print( *arg ): print( ' '.join( map( str, arg ) ) )


def generateTrnsysFMU(
                fmi_model_identifier,
                deck_file_name,
                trnsys_install_dir,
                fmi_input_vars,
                fmi_output_vars,
                start_values,
                optional_files,
                trnsys_fmu_root_dir ):
        """Generate an FMU for TRNSYS.

    Keyword arguments:
        fmi_model_identifier -- FMI model identfier for FMU (string)
        deck_file_name -- name of deck file (string)
        trnsys_install_dir -- TRNSYS installation directory (string)
        fmi_input_vars -- definition of input variable names (list of strings)
        fmi_output_vars -- definition of output variable names (list of strings)
        start_values -- definition of start values (map of strings to strings)
        optional_files -- definition of additional files (list of strings)
        trnsys_fmu_root_dir -- path root dir of TRNSYS FMU Export Utility (string)
        """
        
        # Template string for XML model description header.
        model_description_header = '<?xml version="1.0" encoding="UTF-8"?>\n<fmiModelDescription fmiVersion="1.0" modelName="__MODEL_NAME__" modelIdentifier="__MODEL_IDENTIFIER__" description="TRNSYS FMI CS export" generationTool="FMI++ TRNSYS Export Utility" generationDateAndTime="__DATE_AND_TIME__" variableNamingConvention="flat" numberOfContinuousStates="0" numberOfEventIndicators="0" author="__USER__" guid="{__GUID__}">\n\t<VendorAnnotations>\n\t\t<Tool name="trnexe">\n\t\t\t<Executable preArguments="" postArguments="/n" executableURI="__TRNEXE_URI__"/>\n\t\t</Tool>\n\t</VendorAnnotations>\n\t<ModelVariables>\n'

        # Template string for XML model description of scalar variables.
        scalar_variable_node = '\t\t<ScalarVariable name="__VAR_NAME__" valueReference="__VAL_REF__" variability="continuous" causality="__CAUSALITY__">\n\t\t\t<Real__START_VALUE__/>\n\t\t</ScalarVariable>\n'

        # Template string for XML model description footer.
        model_description_footer = '\t</ModelVariables>\n\t<Implementation>\n\t\t<CoSimulation_Tool>\n\t\t\t<Capabilities canHandleVariableCommunicationStepSize="false" canHandleEvents="true" canRejectSteps="false" canInterpolateInputs="false" maxOutputDerivativeOrder="0" canRunAsynchronuously="false" canBeInstantiatedOnlyOncePerProcess="false" canNotUseMemoryManagementFunctions="true"/>\n\t\t\t<Model entryPoint="fmu://__DECK_FILE_NAME__" manualStart="false" type="application/x-trnexe">__ADDITIONAL_FILES__</Model>\n\t\t</CoSimulation_Tool>\n\t</Implementation>\n</fmiModelDescription>'

        # Create new XML model description file.
        model_description_name = 'modelDescription.xml'
        model_description = open( model_description_name, 'w' )

        #
        # Replace template arguments in header.
        #

        # FMI model identifier.
        model_description_header = model_description_header.replace( '__MODEL_IDENTIFIER__', fmi_model_identifier )

        # Model name.
        fmi_model_name = os.path.basename( deck_file_name ).split( '.' )[0] # Deck file name with extension.
        model_description_header = model_description_header.replace( '__MODEL_NAME__', fmi_model_name )

        # Creation date and time.
        model_description_header = model_description_header.replace( '__DATE_AND_TIME__', time.strftime( "%Y-%m-%dT%H:%M:%S" ) )

        # Author name.
        model_description_header = model_description_header.replace( '__USER__', getpass.getuser() )

        # GUID.
        model_description_header = model_description_header.replace( '__GUID__', str( uuid.uuid1() ) )

        # URI of TRNSYS main executable (TRNExe.exe).
        trnsys_exe_uri = urlparse.urljoin( 'file:', urllib.pathname2url( trnsys_install_dir ) ) + '/exe/trnexe.exe'
        model_description_header = model_description_header.replace( '__TRNEXE_URI__', trnsys_exe_uri )

        # Write header to file.
        model_description.write( model_description_header );

        #
        # Add scalar variable description.
        #
        input_val_ref = 1 # Value references for inputs start with 1.
        for var in fmi_input_vars:
                scalar_variable_description = scalar_variable_node
                scalar_variable_description = scalar_variable_description.replace( '__VAR_NAME__', var )
                scalar_variable_description = scalar_variable_description.replace( '__CAUSALITY__', "input" )
                scalar_variable_description = scalar_variable_description.replace( '__VAL_REF__', str( input_val_ref ) )
                if var in start_values:
                        start_value_description = ' start=\"' + start_values[var] + '\"'
                        scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', start_value_description )
                        if ( True == verbose ): _print( '[DEBUG] Added start value to model description: ', var, '=', start_values[var] )
                else:
                        scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', '' )
                input_val_ref += 1
                # Write scalar variable description to file.
                model_description.write( scalar_variable_description );

        # Value references for outputs start with 1001 (except there are already input value references with corresponding values).
        output_val_ref = 1001 if ( input_val_ref < 1001 ) else input_val_ref
        for var in fmi_output_vars:
                scalar_variable_description = scalar_variable_node
                scalar_variable_description = scalar_variable_description.replace( '__VAR_NAME__', var )
                scalar_variable_description = scalar_variable_description.replace( '__CAUSALITY__', "output" )
                scalar_variable_description = scalar_variable_description.replace( '__VAL_REF__', str( output_val_ref ) )
                if var in start_values:
                        start_value_description = ' start=\"' + start_values[var] + '\"'
                        scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', start_value_description )
                        if ( True == verbose ): _print( '[DEBUG] Added start value to model description: ', var, '=', start_values[var] )
                else:
                        scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', '' )
                output_val_ref += 1
                # Write scalar variable description to file.
                model_description.write( scalar_variable_description );

        #
        # Replace template arguments in footer.
        #

        # Input deck file.
        model_description_footer = model_description_footer.replace( '__DECK_FILE_NAME__', os.path.basename( deck_file_name ) )

        # Additional input files.
        if ( 0 == len( optional_files ) ):
                model_description_footer = model_description_footer.replace( '__ADDITIONAL_FILES__', '' )
        else:
                additional_files_description = ''
                for file_name in optional_files:
                        additional_files_description += '\n\t\t\t\t<File file=\"fmu://' + os.path.basename( file_name ) + '\"/>'
                        if ( True == verbose ): _print( '[DEBUG] Added additional file to model description: ', os.path.basename( file_name ) )
                additional_files_description += '\n\t\t\t'
                model_description_footer = model_description_footer.replace( '__ADDITIONAL_FILES__', additional_files_description )


        # Write footer to file.
        model_description.write( model_description_footer );

        # Close file.
        model_description.close()

        # Check if model description is XML compliant.
        #import xml.etree.ElementTree as ET
        #tree = ET.parse( 'model_description.xml' )

        # FMU shared library name.
        fmu_shared_library_name = fmi_model_identifier + '.dll'

        # Check if batch file for build process exists.
        build_process_batch_file = trnsys_fmu_root_dir + '\\build.bat'
        if ( False == os.path.isfile( build_process_batch_file ) ):
                _print( '\n[ERROR] Could not find file: ', build_process_batch_file )
                raise Exception( 8 )

        # Compile FMU shared library.
        for file_name in glob.glob( fmi_model_identifier + '.*' ):
                if not ( ( ".dck" in file_name ) or ( ".tpf" in file_name ) ): os.remove( file_name ) # Do not accidentaly remove the deck file!
        if ( True == os.path.isfile( 'fmiFunctions.obj' ) ): os.remove( 'fmiFunctions.obj' )
        build_process = subprocess.Popen( [build_process_batch_file, fmi_model_identifier] )
        stdout, stderr = build_process.communicate()

        # Check if batch script has executed successfully.
        if ( False == os.path.isfile( fmu_shared_library_name ) ):
		_print( '\n[ERROR] Not able to create shared library: ', fmu_shared_library_name )
		raise Exception( 16 )

        # Check if working directory for FMU creation already exists.
        if ( True == os.path.isdir( fmi_model_identifier ) ):
                shutil.rmtree( fmi_model_identifier, False )

        # Working directory path for the FMU DLL.
        binaries_dir = os.path.join( fmi_model_identifier, 'binaries', 'win32' )

        # Create working directory (incl. sub-directories) for FMU creation.
        os.makedirs( binaries_dir )

        # Copy all files to working directory.
        shutil.copy( model_description_name, fmi_model_identifier ) # XML model description.
        shutil.copy( deck_file_name, fmi_model_identifier ) # TRNSYS deck file.
        for file_name in optional_files: # Additional files.
                shutil.copy( file_name, fmi_model_identifier )
        shutil.copy( fmu_shared_library_name, binaries_dir ) # FMU DLL.


        # Create ZIP archive.
        if ( True == os.path.isfile( fmi_model_identifier + '.zip' ) ):
                os.remove( fmi_model_identifier + '.zip' )
        shutil.make_archive( fmi_model_identifier, 'zip', fmi_model_identifier )

        # Finally, create the FMU!!!
        if ( True == os.path.isfile( fmi_model_identifier + '.fmu' ) ):
                os.remove( fmi_model_identifier + '.fmu' )
        os.rename( fmi_model_identifier + '.zip', fmi_model_identifier + '.fmu' )

        # Clean up.
        if ( False == litter ):
                os.remove( model_description_name )
                os.remove( 'build.log' )
                os.remove( 'fmiFunctions.obj' )
                shutil.rmtree( fmi_model_identifier, False )
                for file_name in glob.glob( fmi_model_identifier + '.*' ):
                        if not ( ( ".fmu" in file_name ) or ( ".dck" in file_name ) or ( ".tpf" in file_name ) ): os.remove( file_name )


# Helper function. Retrieve labels from file. The file is expected to
# have one entry per line, comment lines start with a semicolon (;).
def retrieveLabelsFromFile( file_name, labels ):
        input_file = open( file_name, 'r' ) # Open the file.
        while True:
                line = input_file.readline() # Read next line.
                if not line: break # End of file.

                line = line.strip(' "\'\n\t') # Strip all leading and trailing whitespaces etc.

                semicolon_position = line.find( ';' ) # Check for comments.
                if ( 0 == semicolon_position ):
                        continue # Comment line.
                elif ( -1 != semicolon_position ):
                        line = line[0:semicolon_position].strip(' "\'\n\t') # Remove comment from line

                if 0 != len( line ):
                        labels.append( line ) # Append line to list of labels.
                        

# Helper function
def usage():
        """Print the usage of this script when used as main program."""
        _print( '\nABOUT:' )
        _print( 'This script generates FMUs for Co-Simulation (tool coupling) from TRNSYS deck files' )
        _print( '\nUSAGE:' )
        _print( 'python trnsys_fmu_create.py [-h] [-v] [-t trnsys_install_dir] -m model_id -d deck_file [additional_file_1 ... additional_file_N] [var1=start_val1 ... varN=start_valN]' )
        _print( '\nREQUIRED ARGUMENTS:' )
        _print( '-m, --model-id=\t\tspecify FMU model identifier' )
        _print( '-d, --deck-file=\tpath to TRNSYS deck file' )
        _print( '\nOPTIONAL ARGUMENTS:' )
        _print( '-h, --help\t\tdisplay this information' )
        _print( '-v, --verbose\t\tturn on log messages' )
        _print( '-l, --litter\t\tdo not clean-up intermediate files' )
        _print( '-t, --trnsys-install-dir=\tpath to TRNSYS installation directory (e.g., C:\\Trnsys17)' )
        _print( '\nAdditional files may be specified (e.g., weather data) that will be automatically copied to the FMU.' )
        _print( '\nStart values for variables may be defined. For instance, to set variable with name \"var1\" to value 12.34, specifiy \"var1=12.34\" in the command line as optional argument.' )


# Main function
if __name__ == "__main__":

        # FMI model identifier.
        fmi_model_identifier = None

        # TRNSYS deck file.
        deck_file_name = None

        # Set TRNSYS install dir.
        trnsys_install_dir = None

        # List of optional files (e.g., weather file)
        optional_files = []

        # Dictionary of start values.
        start_values = {}

        # Relative or absolute path to TRNSYS FMU Export Utility.
        trnsys_fmu_root_dir = os.path.dirname( sys.argv[0] ) if len( os.path.dirname( sys.argv[0] ) ) else '.'

        # Verbose flag.
        verbose = False

        # Litter flag.
        litter = False

        # Parse command line arguments.
        try:
                options_definition_short = "vhlm:d:t:"
                options_definition_long = [ "verbose", "help", "litter", "model-id=", 'deck-file=', 'trnsys-install-dir=' ]
                options, extra = getopt.getopt( sys.argv[1:], options_definition_short, options_definition_long )
        except getopt.GetoptError as err:
                _print( str( err ) )
                usage()
                sys.exit(1)

        # Parse options.
        for opt, arg in options:
                if opt in ( '-h', '--help' ):
                        usage()
                        sys.exit()
                elif opt in ( '-m', '--model-id' ):
                        fmi_model_identifier = arg
                elif opt in ( '-d', '--deck-file' ):
                        deck_file_name = arg
                elif opt in ( '-t', '--trnsys-install-dir' ):
                        trnsys_install_dir = arg
                elif opt in ( '-v', '--verbose' ):
                        verbose = True
                elif opt in ( '-l', '--litter' ):
                        litter = True

        # Check if FMI model identifier has been specified.
        if ( None == fmi_model_identifier ):
                _print( '\n[ERROR] No FMU model identifier specified!' )
                usage()
                sys.exit(2)

        # Check if TRNSYS deck file has been specified.
        if ( None == deck_file_name ):
                _print( '\n[ERROR] No TRNSYS deck file specified!' )
                usage()
                sys.exit(3)
        elif ( False == os.path.isfile( deck_file_name ) ): # Check if specified deck file is valid.
                _print( '\n[ERROR] Invalid TRNSYS deck file: ', deck_file_name )
                usage()
                sys.exit(4)
        
        # No TRNSYS install directory provided -> read from file (created by script 'trnsys_fmu_install.py').
        if ( None == trnsys_install_dir ):
                pkl_file_name = trnsys_fmu_root_dir + '\\trnsys_fmu_install.pkl'
                if ( True == os.path.isfile( pkl_file_name ) ):
                        pkl_file = open( pkl_file_name, 'rb' )
                        trnsys_install_dir = pickle.load( pkl_file )
                        pkl_file.close()
                else:
                        _print( '\n[ERROR] Please re-run script \'trnsys_fmu_install.py\' or provide TRNSYS install directory via command line option -t (--trnsys-install-dir)!' )
                        usage()
                        sys.exit(5)

        # Check if specified TRNSYS install directory exists.
        if ( False == os.path.isdir( trnsys_install_dir ) ):
                _print( '\n[WARNING] TRNSYS install directory does not exist: ', trnsys_install_dir )
        
        # Retrieve additional files from command line arguments.
        for item in extra:
                if "=" in item:
                        start_value_pair = item.split( '=' )
                        varname = start_value_pair[0].strip(' "\n\t')
                        value = start_value_pair[1].strip(' "\n\t')
                        if ( True == verbose ): _print( '[DEBUG] Found start value: ', varname, '=', value )
                        start_values[varname] = value;
                elif ( True == os.path.isfile( item ) ): # Check if this is an additional input file.
                        optional_files.append( item )
                        if ( True == verbose ): _print( '[DEBUG] Found additional file: ', item )
                else:
                        _print( '\n[ERROR] Invalid input argument: ', item )
                        usage()
                        sys.exit(7)

        if ( True == verbose ):
                _print( '[DEBUG] FMI model identifier: ', fmi_model_identifier )
                _print( '[DEBUG] TRNSYS deck file: ', deck_file_name )
                _print( '[DEBUG] TRNSYS install directory: ', trnsys_install_dir )
                _print( '[DEBUG] Aditional files: ' )
                for file_name in optional_files:
                        _print( '\t', file_name )

        # Lists containing the FMI input and output variable names.
        fmi_input_vars = []
        fmi_output_vars = []

        # Use these flags to check if instances of Type6139a and Type6139b are in the deck file.
        found_type_6139a = False
        found_type_6139b = False

        # Parse TRNSYS deck file to retrieve FMI input and output variable names.
        deck_file = open( deck_file_name, 'r' )
        while True:
                line = deck_file.readline()
                if not line: break

                if 'FMI input interface' in line:
                        found_type_6139a = True

                        line = deck_file.readline()
                        if ( line == '\n' ):
                                _print( '\n[ERROR] No FMI input variable names have been specified in special cards tab of Type6139a.' )
                                sys.exit(8)

                        fmi_input_vars = [ var.strip(' "\n\t') for var in line.split(',') ]

                        # In case there is just one variable, check if it is actually the name of an existing file.
                        if ( 1 == len( fmi_input_vars ) ):
                                if ( os.path.isfile( fmi_input_vars[0] ) ):
                                     # Retrieve labels of input variables from file.
                                     file_name = fmi_input_vars[0]
                                     if ( True == verbose ): _print( '\n[DEBUG] Read input variable names from file: ', file_name )
                                     fmi_input_vars = []
                                     retrieveLabelsFromFile( file_name, fmi_input_vars );

                        # Check if input variable names are available.
                        if ( 0 == len( fmi_input_vars ) ):
                                _print( '\n[ERROR] No FMI input variable names have been specified in special cards tab of Type6139a.' )
                                sys.exit(8)

                        if ( True == verbose ):
                                _print( '[DEBUG] FMI input parameters:' )
                                for var in fmi_input_vars:
                                        _print( '\t', var )

                elif 'FMI output interface' in line:
                        found_type_6139b = True

                        line = deck_file.readline()
                        if ( line == '\n' ):
                                _print( '\n[ERROR] No FMI output variable names have been specified in special cards tab of Type6139b.' )
                                sys.exit(8)

                        fmi_output_vars = [ var.strip(' "\n\t') for var in line.split(',') ]

                        # In case there is just one variable, check if it is actually the name of an existing file.
                        if ( 1 == len( fmi_output_vars ) ):
                                if ( os.path.isfile( fmi_output_vars[0] ) ):
                                     # Retrieve labels of output variables from file.
                                     file_name = fmi_output_vars[0]
                                     if ( True == verbose ): _print( '\n[DEBUG] Read output variable names from file: ', file_name )
                                     fmi_output_vars = []
                                     retrieveLabelsFromFile( file_name, fmi_output_vars );

                        # Check if input variable names are available.
                        if ( 0 == len( fmi_output_vars ) ):
                                _print( '\n[ERROR] No FMI output variable names have been specified in special cards tab of Type6139b.' )
                                sys.exit(9)

                        if ( True == verbose ):
                                _print( '[DEBUG] FMI output parameters:' )
                                for var in fmi_output_vars:
                                        _print( '\t', var )

        if ( found_type_6139a == False ): _print( '\n[WARNING] No instance of Type6139a found.\n' )
        if ( found_type_6139b == False ): _print( '\n[WARNING] No instance of Type6139b found.\n' )

        try:
                generateTrnsysFMU(
                        fmi_model_identifier,
                        deck_file_name,
                        trnsys_install_dir,
                        fmi_input_vars,
                        fmi_output_vars,
                        start_values,
                        optional_files,
                        trnsys_fmu_root_dir )
        except Exception as e:
                sys.exit( e.args[0] )
        
        if ( True == verbose ): _print( "[DEBUG] FMU created successfully!" )
