@echo off
rem INSTALL.BAT - Easy installer for Python modules on Windows

rem version 0.02 2009-02-27 Philippe Lagadec - http://www.decalage.info

rem License: 
rem This file install.bat can freely used, modified and redistributed, as 
rem long as credit to the author is kept intact. Please send any feedback,
rem issues or improvements to decalage at laposte.net.

rem CHANGELOG:
rem 2007-09-04 v0.01 PL: - first version, for Python 2.3 to 2.5
rem 2009-02-27 v0.02 PL: - added support for Python 2.6

rem install python 2.7

rem cd %~dp0\install_files
echo installing from: %~dp0install_files
msiexec.exe /i install_files\python-2.7.12.msi /QN /L*V "C:\Temp\msilog.log"
goto check

rem 1) test if python.exe is in the path:

rem python.exe --version >NUL 2>&1
rem if errorlevel 1 goto notpath
rem echo Python.exe found in the path.
rem python setup.py install
rem if errorlevel 1 goto error
rem goto end
rem :NOTPATH

rem 2) test for usual python.exe paths:

REM Python 2.7: 
:CHECK
c:\python27\python.exe --version >NUL 2>&1
if errorlevel 1 goto error
echo Python.exe found in C:\Python27
rem c:\python27\python.exe setup.py install
rem if errorlevel 1 goto error
goto pip 

:PIP
echo installing pip...
c:\python27\python.exe install_files\get-pip.py
echo upgrading pip...
c:\python27\Scripts\pip.exe install --upgrade pip
goto libs

:LIBS
echo installing libs
c:\python27\Scripts\pip.exe install install_files\scipy-0.18.0-cp27-cp27m-win32.whl
c:\python27\Scripts\pip.exe install install_files\numpy-1.11.1mkl-cp27-cp27m-win32.whl
c:\python27\Scripts\pip.exe install install_files\Pillow-3.3.1-cp27-cp27m-win32.whl
c:\python27\Scripts\pip.exe install -r install_files\libraries.txt
goto done

:done
echo
echo
echo You can know generate heat maps! 
echo Simply make a csv file name input.csv to keep track of makes and misses
echo The format must be: Position Number, Made, Attempt
echo The floor position cooresponding to the postion numbers can be found in floor_postions.png
echo An example input.csv should be included in your download.
echo 
echo Once you have entered the makes and misses, double click GenerateHeatMaps.py
echo Wait a minute, and boom: a nice heat map
goto end

:ERROR
echo.
echo Something went wrong :( Have you used Python before? Try manually installing python 2.7, then run again.
REM pause

:END
pause
