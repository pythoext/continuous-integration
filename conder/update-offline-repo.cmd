@ECHO OFF
SET distro=%1
SHIFT
SET distrotoken=%1
SHIFT
SET mainrepo=%1
SHIFT

echo Aggiornamento ambiente Conda base
call activate base
call conda update -y -n base conda

echo Creazione ambiente Conda %distro%, puntato alla label %distro%
call conda create -y -n %distro%
call activate %distro%
call conda config --env --add channels http://conda.anaconda.org/prometeia
call conda config --env --add channels https://conda.anaconda.org/t/%distrotoken%/prometeia
call conda config --env --add channels https://conda.anaconda.org/t/%distrotoken%/prometeia/channel/%distro%

echo Installazione nell'ambiente dei pacchtti finali voluti
call conda install -y %1 %2 %3 %4 %5 %6 %7 %8 %9

echo Trasferimento dalla cache ai pacchetti
call conda info --json > envinfo.json
python repackenv.py %mainrepo%

echo Reindicizzazione
SET /p target=<tgfolder.txt
for /D %%d IN (%target%\..\*) DO call conda index %%d

echo Fatto, rimozione ambiente %distro%
call activate base
call conda env remove -y -n %distro%

echo Indici nell'offline channel %distro%:
dir %target%\..\*\repodata.*

echo --- Done! ---