@ECHO OFF
IF [%2] == [] GOTO usage
SET distrotoken=%1
SET mainrepo=%2
SET applications=pytho ratingpro

ECHO Installing prerequisites...
docker build . -t linuxbuilder
call conda install -y anaconda-client

ECHO Extracting labels to package...
call anaconda -t %distrotoken% label --list 2> labelsout.tmp
findstr /R /C:"pytho_dev_[0-9][0-9]_[0-9][0-9]" labelsout.tmp | sort > labels.tmp
findstr /R /C:"pytho_[0-9][0-9]_[0-9][0-9]" labelsout.tmp | sort >> labels.tmp

FOR /F "tokens=2 delims= " %%G IN (labels.tmp) DO (
    echo ====== Offline packaging %applications% label %%G ========
    docker run -e DONTINDEX=DONTINDEX -e REPO=%mainrepo% -e DISTRO=%%G -e TOKEN=%distrotoken% -e APPLICATIONS="%applications%" -v %mainrepo%:/pythomainrepo --name conderbuilder --rm linuxbuilder
    call update-offline-repo %%G %distrotoken% %mainrepo% %applications%
)

echo ===== DONE ====== 
exit /b 0

:usage
echo "USAGE: mutiplatfom-offline-repo <anaconda token> <offline repository root>"
