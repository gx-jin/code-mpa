# -*- coding: utf-8 -*-
"""
    Check and download all the MaNGA DAP LOGCUBE files to the given path.
    
    Copyright (C) 2019-2024, Gaoxiang Jin

    E-mail: gx-jin@outlook.com

    Updated versions of the codes are available from github pages:
    https://github.com/gx-jin/py_astro_gxjin

    This software is provided as is without any warranty whatsoever.
    Permission to use, for non-commercial purposes is granted.
    Permission to modify for personal or internal use is granted,
    provided this copyright and disclaimer are included unchanged
    at the beginning of the file. All other rights are reserved.
    In particular, redistribution of the code is not allowed.
"""


import os
import requests
from astropy.io import fits
from tqdm import tqdm
from requests.auth import HTTPBasicAuth


def download(url: str, local_filename: str,
             username='None', password='None',
             quiet=True):
    
    headers = {'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'}
    
    # Check parent directory
    parent_directory = os.path.dirname(local_filename)
    if not os.path.isdir(os.path.dirname(local_filename)):
        print(f"The parent directory '{parent_directory}' does not exist")
        return
    
    # Check if file exists
    if os.path.exists(local_filename) & (not quiet):
        print(f"File exists: '{local_filename}'")
        return
    
    # Try download
    try:
        response = requests.head(url, 
                                 headers=headers, stream=True, timeout=540,
                                 auth = HTTPBasicAuth(username, password))
        if response.status_code == requests.codes.ok:
            with requests.get(url,
                              headers=headers, stream=True, timeout=540,
                              auth = HTTPBasicAuth(username, password)) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            if not quiet:
                print(f"File '{local_filename}' downloaded")
            return        
        else:
            print(f'HTTP error {response.status_code}: {url}')
    except requests.RequestException:
        print('Invalid url')
        
        
def download_cube(dapall='?', save_dir='?', daptype='SPX', test=False):
    if not os.path.exists(dapall):
        raise RuntimeError("No such directory: " + str(dapall))
    elif not os.path.exists(save_dir):
        raise RuntimeError("No such directory: " + str(save_dir))
    elif test:
        hdu = fits.open(dapall)
        plate = hdu[1].data['PLATE']
        ifu = hdu[1].data['IFUDESIGN']
        i = 3 
        save_loc = f'{save_dir}/manga-{plate[i]}-{ifu[i]}-LOGCUBE-{daptype}-MILESHC-MASTARSSP.fits.gz'
        maps_url = f'https://data.sdss.org/sas/dr17/manga/spectro/analysis/v3_1_1/3.1.0/{daptype}-MILESHC-MASTARSSP/{plate[i]}/{ifu[i]}/manga-{plate[i]}-{ifu[i]}-LOGCUBE-{daptype}-MILESHC-MASTARSSP.fits.gz'
        download(maps_url, save_loc, quiet=True)
        
    else:
        hdu = fits.open(dapall)
        plate = hdu[1].data['PLATE']
        ifu = hdu[1].data['IFUDESIGN']
        dapdone = hdu[1].data['DAPDONE']
        for i in tqdm(range(len(plate))):  
            save_loc = f'{save_dir}manga-{plate[i]}-{ifu[i]}-LOGCUBE-{daptype}-MILESHC-MASTARSSP.fits.gz'
            if os.path.exists(save_loc):
                continue
            elif dapdone[i]:
                maps_url = f'https://data.sdss.org/sas/dr17/manga/spectro/analysis/v3_1_1/3.1.0/{daptype}-MILESHC-MASTARSSP/{plate[i]}/{ifu[i]}/manga-{plate[i]}-{ifu[i]}-LOGCUBE-{daptype}-MILESHC-MASTARSSP.fits.gz'
                download(maps_url, save_loc, quiet=True)

dapall_dir = '/afs/mpa/home/gxjin/code-mpa/data/dapall-v3_1_1-3.1.0_spx.fits'
save_dir = '/afs/mpa/project/sdss/manga/dap_v311/DAP11_LOGCUBE_SPX/'
download_cube(dapall=dapall_dir, save_dir=save_dir, daptype='SPX', test=False)

# todo: check how many files, etc.

