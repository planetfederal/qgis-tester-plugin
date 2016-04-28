To run unittest from CLI i't necessary to setup some QGIS env vars.
Below a configuration example when using a compiled QGIS

export QGIS_PREFIX="<where is located qgis source code>"
export QGIS_PREFIX_PATH=${QGIS_PREFIX}"/build/output"
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${QGIS_PREFIX_PATH}"/lib"
export PYTHONPATH=${QGIS_PREFIX_PATH}"/python":${PYTHONPATH}

to run all tests:
$> python run_all_tests.py

to run a single suite of tests eg for Plugin.py source:
$> python test_plugin.py
