@echo off

set BACKUP_PATH=%CD%
cd /d %~dp0
cd ../

call python -m unittest discover

cd %BACKUP_PATH%
