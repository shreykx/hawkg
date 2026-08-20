@echo off
REM Activate the local Python virtual environment
IF EXIST ".\env\Scripts\activate.bat" (
    call .\env\Scripts\activate.bat
) ELSE (
    echo Virtual environment not found. Please create one in the env directory.
)