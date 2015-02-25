MINICONDA_URL="http://repo.continuum.io/miniconda"
MINICONDA_FILE="Miniconda-3.5.5-Linux-x86_64.sh"
wget "${MINICONDA_URL}/${MINICONDA_FILE}"
bash $MINICONDA_FILE -b

export PATH=$HOME/miniconda/bin:$PATH

conda install --yes pip conda-build jinja2 binstar
#conda update --yes conda
conda config --add channels https://conda.binstar.org/prometeia
conda config --add channels https://conda.binstar.org/t/$BINSTAR_TOKEN/prometeia