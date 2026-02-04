@echo off
cd /d C:\Users\ryovo\Documents\Projects\study-tracker

set /p SUBJECT=What are you studying? 
set /p DEVICE=Device (pc/phone): 

py study.py start "%SUBJECT%" %DEVICE%
pause
