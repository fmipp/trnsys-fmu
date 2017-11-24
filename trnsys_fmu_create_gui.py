from gooey import Gooey, GooeyParser
import os, sys, argparse

import trnsys_fmu_create

# Retrieve the absolute path to the root directory of the TRNSYS FMU Export Utility.
# This has to be done differently in case the GUI has already been packaged with the help of
# PyInstaller (via sys.executable) or in case this script is run using Python (via __file__).
trnsys_fmu_root_dir = os.path.dirname( sys.executable ) if getattr( sys, 'frozen', False ) else os.path.dirname( __file__ )
trnsys_fmu_root_dir = os.path.abspath( trnsys_fmu_root_dir )

# Retrieve the absolute path to the directory containing the icons.
# This has to be done differently in case the GUI has already been packaged with the help of
# PyInstaller (via sys._MEIPASS) or in case this script is run using Python (via __file__).
gui_image_dir = sys._MEIPASS if getattr( sys, 'frozen', False ) else os.path.join( os.path.dirname( __file__ ), 'sources', 'logo' )
gui_image_dir = os.path.abspath( gui_image_dir )


@Gooey(
    program_name = 'FMI++ TRNSYS FMU Export Utility',
    required_cols = 1, # Number of columns in the "Required" section.
    optional_cols = 1, # Number of columbs in the "Optional" section.
    default_size=( 610, 820 ), # starting size of the GUI
    image_dir = gui_image_dir
    )
def parseCommandLineArgumentsGooey():
    # Create new parser.
    parser = GooeyParser( description = 'This program generates FMUs for Co-Simulation (tool coupling) from TRNSYS deck files.', prog = 'trnsys_fmu_create' )

    # Define optional arguments.
    parser.add_argument( 'extra_arguments', nargs = '*', default = None, help = 'start values and/or extra files (absolute paths or paths relative to current working directory)', metavar = 'Additional arguments' )
    parser.add_argument( '-f', '--fmi_version', choices = [ '1', '2' ], default = '2', help = 'specify FMI version', metavar = 'FMI Version' )
    parser.add_argument( '-v', '--verbose', action = 'store_true', default = True, help = 'turn on log messages', metavar = 'Verbosity' )
    parser.add_argument( '-l', '--litter', action = 'store_true', help = 'do not clean-up intermediate files', metavar = 'Litter' )
    parser.add_argument( '-t', '--trnsys_install_dir', default = None, help = 'path to TRNSYS installation directory (e.g., C:\\Trnsys17)', metavar = 'TRNSYS installation directory', widget = 'DirChooser' )

    # Define mandatory arguments.
    required_args = parser.add_argument_group( 'required arguments' )
    required_args.add_argument( '-m', '--model_id', required = True, help = 'specify FMU model identifier', metavar = 'FMI model identifier' )
    required_args.add_argument( '-d', '--deck_file', required = True, help = 'path to TRNSYS deck file', metavar = 'TRNSYS deck file', widget = 'FileChooser' )

    return parser.parse_args()


if __name__ == '__main__':

    trnsys_fmu_create.main( trnsys_fmu_root_dir, parseCommandLineArgumentsGooey )