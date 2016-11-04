MINICONDA_URL="http://repo.continuum.io/miniconda"
MINICONDA_FILE="Miniconda2-latest-Linux-x86_64.sh"
wget "https://github.com/prometeia/continuous-integration/raw/master/Miniconda2-latest-Linux-x86_64.sh"
bash $MINICONDA_FILE -b

export PATH=$HOME/miniconda/bin:$HOME/miniconda2/bin:$PATH
#dalla version conda >=4.2 non esiste piu' la get_proxy_server dal modulo config 
#facendo rompere tutte le nostre  build!!! 
conda install --yes pip jinja2 anaconda-client==1.2.1 conda-build==1.16 conda==4.1.12
conda install conda-build==2.0.7
conda config --add channels https://conda.anaconda.org/prometeia
conda config --add channels https://conda.anaconda.org/t/$BINSTAR_TOKEN/prometeia
