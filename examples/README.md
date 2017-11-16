Create the TRNSYS FMU with the following command (from the TRNSYS-FMU test directory):

```
python.exe ..\trnsys_fmu_create.py -v -m TRNSYS_Room_Plant -d plant_room_model.dck room_temperature=20.3
```

Then start Dymola (32-bit), import the FMU and load the Dymola model *trnsys_closed_loop_control_example.mo*.
