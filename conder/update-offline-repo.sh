set -e

USAGE="$0 <cliente> <token cliente> <root del repository offline> <pacchetto1> <...> <pacchettoN>"

export distro=$1
export distrotoken=$2
export mainrepo=$3

echo Aggiornamento e pulizia ambiente Conda base
source activate base
conda update -y -n base conda
conda clean --all -y

echo Creazione ambiente Conda $distro, puntato alla label $distro
conda create -y -n $distro
source activate $distro
conda config --env --add channels http://conda.anaconda.org/prometeia
conda config --env --add channels https://conda.anaconda.org/t/$distrotoken/prometeia
conda config --env --add channels https://conda.anaconda.org/t/$distrotoken/prometeia/channel/$distro

echo "Installazione nell'ambiente dei pacchtti finali voluti: ${@:4}"
conda install --insecure --show-channel-urls -y -n $distro "${@:4}"

echo Trasferimento dalla cache ai pacchetti
conda info --json | tee envinfo.json
python repackenv.py $mainrepo

echo Reindicizzazione
export target=$(cat tgfolder.txt)
conda index $target
conda index $target/../noarch

echo Fatto, rimozione ambiente $distro
source activate base
conda env remove -y -n $distro

if [ -z "$DONTINDEX" ]; then
    echo "Indici nell'offline channel $distro:"
    ls $target/repodata.*  $target/../noarch/repodata.*
else
    echo "WARNING: Indicizzazione di $target e $target/../noarch saltata, provvedere esternamente."
fi
echo Pacchetti rilasciati: $(ls $target | grep '.tar.bz2' | wc -l)

echo --- Done! ---