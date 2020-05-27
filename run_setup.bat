python -m pip install --user --upgrade setuptools wheel

@echo off
echo.
echo.
echo.
echo are you sure you want to create a new build? y-yes , otherwise no
echo.
set /p "answer=____"
if "%answer%"=="Y" python setup.py sdist bdist_wheel
pause