# Edit the next two lines to create the GUI.
trnsys_fmu_dir = 'D:\\Development\\trnsys-fmu'
python_path = 'D:\\Python34\\Scripts'

import gooey
gooey_root = os.path.dirname(gooey.__file__)
gooey_languages = Tree(os.path.join(gooey_root, 'languages'), prefix = 'gooey/languages')
gooey_images = Tree(os.path.join(gooey_root, 'images'), prefix = 'gooey/images')

a = Analysis( [ os.path.join( trnsys_fmu_dir, 'trnsys_fmu_create_gui.py' ) ],
              pathex = [ python_path ],
              hiddenimports = [],
              hookspath = None,
              runtime_hooks = None,
			  datas = [ ( os.path.join( trnsys_fmu_dir, 'sources', 'logo', 'config_icon.png' ), '.' ) ]
              )

pyz = PYZ( a.pure )

options = [ ( 'u', None, 'OPTION' ) ]

exe = EXE( pyz,
           a.scripts,
           a.binaries,
           a.zipfiles,
           a.datas,
           options,
           gooey_languages,
           gooey_images,
           name = 'trnsys_fmu_create.exe',
           debug = False,
           strip = None,
           upx = True,
           console = False,
           icon = os.path.join( trnsys_fmu_dir, 'sources', 'logo', 'program_icon.ico' )
		   )