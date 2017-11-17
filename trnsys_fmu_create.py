# -----------------------------------------------------------------
# Copyright (c) 2017, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file TRNSYS_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------

### Python 2
# import sys, os, shutil, time, getpass, uuid, urlparse, urllib, getopt, pickle, subprocess, glob
# def _print( *arg ): print ' '.join( map( str, arg ) )

### Python 3
import sys, os, shutil, time, getpass, uuid, getopt, pickle, subprocess, glob
import urllib.parse as urlparse
import urllib.request as urllib
def _print( *arg ): print( ' '.join( map( str, arg ) ) )

### Import helper functions for specific FMI versions.
from scripts.fmi1 import *
from scripts.fmi2 import *


def generateTrnsysFMU(
    fmi_version,
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

    # Retrieve templates for different parts of XML model description according to FMI version.
    ( model_description_header, scalar_variable_node, model_description_footer ) = getModelDescriptionTemplates( fmi_version )

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

    # Define a string to collect all scalar variable definitions.
    model_description_scalars = ''

    # Add scalar input variables description. Value references for inputs start with 1.
    input_val_ref = 1
    for var in fmi_input_vars:
        scalar_variable_description = scalar_variable_node
        scalar_variable_description = scalar_variable_description.replace( '__VAR_NAME__', var )
        scalar_variable_description = scalar_variable_description.replace( '__CAUSALITY__', "input" )
        scalar_variable_description = scalar_variable_description.replace( '__VAL_REF__', str( input_val_ref ) )
        scalar_variable_description = scalar_variable_description.replace( '__INITIAL__', '' )
        if var in start_values:
            start_value_description = ' start=\"' + start_values[var] + '\"'
            scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', start_value_description )
            if ( True == verbose ): _print( '[DEBUG] Added start value to model description: ', var, '=', start_values[var] )
        else:
            scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', '' )
        input_val_ref += 1
        # Write scalar variable description to file.
        model_description_scalars += scalar_variable_description;

    # Add scalar input variables description. Value references for outputs start with 1001 (except there are already input value references with corresponding values).
    output_val_ref = 1001 if ( input_val_ref < 1001 ) else input_val_ref
    for var in fmi_output_vars:
        scalar_variable_description = scalar_variable_node
        scalar_variable_description = scalar_variable_description.replace( '__VAR_NAME__', var )
        scalar_variable_description = scalar_variable_description.replace( '__CAUSALITY__', "output" )
        scalar_variable_description = scalar_variable_description.replace( '__VAL_REF__', str( output_val_ref ) )
        if var in start_values:
            start_value_description = ' start=\"' + start_values[var] + '\"'
            scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', start_value_description )
            scalar_variable_description = scalar_variable_description.replace( '__INITIAL__', 'initial="exact"' )
            if ( True == verbose ): _print( '[DEBUG] Added start value to model description: ', var, '=', start_values[var] )
        else:
            scalar_variable_description = scalar_variable_description.replace( '__START_VALUE__', '' )
            scalar_variable_description = scalar_variable_description.replace( '__INITIAL__', '' )
        output_val_ref += 1
        # Write scalar variable description to file.
        model_description_scalars += scalar_variable_description;

    # Input deck file.
    ( model_description_header, model_description_footer ) = \
        addDeckFileToModelDescription( deck_file_name, model_description_header, model_description_footer, fmi_version )

    # Optional files.
    ( model_description_header, model_description_footer ) = \
        addOptionalFilesToModelDescription( model_description_header, model_description_footer, optional_files, fmi_version )

    # Create new XML model description file.
    model_description_name = 'modelDescription.xml'
    model_description = open( model_description_name, 'w' )
    model_description.write( model_description_header );
    model_description.write( model_description_scalars );
    model_description.write( model_description_footer );
    model_description.close()

    # Create FMU shared library.
    fmu_shared_library_name = createSharedLibrary( fmi_model_identifier, trnsys_fmu_root_dir, fmi_version )

    # Check if working directory for FMU creation already exists.
    if ( True == os.path.isdir( fmi_model_identifier ) ):
        shutil.rmtree( fmi_model_identifier, False )

    # Working directory path for the FMU DLL.
    binaries_dir = os.path.join( fmi_model_identifier, 'binaries', 'win32' )

    # Create working directory (incl. sub-directories) for FMU creation.
    os.makedirs( binaries_dir )

    # Resources directory path.
    resources_dir = os.path.join( fmi_model_identifier, 'resources' )

    # Create resources directory for FMU creation.
    os.makedirs( resources_dir )

    # Copy all files to working directory.
    shutil.copy( model_description_name, fmi_model_identifier ) # XML model description.
    shutil.copy( deck_file_name, resources_dir ) # TRNSYS deck file.
    for file_name in optional_files: # Additional files.
        shutil.copy( file_name, resources_dir )
    shutil.copy( fmu_shared_library_name, binaries_dir ) # FMU DLL.


    # Create ZIP archive.
    if ( True == os.path.isfile( fmi_model_identifier + '.zip' ) ):
        os.remove( fmi_model_identifier + '.zip' )
    shutil.make_archive( fmi_model_identifier, 'zip', fmi_model_identifier )

    # Finally, create the FMU!!!
    fmu_file_name = fmi_model_identifier + '.fmu'
    if ( True == os.path.isfile( fmu_file_name ) ):
        os.remove( fmu_file_name )
    os.rename( fmi_model_identifier + '.zip', fmu_file_name )

    # Clean up.
    if ( False == litter ):
        for fn in [ model_description_name, 'build.log', 'fmiFunctions.obj' ]:
            os.remove( fn ) if os.path.isfile( fn ) else None
        shutil.rmtree( fmi_model_identifier, False )
        for file_name in glob.glob( fmi_model_identifier + '.*' ):
            if not ( ( ".fmu" in file_name ) or ( ".dck" in file_name ) or ( ".tpf" in file_name ) ): os.remove( file_name )

    # Return name of created FMU.
    return fmu_file_name


# Get templates for the XML model description depending on the FMI version.
def getModelDescriptionTemplates( fmi_version ):
    if ( '1' == fmi_version ): # FMI 1.0
       return fmi1GetModelDescriptionTemplates()
    elif ( '2' == fmi_version ): # FMI 2.0
        return fmi2GetModelDescriptionTemplates()


# Add deck file as entry point to XML model description.
def addDeckFileToModelDescription( deck_file_name, header, footer, fmi_version ):
    if ( '1' == fmi_version ): # FMI 1.0
        return fmi1AddDeckFileToModelDescription( deck_file_name, header, footer, os )
    elif ( '2' == fmi_version ): # FMI 2.0
        return fmi2AddDeckFileToModelDescription( deck_file_name, header, footer, os )


# Add optional files to XML model description.
def addOptionalFilesToModelDescription( header, footer, optional_files, fmi_version ):
    if ( '1' == fmi_version ):
        return fmi1AddOptionalFilesToModelDescription( optional_files, header, footer, verbose, _print, os )
    if ( '2' == fmi_version ):
        return fmi2AddOptionalFilesToModelDescription( optional_files, header, footer, verbose, _print, os )


# Create DLL for FMU.
def createSharedLibrary( fmi_model_identifier, trnsys_fmu_root_dir, fmi_version ):
    if ( '1' == fmi_version ):
        return fmi1CreateSharedLibrary( fmi_model_identifier, trnsys_fmu_root_dir, glob, subprocess, os )
    if ( '2' == fmi_version ):
        return fmi2CreateSharedLibrary( fmi_model_identifier, trnsys_fmu_root_dir, shutil, os )


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
    _print( '-f, --fmi-version=\tspecify FMI version (allowed values: 1 or 2, default: 2)' )
    _print( '-h, --help\t\tdisplay this information' )
    _print( '-v, --verbose\t\tturn on log messages' )
    _print( '-l, --litter\t\tdo not clean-up intermediate files' )
    _print( '-t, --trnsys-install-dir=\tpath to TRNSYS installation directory (e.g., C:\\Trnsys17)' )
    _print( '\nAdditional files may be specified (e.g., weather data) that will be automatically copied to the FMU.' )
    _print( '\nStart values for variables may be defined. For instance, to set variable with name \"var1\" to value 12.34, specifiy \"var1=12.34\" in the command line as optional argument.' )


# Main function
if __name__ == "__main__":

    # FMI version
    fmi_version = None

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
        options_definition_short = "hvlm:d:t:f:"
        options_definition_long = [ "help", "verbose", "litter", "model-id=", 'deck-file=', 'trnsys-install-dir=', 'fmi-version=' ]
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
        elif opt in ( '-v', '--verbose' ):
            verbose = True
        elif opt in ( '-l', '--litter' ):
            litter = True
        elif opt in ( '-m', '--model-id' ):
            fmi_model_identifier = arg
        elif opt in ( '-d', '--deck-file' ):
            deck_file_name = arg
        elif opt in ( '-t', '--trnsys-install-dir' ):
            trnsys_install_dir = arg
        elif opt in ( '-f', '--fmi-version' ):
            if ( ( arg != '1' ) and ( arg != '2' ) ):
                _print( '\n[ERROR] Invalid input for FMI version. Allowed inputs: 1 or 2.' )
                usage()
                sys.exit(2)
            fmi_version = arg

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

    # Check if FMI version has been specified.
    if ( None == fmi_version ):
        fmi_version = '2'
        if ( True == verbose ):
            _print( '[DEBUG] Using FMI version 2 (default)' )
    elif ( True == verbose ):
        _print( '[DEBUG] Using FMI version', fmi_version )

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
        fmu_name = generateTrnsysFMU(
            fmi_version,
            fmi_model_identifier,
            deck_file_name,
            trnsys_install_dir,
            fmi_input_vars,
            fmi_output_vars,
            start_values,
            optional_files,
            trnsys_fmu_root_dir )

        if ( True == verbose ): _print( "[DEBUG] FMU created successfully:", fmu_name )

    except Exception as e:
        _print( e )
        sys.exit( e.args[0] )
