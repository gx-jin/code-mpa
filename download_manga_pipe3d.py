# -*- coding: utf-8 -*-
"""
    Check and download all the MaNGA DAP MAPS files to the given path.
    
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
    if os.path.exists(local_filename):
        if not quiet:
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

def download_pipe3d(allfile='?', save_dir='?', test=False):
    if not os.path.exists(allfile):
        raise RuntimeError("No Pipe3D catalog: " + str(allfile))
    elif not os.path.exists(save_dir):
        raise RuntimeError("No such directory: " + str(save_dir))
    elif test:
        hdu = fits.open(allfile)
        plate = hdu[1].data['plate']
        ifu = hdu[1].data['ifudsgn']
        i = 3
        save_loc = f'{save_dir}manga-{plate[i]}-{ifu[i]}.Pipe3D.cube.fits.gz'

        maps_url = f'https://data.sdss.org/sas/dr17/manga/spectro/pipe3d/v3_1_1/3.1.1/{plate[i]}/manga-{plate[i]}-{ifu[i]}.Pipe3D.cube.fits.gz'
        download(maps_url, save_loc, quiet=True)
    else:
        hdu = fits.open(allfile)
        plate = hdu[1].data['plate']
        ifu = hdu[1].data['ifudsgn']
        for i in tqdm(range(len(plate))):  
            save_loc = f'{save_dir}manga-{plate[i]}-{ifu[i]}.Pipe3D.cube.fits.gz'
            if os.path.exists(save_loc):
                continue
            else:
                maps_url = f'https://data.sdss.org/sas/dr17/manga/spectro/pipe3d/v3_1_1/3.1.1/{plate[i]}/manga-{plate[i]}-{ifu[i]}.Pipe3D.cube.fits.gz'
                download(maps_url, save_loc, quiet=True)


allfile_dir = '/afs/mpa/home/gxjin/code-mpa/data/SDSS17Pipe3D_v3_1_1_part.fits'
save_dir = '/afs/mpa/project/sdss/manga/dap_v311/PIPE3D/'

download_pipe3d(allfile=allfile_dir, save_dir=save_dir, test=False)

# todo: check how many files, etc.
