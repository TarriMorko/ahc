"""Main Function."""

from lib.ahc import SystemTemplate
from lib.ahc import DB2_Product
from lib.ahc import CustomerTemplate
print("Hello")


# 糟糕，想不出來怎麼寫
# 先用傳統方式寫一次看看


# 假設土銀

# 給一個檔案來源資料夾 src C:\GoogleDrive\Desktop\Landbank
# 給一個目的資料夾 des C:\src\ahc_landbank_html

# 第一部應該是確認檔案

# account = {"LandBank": [{"etabs_north": ["db2", "ihs", "was", "wmq"]},
#                         {"etabs_south": ["db2", "ihs", "was", "wmq"]}
#                         ],
#            "CHB": ["eai", "netbank", "payment"]
#            }

# for file in src.rglob('*.zip'):  # 靠 土銀的是 zip

netbank = SystemTemplate('netbank')
netbank.add_product(DB2_Product('cpdb1', 'cpdb2'))

eai = SystemTemplate('eai')
eai.add_product(DB2_Product('cpdb1', 'cpdb2'))

payment = SystemTemplate('payment')
payment.add_product(DB2_Product('cpdb1', 'cpdb2'))



CHB = CustomerTemplate(netbank, payment, eai, 
                       input_directory='D:\IBM\CHB - 原本的',
                       output_directory='C:\src\ahc_html')
CHB.run()
