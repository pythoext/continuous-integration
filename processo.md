# Processo di CI

## Flusso

1. Push su https://github.com/prometeia/doob.
    1. Integrazione (hook) con travis-ci.com.
1. Avvio di https://travis-ci.com/prometeia/doob.
    1. Clone del relativo branch $TRAVIS_BRANCH di doob.
    1. Checkout subproject https://github.com/prometeia/continuous-integration.git master.
    1. Salvataggio ultimo commento doob sul $TRAVIS_COMMIT in $TRAVIS_COMMIT_MESSAGE.
    1. Verifica se da buildare mediante continuous-integration/check_build_trigger.py (branch tra i censiti, o commento con magicstring "trigger-ci").
    1. Tre esecuzione di continuous-integration/trigger_builds.sh con parametri rispettivamente _gsf\_package_, _datamanagement\_package_ e _pytho\_package_:
        1. Se non da buildare, esce e FINE.
        1. Push sul progetto https://github.com/prometeia/$parametro di $TRAVIS_BRANCH e $TRAVIS_BUILD_NUMBER nei file build_trigger_branch e build_trigger_number
        1. Integrazione con Travis, again. 
1. Avvio di https://travis-ci.com/prometeia/gsf_package.
    1. Clone del relativo branch $TRAVIS_BRANCH di gsf_package.
    1. Checkout subproject https://github.com/prometeia/continuous-integration.git master.
    1. Installazione Miniconda e impostazioni _channel_ pubblici/privati prometeia, mediante continuous-integration\travis\install.sh.
    1. Esecuzione di continuous-integration\update_build_settings.py:
        1. Estrazione in $BRANCH_TO_BUILD e $BUILD_NUMBER di build_trigger_branch e build_trigger_number
        1. Se il branch non è _master_, aggiunta del _channel_ legato al master (convertito in base a continuous-integration.config.BRANCH_TO_CHANNEL o in mancanza omonimo) all'ambiente conda.
    1. Inoculazione di doob (sempre branch $BRANCH_TO_BUILD) nella folder gsf
    1. Recupero dal doop così estratto di "setup_gsf_conda.py", "packages/*" (gsf, gsf_datamanagement, pytho, ratingpro, simviewer) e "commonlib/gsf" (escludendo "sta" e "calibrators"), scartando tutto il resto. La prima è la procedura di build pythonica vera e propria, la seconda metadati di versione e requirement (verranno poi usato solo gsf/version e gsf/requirements.txt), la terza l'insieme dei veri package delle librerie gsf.
    1. Produzione del pacchetto conda (senza recipe) mediante il lancio di "setup_gsf_conda.py". Tutti i package al punto precedenti sono inclusi nel pacchetto, il numero di build è impostato a $BUILD_NUMBER, la versione a quanto in gsf/version, i requirement quanto in gsf/requirements.txt. La procedura preventivamente importa numpy e Cython.Build.cythonize, installando con pip eventuali requirement mancanti (why?).
    1. Trasferimento dei pacchetti conda prodotti nella cartella corrente, tramite "continuos-integration/move-conda-package.py", e poi upload su Anaconda Cloud degli stessi, tramite  "continuos-integration/binstar-push.py". Il canale di upload è di nuovo decodificato dal branch, a sua volta letto dal file "build_trigger_branch". Dovrebbe trattarsi sempre di un solo pacchetto, nel caso gsf, con naming del tipo _gsf-4.1.2-np110py27\_2025.tar.bz2_.
1. Come al punto precedente, in parallelo, per _datamanagement\_package_ e _pytho\_package_: cambiano solo versioni/requirement e package inclusi; i secondi sono cablati