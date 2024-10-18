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
import shutil
from astropy.io import fits
from tqdm import tqdm


# def download_logcube(dapall='?', save_dir='?', daptype='SPX', test=False):
#     if not os.path.exists(dapall):
#         raise RuntimeError("No such directory: " + str(dapall))
#     elif not os.path.exists(save_dir):
#         raise RuntimeError("No such directory: " + str(save_dir))
#     elif not test:
#         hdu = fits.open(dapall)
#         plate = hdu[1].data['PLATE']
#         ifu = hdu[1].data['IFUDESIGN']
#         save_loc = f'{save_dir}/manga-{plate[1]}-{ifu[1]}-LOGCUBE-{daptype}-MILESHC-MASTARSSP.fits.gz'
#         maps_url = f'https://data.sdss.org/sas/dr17/manga/spectro/analysis/v3_1_1/3.1.0/{daptype}-MILESHC-MASTARSSP/{plate[1]}/{ifu[1]}/manga-{plate[1]}-{ifu[1]}-LOGCUBE-{daptype}-MILESHC-MASTARSSP.fits.gz'
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; \
#                 rv:80.0) Gecko/20100101 Firefox/80.0'}
#         with requests.get(maps_url, headers=headers, stream=True) as r:
#             if r.status_code == requests.codes.ok:
#                 with open(save_loc, 'wb') as f:
#                     shutil.copyfileobj(r.raw, f)
#     else:
#         hdu = fits.open(dapall)
#         plate = hdu[1].data['PLATE']
#         ifu = hdu[1].data['IFUDESIGN']
#         for i in tqdm(range(len(plate))):  
#             save_loc = f'{save_dir}/manga-{plate[i]}-{ifu[i]}-LOGCUBE-{daptype}-MILESHC-MASTARSSP.fits.gz'
#             if os.path.exists(save_loc):
#                 continue
#             else:
#                 maps_url = f'https://data.sdss.org/sas/dr17/manga/spectro/analysis/v3_1_1/3.1.0/{daptype}-MILESHC-MASTARSSP/{plate[i]}/{ifu[i]}/manga-{plate[i]}-{ifu[i]}-LOGCUBE-{daptype}-MILESHC-MASTARSSP.fits.gz'
#                 headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; \
#                     rv:80.0) Gecko/20100101 Firefox/80.0'}
#                 with requests.get(maps_url, headers=headers, stream=True) as r:
#                     if r.status_code == requests.codes.ok:
#                         with open(save_loc, 'wb') as f:
#                             shutil.copyfileobj(r.raw, f)


# dapall_dir = '../dap'
# save_dir = './'
# download_logcube(dapall=dapall_dir, save_dir=save_dir, daptype='SPX', test=True)

# # todo: check how many files, etc.
