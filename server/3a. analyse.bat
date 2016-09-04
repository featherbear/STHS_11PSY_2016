@echo off
cd /d %~dp0
python "3b. analyse.py">"3c. analyse.txt"
type "3c. analyse.txt"
timeout /t 2 /nobreak>nul
pause>nul