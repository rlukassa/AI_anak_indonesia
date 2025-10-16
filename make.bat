@echo off
REM Usage: make build | make run | make stop

SET IMAGE=myproject
SET NAME=myproject
SET PORT=8000

IF "%1"=="build" GOTO build
IF "%1"=="run" GOTO run
IF "%1"=="stop" GOTO stop

ECHO Commands:
ECHO   make build   - Build Docker image
ECHO   make run     - Run container
ECHO   make stop    - Stop existing container
GOTO end

:build
ECHO Building Docker image...
docker build -t %IMAGE% .
GOTO end

:run
ECHO Running container...
docker run --rm -it --name %NAME% -p %PORT%:%PORT% %IMAGE%
GOTO end

:stop
ECHO Stopping container "%NAME%" if running...
docker stop %NAME%
GOTO end

:end
