@ECHO OFF
IF [%2] == [] GOTO usage
SET distrotoken=%1
SET mainrepo=%2
SET applications=pytho ratingpro

REM Prerequisites...
REM docker build . -t linuxbuilder
REM call conda install -y anaconda-client

ECHO Extracting labels to package...
call anaconda -t %distrotoken% label --list 2> labelsout.tmp
findstr /R /C:"pytho_dev_[0-9][0-9]_[0-9][0-9]" labelsout.tmp | sort > labels.tmp
findstr /R /C:"pytho_[0-9][0-9]_[0-9][0-9]" labelsout.tmp | sort >> labels.tmp

FOR /F "tokens=2 delims= " %%G IN (labels.tmp) DO (
    echo ====== Offline packaging %applications% label %%G ========
    echo "== NOW WORKING ON DOCKER/LINUX =="
    docker run -e DONTINDEX=DONTINDEX -e DONTREMOVE=DONTREMOVE -e REPO=/pythomainrepo -e DISTRO=%%G -e TOKEN=%distrotoken% -e APPLICATIONS="%applications%" -v "%mainrepo%:/pythomainrepo" --name conderbuilder --rm linuxbuilder
    echo "== NOW BACK TO WINDOWS =="
    call update-offline-repo %%G %distrotoken% %mainrepo% %applications%
)

echo ===== DONE ====== 
exit /b 0

:usage
echo USAGE: mutiplatfom-offline-repo <anaconda token> <offline repository root>
