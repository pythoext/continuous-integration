@ECHO OFF
IF [%4] == [] GOTO usage
SET distro=%1
SET distrotoken=%2
SET mainrepo=%3

docker build . -t linuxbuilder
docker run -e DONTINDEX=DONTINDEX -e REPO=%mainrepo% -e DISTRO=%distro% -e TOKEN=%distrotoken% -e APPLICATIONS="%4 %5 %6 %7 %8 %9" -v %mainrepo%:/pythomainrepo --name conderbuilder --rm linuxbuilder

call update-offline-repo %1 %2 %3 %4 %5 %6 %7 %8 %9

exit /b 0

:usage
echo "USAGE: mutiplatfom-offline-repo <label> <token accesso> <root del repository offline> <pacchetto1> <...> <pacchettoN>"