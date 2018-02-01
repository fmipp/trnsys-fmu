# -----------------------------------------------------------------
# Copyright (c) 2017-2018, AIT Austrian Institute of Technology GmbH.
# All rights reserved. See file TRNSYS_FMU_LICENSE.txt for details.
# -----------------------------------------------------------------

#
# Collection of helper functions for creating FMU CS for TRNSYS.
#

# Parse command line arguments.
def parseCommandLineArguments( modules ):
    # Create new parser.
    parser = modules.argparse.ArgumentParser( description = 'This script generates FMUs for Co-Simulation (tool coupling) from TRNSYS deck files.', prog = 'trnsys_fmu_create' )

    # Define optional arguments.
    parser.add_argument( '-v', '--verbose', action = 'store_true', help = 'turn on log messages' )
    parser.add_argument( '-l', '--litter', action = 'store_true', help = 'do not clean-up intermediate files' )
    parser.add_argument( '-t', '--trnsys-install-dir', default = None, help = 'path to TRNSYS installation directory (e.g., C:\\Trnsys17)', metavar = 'TRNSYS-INSTALL-DIR' )
    parser.add_argument( '-f', '--fmi-version', choices = [ '1', '2' ], default = '2', help = 'specify FMI version (default: 2)' )

    # Define mandatory arguments.
    required_args = parser.add_argument_group( 'required arguments' )
    required_args.add_argument( '-m', '--model-id', required = True, help = 'specify FMU model identifier', metavar = 'MODEL-ID' )
    required_args.add_argument( '-d', '--deck-file', required = True, help = 'path to TRNSYS deck file', metavar = 'DECK-FILE' )

    # Parse remaining optional arguments (start values, additional files).
    #parser.add_argument( 'extra_arguments', nargs = modules.argparse.REMAINDER, help = 'extra files and/or start values', metavar = 'additional arguments' )
    parser.add_argument( 'extra_arguments', nargs = '*', default = None, help = 'extra files and/or start values', metavar = 'additional arguments' )

    # Add help for additional files.
    parser.add_argument_group( 'additional files', 'Additional files (e.g., for weather data) may be specified as extra arguments. These files will be automatically copied to the resources directory of the FMU.' )

    # Add help for start values.
    parser.add_argument_group( 'start values', 'Specify start values for FMU input variables and parameters.' )

    return parser.parse_args()


# Parse additional command line inputs (start values, additional files).
def parseAdditionalInputs( extra_arguments, verbose, modules ):
    # List of optional files (e.g., weather file)
    optional_files = []

    # Dictionary of start values.
    start_values = {}

    # Retrieve additional files from command line arguments.
    if extra_arguments != None:
        for item in extra_arguments:
            if '=' in item:
                start_value_pair = item.split( '=' )
                varname = start_value_pair[0].strip(' "\n\t')
                value = start_value_pair[1].strip(' "\n\t')
                if ( True == verbose ): modules.log( '[DEBUG] Found start value: ', varname, '=', value )
                start_values[varname] = value;
            elif ( True == modules.os.path.isfile( item ) ): # Check if this is an additional input file.
                optional_files.append( item )
                if ( True == verbose ): modules.log( '[DEBUG] Found additional file: ', item )
            else:
                modules.log( '\n[ERROR] Invalid input argument: ', item )
                modules.sys.exit(7)

    return ( optional_files, start_values )


# Parse TRNSYS deck file.
def parseDeckFile( deck_file_name, verbose, modules ):
    # Lists containing the FMI input and output variable names.
    fmi_input_vars = []
    fmi_output_vars = []

    # Use these flags to check if instances of Type6139a and Type6139b are in the deck file.
    found_type_6139a = False
    found_type_6139b = False

    # Open file.
    deck_file = open( deck_file_name, 'r' )
    while True:
        line = deck_file.readline()
        if not line: break

        if 'FMI input interface' in line:
            found_type_6139a = True

            line = deck_file.readline()
            if ( line == '\n' ):
                modules.log( '\n[ERROR] No FMI input variable names have been specified in special cards tab of Type6139a.' )
                modules.sys.exit(8)

            fmi_input_vars = [ var.strip(' "\n\t') for var in line.split(',') ]

            # In case there is just one variable, check if it is actually the name of an existing file.
            if ( 1 == len( fmi_input_vars ) ):
                if ( modules.os.path.isfile( fmi_input_vars[0] ) ):
                    # Retrieve labels of input variables from file.
                    file_name = fmi_input_vars[0]
                    if ( True == verbose ): modules.log( '\n[DEBUG] Read input variable names from file: ', file_name )
                    fmi_input_vars = []
                    retrieveLabelsFromFile( file_name, fmi_input_vars );

            # Check if input variable names are available.
            if ( 0 == len( fmi_input_vars ) ):
                modules.log( '\n[ERROR] No FMI input variable names have been specified in special cards tab of Type6139a.' )
                modules.sys.exit(8)

            if ( True == verbose ):
                modules.log( '[DEBUG] FMI input parameters:' )
                for var in fmi_input_vars:
                    modules.log( '\t', var )

        elif 'FMI output interface' in line:
            found_type_6139b = True

            line = deck_file.readline()
            if ( line == '\n' ):
                modules.log( '\n[ERROR] No FMI output variable names have been specified in special cards tab of Type6139b.' )
                modules.sys.exit(8)

            fmi_output_vars = [ var.strip(' "\n\t') for var in line.split(',') ]

            # In case there is just one variable, check if it is actually the name of an existing file.
            if ( 1 == len( fmi_output_vars ) ):
                if ( modules.os.path.isfile( fmi_output_vars[0] ) ):
                    # Retrieve labels of output variables from file.
                    file_name = fmi_output_vars[0]
                    if ( True == verbose ): modules.log( '\n[DEBUG] Read output variable names from file: ', file_name )
                    fmi_output_vars = []
                    retrieveLabelsFromFile( file_name, fmi_output_vars );

            # Check if input variable names are available.
            if ( 0 == len( fmi_output_vars ) ):
                modules.log( '\n[ERROR] No FMI output variable names have been specified in special cards tab of Type6139b.' )
                modules.sys.exit(9)

            if ( True == verbose ):
                modules.log( '[DEBUG] FMI output parameters:' )
                for var in fmi_output_vars:
                    modules.log( '\t', var )

    return ( fmi_input_vars, fmi_output_vars, found_type_6139a, found_type_6139b )


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
