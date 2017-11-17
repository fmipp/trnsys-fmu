// -------------------------------------------------------------------
// Copyright (c) 2013-2017, AIT Austrian Institute of Technology GmbH.
// All rights reserved. See file FMIPP_LICENSE for details.
// -------------------------------------------------------------------

#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE testTrnsysFMU

/// \file testTrnsysFMU.cpp

#include <boost/test/unit_test.hpp>
#include <boost/filesystem.hpp>
#include <cmath>

#include "export/functions/fmi_v2.0/fmi2Functions.h"
#include "import/base/include/CallbackFunctions.h"


#ifdef _MSC_VER
#pragma comment( linker, "/SUBSYSTEM:CONSOLE" )
#pragma comment( linker, "/ENTRY:mainCRTStartup" )
#endif

static fmi2CallbackFunctions invalidFunctions = { 0, 0, 0, 0 };


static fmi2CallbackFunctions functions =
{ callback2::verboseLogger, callback2::allocateMemory, callback2::freeMemory, callback2::stepFinished };


BOOST_AUTO_TEST_CASE( test_trnsys_fmu )
{
	fmi2Status status = fmi2Fatal;
	fmi2Boolean loggingOn = fmi2True;
	fmi2Component trnsysSlave;

	fmiReal time = 0.;
	fmiReal delta = 450.; // equals 1/8th of an hour.
	fmiReal eps = 1e-8;

	// Try with invalid set of callback functions.
	trnsysSlave = fmi2Instantiate( "Type6139_FMI2_Test", fmi2CoSimulation,
		"{TRNSYS17-TYPE-6139-TEST-FMI200000000}", FMU_RESOURCES_URI,
		&invalidFunctions, fmiFalse, loggingOn );
	BOOST_REQUIRE_MESSAGE( 0 == trnsysSlave, "fmi2Instantiate(...) should have failed." );

	trnsysSlave = fmi2Instantiate( "Type6139_FMI2_Test", fmi2CoSimulation,
		"{TRNSYS17-TYPE-6139-TEST-FMI200000000}", FMU_RESOURCES_URI,
		&functions, fmiFalse, loggingOn );
	BOOST_REQUIRE_MESSAGE( 0 != trnsysSlave, "fmi2Instantiate(...) failed." );

	status = fmi2SetupExperiment( trnsysSlave, fmi2False, 0., time, fmi2False, 0. );
	BOOST_REQUIRE_MESSAGE( fmi2OK == status, "fmi2SetupExperiment(...) failed." );

	status = fmi2EnterInitializationMode( trnsysSlave );
	BOOST_REQUIRE_MESSAGE( fmi2OK == status, "fmi2EnterInitializationMode(...) failed." );

	status = fmi2ExitInitializationMode( trnsysSlave );
	BOOST_REQUIRE_MESSAGE( fmi2OK == status, "fmi2ExitInitializationMode(...) failed." );

	fmi2Real FMI_in;
	fmi2ValueReference FMI_in_ref = 1;
	status = fmi2GetReal( trnsysSlave, &FMI_in_ref, 1, &FMI_in );
	BOOST_REQUIRE_MESSAGE( fmi2OK == status, "fmi2GetReal(...) failed." );

	fmi2Real FMI_out;
	fmi2ValueReference FMI_out_ref = 2;

	while ( time < 100.*3600. ) {

		status = fmi2DoStep( trnsysSlave, time, delta, fmiTrue );
		BOOST_REQUIRE_MESSAGE( fmiOK == status, "fmi2DoStep(...) failed." );

		time += delta;

		status = fmi2GetReal( trnsysSlave, &FMI_out_ref, 1, &FMI_out );
		BOOST_REQUIRE_MESSAGE( fmi2OK == status, "fmiGetReal(...) failed." );

		if ( ( static_cast<int>( time ) - 36000 )%72000 == 0 ) BOOST_CHECK_CLOSE( FMI_out, 1.0, eps );

		if ( FMI_out < 0. ) FMI_in *= -1.;

		status = fmi2SetReal( trnsysSlave, &FMI_in_ref, 1, &FMI_in );
		BOOST_REQUIRE_MESSAGE( fmi2OK == status, "fmi2SetReal(...) failed." );
	}

	status = fmi2Terminate( trnsysSlave );
	BOOST_REQUIRE_MESSAGE( fmi2OK == status, "fmi2TerminateSlave(...) failed." );

	fmi2FreeInstance( trnsysSlave );
}
