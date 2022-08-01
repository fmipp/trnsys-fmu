# The FMI++ TRNSYS FMU Export Utility

This open-source project provides a stand-alone tool for exporting FMUs for Co-Simulation from [TRNSYS 17](https://www.trnsys.com) models.
The current release supports FMI version 1.0 and 2.0.

Instructions on installation and usage are given in the documentation, which is provided as part of the download.
This documentation also contains a tutorial on how to export a TRNSYS model as FMU for co-simulation and how to link it with a simple controller implemented in Modelica.

The tool is based on code from the [FMI++ library](https://github.com/fmipp/fmipp).

Features:

+ exports [TRNSYS 17](https://www.trnsys.com) models as FMUs for co-simulation (tool coupling)
+ generated FMUs are compliant with FMI Version 1.0 and 2.0
+ requires an installed version of [TRNSYS 17](https://www.trnsys.com) at runtime
+ FMUs can be generated with the help of a graphical user interface or using Python scripts
