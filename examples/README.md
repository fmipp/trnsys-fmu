Create the TRNSYS FMU with the following command (from the TRNSYS-FMU example directory):

```
python.exe ..\trnsys_fmu_create.py -v -m TRNSYS_Room_Plant -d plant_room_model.dck extra_file.dat room_temperature=20.3 control_signal=0
```

Then start Dymola 2018 (32-bit), import the FMU and load the Dymola model *trnsys_closed_loop_control_example.mo* to run the example.
