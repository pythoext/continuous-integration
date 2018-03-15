# Distribuzione offline

## Intro
Si tratta di produrre un repository locale Anaconda per ogni _label_ cliente, da fornire per le installazioni offline. Tecnicamente si tratta di creare dei [custom channel](https://conda.io/docs/user-guide/tasks/create-custom-channels.html).


## Prerequisiti
- MiniConda (choco install miniconda)
- Package conda-build (conda install conda-build)

## Creazione repository per label

Ogni _custom channel_ prevede cartelle separate per architettura. Nel nostro caso è necessaria _noarch_, più _win-64_ o _linux-64_ a seconda del sito finale.

La procedura è così articolata:

1. Aggiornamento dell'ambiente Conda _base_
2. Creazione di un ambiente Conda ad hoc, omonimo alla label per cui vogliamo pacchettizzare.
3. Attivazione di quest'ultimo e puntamento ai tre repository Anaconda Cloud di Pytho: Prometeia pubblico e privato, label privata.
4. Installazione del pacchetto finale richiesto (ad esempio, _ratingpro_) sull'ambiente.
5. A questo punto sulle varie cache locali ci saranno i pacchetti che son stati usati. Si salvano su json le configurazioni dell'ambiente e si aziona lo script _repackenv.py_ indicando dove è posizionato il repository globale offline target. Il resto dei parametri viene estratto dal json, locazione delle cache incluse, per cui la procedura in automatico rileva e copia tutto e solo il necessario, lasciando su un file di testo le coordinate della folder target dell'architettura.
6. Recuperata la folder, si reindicizza quella e la gemella vuota _noarch_.
7. Rimozione dell'ambiente ad hoc, non più necessario. 

Come esempio, prendiamo la label [halkbank](https://anaconda.org/prometeia/repo/files?type=any&label=halkbank), procedura in CMD Windows essendo tale il target.

    REM Parametri
    SET distro="halkbank"
    SET distrotoken="xxx"
    SET distropackages="ratingpro"
    SET mainrepo="C:\MAINPYTHOREPO"

    echo Creazione ambiente Conda di riferimento, puntato alla label voluta
    conda create -y -n %distro%
    activate %distro%
    conda config --env --add channels http://conda.anaconda.org/prometeia
    conda config --env --add channels https://conda.anaconda.org/t/%distrotoken%/prometeia
    conda config --env --add channels https://conda.anaconda.org/t/%distrotoken%/prometeia/channel/%distro%

    echo Installazione nell'ambiente dei pacchtti finali voluti
    conda install -y %distropackages%

    echo Trasferimento dalla cache ai pacchetti
    conda info --json > envinfo.json
    python repackenv.py %mainrepo%

    echo Reindicizzazione
    SET /p target=<tgfolder.txt
    conda index %target%
    conda index %target%\..\noarch

## Script windows di creazione

 La procedura rigenera ogni volta da zero il pacchetto di distribuzione, per rimuovere così eventuali zombie.

    update-offline-repo <cliente> <token cliente> <root del repository offline> <pacchetto1> <...> <pacchettoN>

Esempio:

    update-offline-repo halkbank xx-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx c:\tmp\megarpo ratingpro pytho

## Utilizzo del repository

Nella macchina target, dopo aver installato MiniConda, andrà copiata l'intera folder sopra preparata, poi creato un ambiente Conda ad hoc, configurato offline e infine aggiunta la folder copiata come channel locale. 

    REM Parametri
    SET ambiente="halbank-test"
    SET distrofolder="X:\path\to\local\repo"

    echo Creazione e configurazione ambiente Conda
    conda create -y -n %ambiente%
    activate %ambiente%
    conda config --env --set offline yes
    conda config --env --add channels file:///$env:distrofolder
    
A questo punto ogni installazione da tale ambiente Conda opererà direttamente e unicamente da quanto nel custom channel. Ad esempio, per l'installazione di _PYTHO_ e _RatingPro_:

    activate %ambiente%
    conda install pytho ratingpro

Per gli aggiornamenti, sarà sufficiente riallineare il contenuto del repository locale del custom channel con quanto nella relativa folder sul master centrale, ad esempio via _rsync_ o _robocopy_; dopodiché, nell'effettivo ambiente conda basterà la solita _conda update_.

## Test halkbank

    REM Aggiornamento repository offline halkbank
    update-offline-repo halkbank xx-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx G:\PYTHO-offline-repo ratingpro

    REM Creazione ambiente di test e installazione offline di ratingpro
    robocopy /MIR G:\PYTHO-offline-repo\halkbank c:\tmp\halkbankofflinerepo

    conda create -y -n testhalkbank
    activate testhalkbank
    conda config --env --set offline yes
    conda config --env --add channels file:///c:\tmp\halkbankofflinerepo
    conda info

             active environment : testhalkbank
            active env location : C:\Users\brandolinid\AppData\Local\Continuum\miniconda2\envs\testhalkbank
                   shell level : 2
              user config file : C:\Users\brandolinid\.condarc
        populated config files : C:\Users\brandolinid\AppData\Local\Continuum\miniconda2\.condarc
                                C:\Users\brandolinid\AppData\Local\Continuum\miniconda2\envs\testhalkbank\.condarc
                conda version : 4.4.11
          conda-build version : not installed
               python version : 2.7.14.final.0
             base environment : C:\Users\brandolinid\AppData\Local\Continuum\miniconda2  (writable)
                 channel URLs : file:///c:/tmp/halkbankofflinerepo/win-64
                                file:///c:/tmp/halkbankofflinerepo/noarch
                                https://repo.continuum.io/pkgs/main/win-64  (offline)
                                https://repo.continuum.io/pkgs/main/noarch  (offline)
                                https://repo.continuum.io/pkgs/free/win-64  (offline)
                                https://repo.continuum.io/pkgs/free/noarch  (offline)
                                https://repo.continuum.io/pkgs/r/win-64  (offline)
                                https://repo.continuum.io/pkgs/r/noarch  (offline)
                                https://repo.continuum.io/pkgs/pro/win-64  (offline)
                                https://repo.continuum.io/pkgs/pro/noarch  (offline)
                                https://repo.continuum.io/pkgs/msys2/win-64  (offline)
                                https://repo.continuum.io/pkgs/msys2/noarch  (offline)
                package cache : C:\Users\brandolinid\AppData\Local\Continuum\miniconda2\pkgs
                                C:\Users\brandolinid\AppData\Local\conda\conda\pkgs
             envs directories : C:\Users\brandolinid\AppData\Local\Continuum\miniconda2\envs
                                C:\Users\brandolinid\AppData\Local\conda\conda\envs
                                C:\Users\brandolinid\.conda\envs
                     platform : win-64
                   user-agent : conda/4.4.11 requests/2.18.4 CPython/2.7.14 Windows/10 Windows/10.0.16299
                administrator : False
                   netrc file : None
                 offline mode : True

    conda install -y --offline ratingpro --dry-run
    conda install -y --offline ratingpro