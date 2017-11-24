# Creating FMUs for TRNSYS with the help of the graphical user interface

Start *trnsys_fmu_create.exe* in the root directory of the FMI++ TRNSYS FMU Export Utility by double-clicking it.
Provide the following inputs_

* FMI model identifier: *TRNSYS_Room_Plant*
* TRNSYS deck file: click *Browse* and select file *plant_room_model.dck* from the examples folder
* Additional arguments: *examples\extra_file.dat room_temperature=20.3 control_signal=0*

Then click the *Start* button to create the FMU.


# Creating FMUs for TRNSYS with the help of Python scripts

Or create the TRNSYS FMU from the command line with the following command (from the examples directory):
```
python.exe ..\trnsys_fmu_create.py -v -m TRNSYS_Room_Plant -d plant_room_model.dck extra_file.dat room_temperature=20.3 control_signal=0
```


# Testing the FMU

After creating the FMU, start Dymola 2018 (32-bit).
First import the FMU, then load the Dymola model *trnsys_closed_loop_control_example.mo* and run the example.
