"""簡單的完成 06/24 剩下的工作."""

import os
import tempfile
import zipfile
import shutil
import subprocess as sub
from pathlib import Path

WORK_DIR = 'Z:\\CHB_AHC_2017Q2'
AHC_DIR = 'C:\\src\\ahc'
os.chdir(WORK_DIR)
print("Test.")
# 想用 python 來做剩下的
# 來源 Z:\CHB_AHC_2017Q2\WAS\cpap1\Dmgr01\cpap1-cpap1Cell01-cpap1CellManager01-Dmgr01-WASenv.jar
# 有一個這樣的來源檔，我需要先將他解壓縮
# 目的 C:\src\ahc_html\payment\was\cpap1\source\

# with tempfile.TemporaryDirectory() as tmpdirname:
#     print('created temporary directory', tmpdirname)


# 先嘗試解壓縮 jar 檔案看看
# 發現似乎是檔案的 full 名稱(含目錄) 名稱太長 會導致出現 No such file 錯誤
# 可是我用的是 win10 應該可以正常工作才對, 難道 python 的 api 還是舊的
# FileNotFoundError: [Errno 2] No such file or directory: 'Z:\\CHB_AHC_2017Q2\\WAS\\cpap1\\Dmgr01\\cpap1\\root\\usr\\IBM\\WebSphere\\AppServer\\profiles\\Dmgr01\\config\\cells\\cpap1Cell01\\applications\\CHB_SECURITY_SAPII_war.ear\\deployments\\CHB_SECURITY_SAPII_war\\CHB_SECURITY_SAPII.war\\WEB-INF\\lib\\tknAPI.jar\\META-INF\\web-fragment.xml'

# with zipfile.ZipFile("cpap1-cpap1Cell01-cpap1CellManager01-Dmgr01-WASenv.jar") as z:
#     z.extractall()

# 改用 7z.exe 用 subprocess call 還是有問題，但是 7z 的 gui 沒問題

# 如果不要 extractall 呢
# 例如 payment 就只解壓 /waslog

# Z:\CHB_AHC_2017Q2\WAS\cpap1\Dmgr01\cpap1-cpap1Cell01-cpap1CellManager01-Dmgr01-WASenv\cpap1\root\waslog
# cpap1\root\waslog


# with zipfile.ZipFile("cpap1-cpap1Cell01-cpap1CellManager01-Dmgr01-WASenv.jar") as z:
#     for file in z.filelist:
#         if file.filename.find("cpap1/root/waslog") != -1:  # 看起來好怪 # 意思是如果開頭是 "cpap1/root/waslog"
#             # 完了，我對 python 的 if 概念已經望光了
#             # 什麼是 python 的真值？ 0 或 Null 或空集合 以外的才是真
#             # 而 find 返回的是位置， -1 代表沒這個位置, 所以應該這樣寫         
#             print(file.filename)
#             z.extract(file)
#             # 但是這樣寫太醜了，我要換一下

os.chdir('.\\WAS\\cpap1\\Dmgr01')
SERVER_CPAP1 = ['CPAP1', 'dmgr', 'EATMMGR1', 'PKIADMAP1', 'WMAP1', 'EATMAP1',\
                'OTPAP1', 'PKIAP1', 'XMLGWAP1']

# 這一段只負責解壓 jar 檔裡面的 waslog
with zipfile.ZipFile("cpap1-cpap1Cell01-cpap1CellManager01-Dmgr01-WASenv.jar") as z:
    for file in z.filelist:
        for server in SERVER_CPAP1:
            if file.filename.startswith("cpap1/root/waslog/" + server):
                print(file.filename)
                z.extract(file)

os.chdir('.\\cpap1\\root\\waslog')
for SERVER in SERVER_CPAP1:
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
        'C:\\src\\ahc_html\\payment\\was\\cpap1\\source\\' + SERVER + '\\')
    # 應該再加一條 移除所有 native_stderr* 以外的檔案        
    os.chdir('..')

# 到這裡時路徑在這裡 Z:\CHB_AHC_2017Q2\WAS\cpap1\Dmgr01\cpap1\root\waslog