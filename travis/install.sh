MINICONDA_URL="http://repo.continuum.io/miniconda"
MINICONDA_FILE="Miniconda-latest-Linux-x86_64.sh"
wget "${MINICONDA_URL}/${MINICONDA_FILE}"
bash $MINICONDA_FILE -b

export PATH=$HOME/miniconda/bin:$PATH

conda install --yes pip jinja2 anaconda-client conda-build==1.16
conda update --yes conda
conda config --add channels https://conda.anaconda.org/prometeia
conda config --add channels https://conda.anaconda.org/t/$BINSTAR_TOKEN/prometeia