"""簡單的完成 06/24 剩下的工作."""

import os
import tempfile
import zipfile
import shutil
import subprocess as sub
from pathlib import Path

WORK_ROOT_DIR = 'Z:\\CHB_AHC_2017Q2'
AHC_DIR = 'C:\\src\\ahc'
os.chdir(WORK_ROOT_DIR)
print("Test.")

# Z:\CHB_AHC_2017Q2\WAS\cpap2\AppSrv01
LPAR_NAME = "cpap2"
WAS_PROFILE_NAME = "AppSrv01"
PRODUCT = "WAS"
WORK_DIR = '\\'.join([WORK_ROOT_DIR, PRODUCT, LPAR_NAME, WAS_PROFILE_NAME])
COLLE_FILE = "cpap2-cpap1Cell01-cpap2Node01-AppSrv01-WASenv.jar"
SERVER_LISTS = ['CPAP2', 'EATMAP2', 'EDDAAP2', 'OTPAP2', 'PKIADMAP2', 'PKIAP2',
                'TKNAP2', 'WMAP2', 'XMLGWAP2']
os.chdir(WORK_DIR)

# 這一段只負責解壓 jar 檔裡面的 waslog
with zipfile.ZipFile(COLLE_FILE) as z:
    for file in z.filelist:
        for SERVER in SERVER_LISTS:
            if file.filename.startswith(LPAR_NAME +"/root/waslog/" + SERVER):
                print(file.filename)
                z.extract(file)

os.chdir('.\\' + LPAR_NAME + '\\root\\waslog')
for SERVER in SERVER_LISTS:
    os.chdir(SERVER)
    p = Path('.')
    with open('Rev_SystemOut.log', 'wt') as f:
        for file in p.glob('Sys*'):
            sub.call(['C:\\Program Files\\Git\\usr\\bin\\grep.exe', '-i', \
                      'HMGR0152W', file.name, ], shell=True, stdout=f)
            sub.call(['C:\\Program Files\\Git\\usr\\bin\\grep.exe', '-i', \
                      'J2CA0045E', file.name, ], shell=True, stdout=f)
            sub.call(['C:\\Program Files\\Git\\usr\\bin\\grep.exe', '-i', \
                      'WSVR0605W', file.name, ], shell=True, stdout=f)

        for file in p.glob('native_stderr*'):
            sub.call(['C:\\Program Files\\Git\\usr\\bin\\grep.exe', '-i', \
                    'Dump', file.name, ], shell=True, stdout=f)

    # Rev_SystemOut.log 要 cp 到 AHC_DIR = 'C:\\src\\ahc'
    # C:\src\ahc_html\payment\was\cpap1\source\CPAP1
    shutil.copy('.\\Rev_SystemOut.log', \
        'C:\\src\\ahc_html\\payment\\was\\' + LPAR_NAME + '\\source\\' + SERVER + '\\')
    # 應該再加一條 移除所有 native_stderr* 以外的檔案        
    os.chdir('..')
