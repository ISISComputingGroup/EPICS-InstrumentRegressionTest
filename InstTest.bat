@echo off
pushd c:\EPICS
call config_env.bat
popd
inst_test.py