import os
from astropy.io import fits
import numpy as np
#from astropy.io import ascii
#from astropy import units as u
from astropy.coordinates import SkyCoord
#from astropy import constants as const
#from astropy.cosmology import FlatLambdaCDM
import requests


def download_pipe3d(plate, ifudesign, 
                    save_dir='./', quiet=True, ):
    """Download the MaNGA pipe3d file to given path, version SDSS DR17, SSP MaSTAR.

    Args:
        plate (int): MaNGA PLATE
        ifudesign (int): MaNGA IFUDESIGN 
        daptype (str, optional): 'SPX', 'VOR10', or 'HYB10'. Default = 'SPX'.
        save_dir (str, optional): Directory for saving. Default = current path.
        quiet (bool, optional): Print result or not. Default is not.
    """
          
    if not os.path.exists(save_dir):
        raise RuntimeError("No such directory: " + str(save_dir))
    else:
        save_loc = f'{save_dir}/manga-{plate}-{ifudesign}-LOGCUBE-{daptype}-MILESHC-MASTARSSP.fits.gz'
        if os.path.exists(save_loc):
            if ~quiet:
                print('File existed')
        else:
            logcube_url = f'https://data.sdss.org/sas/dr17/manga/spectro/analysis/v3_1_1/3.1.0/{daptype}-MILESHC-MASTARSSP/{plate}/{ifudesign}/manga-{plate}-{ifudesign}-LOGCUBE-{daptype}-MILESHC-MASTARSSP.fits.gz'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; \
                rv:80.0) Gecko/20100101 Firefox/80.0'}
            with requests.get(logcube_url, headers=headers, stream=True) as r:
                if r.status_code == requests.codes.ok:
                    with open(save_loc, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
            if not quiet:
                print(f"File downloaded: {save_loc}")