# -*- coding: utf-8 -*-
"""
    Check and download all the LoTSS DR3 images and rms images which
    contain the MaNGA galaxies.
    
    Copyright (C) 2019-2024, Gaoxiang Jin

    E-mail: gx-jin@outlook.com

    This software is provided as is without any warranty whatsoever.
    Permission to use, for non-commercial purposes is granted.
    Permission to modify for personal or internal use is granted,
    provided this copyright and disclaimer are included unchanged
    at the beginning of the file. All other rights are reserved.
    In particular, redistribution of the code is not allowed.
"""

import os
import numpy as np
import pandas as pd
from astropy.table import Table
from astropy.coordinates import SkyCoord
from tqdm import tqdm
from requests.auth import HTTPBasicAuth
import requests

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


dr3df = pd.read_html('/afs/mpa/home/gxjin/code-mpa/data/dr3list_241021.html')[0]

fieldid = dr3df['Field name'].to_numpy()
ra_dr3 = dr3df['RA'].to_numpy()
dec_dr3 = dr3df['Dec'].to_numpy()

cat_dap = Table.read('/afs/mpa/home/gxjin/code-mpa/data/dapall-v3_1_1-3.1.0_spx.fits')

ra_dap = cat_dap['OBJRA'].data
dec_dap = cat_dap['OBJDEC'].data

mosiac_size = 2.2#1.917 # assuming mosiac size = 1.917 deg
dr3field = np.zeros_like(ra_dap, dtype='S11')

dap_skycoo = SkyCoord(ra_dap, dec_dap, frame='icrs', unit='deg')
field_skycoo = SkyCoord(ra_dr3, dec_dr3, frame='icrs', unit='deg')

for i in range(len(ra_dap)):
    septmp = dap_skycoo[i].separation(field_skycoo).deg
    if np.min(septmp) < mosiac_size:
        dr3field[i] = fieldid[septmp == np.min(septmp)][0]
    elif np.min(septmp) >= mosiac_size:
        dr3field[i] = 'NOCOVERAGE'
    else:
        print('Warning')

def download_mosaic(fid, save_dir):
    save_loc = save_dir+fid+'_high_mosaic.fits'
    url = f'https://lofar-surveys.org/downloads/DR3/mosaics/{fid}/mosaic-blanked.fits'
    download(url, save_loc, username='surveys', password='150megahertz', quiet=True)
                    
def download_rms(fid, save_dir):
    save_loc = save_dir+fid+'_rms.fits'
    url = f'https://lofar-surveys.org/downloads/DR3/mosaics/{fid}/mosaic-blanked--final.rms.fits'
    download(url, save_loc, username='surveys', password='150megahertz', quiet=True)

save_dir = '/afs/mpa/temp/gxjin/LOTSS3/'
for i in tqdm(range(len(ra_dap))): #len(ra_dap)
    fidtmp = dr3field[i].decode('utf-8')
    if fidtmp == 'NOCOVERAGE':
        continue
    else:
        download_mosaic(fidtmp, save_dir)
        download_rms(fidtmp, save_dir)
        if not os.path.exists(save_dir+fidtmp+'_high_mosaic.fits'):
            download(f'https://lofar-surveys.org/downloads/DR2/mosaics/{fidtmp}/mosaic-blanked.fits',
                        save_dir+fidtmp+'_high_mosaic.fits',
                        username='surveys', password='150megahertz', quiet=True)
        if not os.path.exists(save_dir+fidtmp+'_rms.fits'):
            download(f'https://lofar-surveys.org/downloads/DR2/mosaics/{fidtmp}/mosaic.rms.fits',
                        save_dir+fidtmp+'_rms.fits',
                        username='surveys', password='150megahertz', quiet=True)    
