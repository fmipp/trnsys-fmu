within ;
model trnsys_closed_loop_control_example
  "Simple example of closed-loop control model with TRNSYS FMU."
  TRNSYS_Room_Plant_fmu tRNSYS_Room_Plant_fmu(
    fmi_loggingOn=true,
    fmi_StopTime=43200,
    fmi_NumberOfSteps=48,
    fmi_CommunicationStepSize=900,
    fmi_forceShutDownAtStopTime=true)
    annotation (Placement(transformation(extent={{-70,10},{-50,30}})));
  Modelica.Blocks.Sources.Constant const(k=21.0)
    annotation (Placement(transformation(extent={{-70,-30},{-50,-10}})));
  Modelica.Blocks.Math.Add add(k1=-1)
    annotation (Placement(transformation(extent={{-30,-10},{-10,10}})));
  Modelica.Blocks.Logical.Hysteresis hysteresis(uLow=-0.5, uHigh=0.5)
    annotation (Placement(transformation(extent={{10,-10},{30,10}})));
  Modelica.Blocks.Math.BooleanToReal booleanToReal
    annotation (Placement(transformation(extent={{50,-10},{70,10}})));
equation
  connect(const.y, add.u2) annotation (Line(points={{-49,-20},{-40,-20},{-40,-6},
          {-32,-6}}, color={0,0,127}));
  connect(add.y, hysteresis.u)
    annotation (Line(points={{-9,0},{8,0}}, color={0,0,127}));
  connect(hysteresis.y, booleanToReal.u)
    annotation (Line(points={{31,0},{31,0},{48,0}}, color={255,0,255}));
  connect(booleanToReal.y, tRNSYS_Room_Plant_fmu.control_0signal) annotation (
      Line(points={{71,0},{80,0},{80,-40},{-80,-40},{-80,20},{-70.4,20}}, color
        ={0,0,127}));
  connect(tRNSYS_Room_Plant_fmu.room_0temperature, add.u1) annotation (Line(
        points={{-48,23.4},{-40,23.4},{-40,6},{-32,6}}, color={0,0,127}));
  annotation (
    uses(Modelica(version="3.2.1")),
    Diagram(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},{
            100,100}})),
    experiment(StopTime=43200, Interval=900));
end trnsys_closed_loop_control_example;
