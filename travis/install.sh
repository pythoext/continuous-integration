MINICONDA_URL="http://repo.continuum.io/miniconda"
MINICONDA_FILE="Miniconda2-latest-Linux-x86_64.sh"
wget "https://github.com/prometeia/continuous-integration/raw/master/Miniconda2-latest-Linux-x86_64.sh"
bash $MINICONDA_FILE -b

export PATH=$HOME/miniconda/bin:$HOME/miniconda2/bin:$PATH
#dalla version conda >=4.2 non esiste piu' la get_proxy_server dal modulo config 
#facendo rompere tutte le nostre  build!!!
# python==2.7.14 
conda install --yes conda-build pip==8.1.2 jinja2==2.8 anaconda-client==1.2.1 conda==4.1.12 Cython==0.24 numpy==1.10.4
conda config --add channels https://conda.anaconda.org/prometeia
conda config --add channels https://conda.anaconda.org/t/$BINSTAR_TOKEN/prometeia
