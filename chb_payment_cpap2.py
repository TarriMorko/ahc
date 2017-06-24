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



# SYSTEMS = "payment"
# LPAR_NAME = "cpap2"
# WAS_PROFILE_NAME = "AppSrv01"
# PRODUCT = "WAS"
# WORK_DIR = '\\'.join([WORK_ROOT_DIR, PRODUCT, LPAR_NAME, WAS_PROFILE_NAME])
# # Z:\CHB_AHC_2017Q2\WAS\cpap2\AppSrv01 <-- payment 的就是這個
# # # Z:\CHB_AHC_2017Q2\WAS\ebportal5\AppSrv01\ebportal5 <-- 網銀的可能長這樣
# COLLE_FILE = "cpap2-cpap1Cell01-cpap2Node01-AppSrv01-WASenv.jar"
# WAS_LOG_LOCATION = "/root/waslog/"
# # "/root/waslog/" payment
# # "/root/usr/IBM/WebSphere/AppServer/profiles/AppSrv01/logs/" 網銀的應該是這個
# SERVER_LISTS = ['CPAP2', 'EATMAP2', 'EDDAAP2', 'OTPAP2', 'PKIADMAP2', 'PKIAP2',
#                 'TKNAP2', 'WMAP2', 'XMLGWAP2']



def create_was_systemout(systems, lpar_name, was_profile_name,
                         product, colle_file, was_log_location, server_lists):
    """產生 WAS 的 Rev_SystemOut.log."""

    work_dir = '\\'.join([WORK_ROOT_DIR, product.upper(), lpar_name, was_profile_name])
    os.chdir(work_dir)
    # 這一段只負責解壓 jar 檔裡面的 waslog
    with zipfile.ZipFile(colle_file) as z:
        for file in z.filelist:
            for server in server_lists:
                if file.filename.startswith(lpar_name + was_log_location + server):
                    # payment 的 waslog 在這裡
                    # Z:\CHB_AHC_2017Q2\WAS\cpap1\Dmgr01\cpap1 \root\waslog
                    # netbank 的長這樣
                    # Z:\CHB_AHC_2017Q2\WAS\ebportal5\AppSrv01\ebportal5 \root\usr\IBM\WebSphere\AppServer\profiles\AppSrv01\logs
                    print(file.filename)
                    z.extract(file)

    os.chdir('.\\' + lpar_name + was_log_location.replace('/', '\\'))
    for server in server_lists:
        os.chdir(server)
        with open('Rev_SystemOut.log', 'wt') as f:
            for file in Path('.').glob('Sys*'):
                sub.call(['C:\\Program Files\\Git\\usr\\bin\\grep.exe', '-i', \
                        'HMGR0152W', file.name, ], shell=True, stdout=f)
                sub.call(['C:\\Program Files\\Git\\usr\\bin\\grep.exe', '-i', \
                        'J2CA0045E', file.name, ], shell=True, stdout=f)
                sub.call(['C:\\Program Files\\Git\\usr\\bin\\grep.exe', '-i', \
                        'WSVR0605W', file.name, ], shell=True, stdout=f)

            for file in Path('.').glob('native_stderr*'):
                sub.call(['C:\\Program Files\\Git\\usr\\bin\\grep.exe', '-i', \
                        'Dump', file.name, ], shell=True, stdout=f)

        # Rev_SystemOut.log 要 cp 到 AHC_DIR = 'C:\\src\\ahc'
        # C:\src\ahc_html\payment\was\cpap1\source\CPAP1
        shutil.copy('.\\Rev_SystemOut.log', \
            'C:\\src\\ahc_html\\' + systems + '\\' \
            + product.lower() + '\\' + lpar_name + '\\source\\' + server + '\\')
        # 應該再加一條 移除所有 native_stderr* 以外的檔案
        os.chdir('..')

create_was_systemout(systems="payment",
                     lpar_name="cpap3",
                     was_profile_name="AppSrv01",
                     product="WAS",
                     colle_file="cpap3-cpap1Cell01-cpap3Node01-AppSrv01-WASenv.jar",
                     was_log_location="/root/waslog/",
                     server_lists=['EATMAP3', 'OTPAP3', 'PKIADMAP3', 'PKIAP3', 'TKNAP3']
                    )
                    