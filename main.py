"""Main Function."""

# from lib import ahc

print("Hello")


# 糟糕，想不出來怎麼寫
# 先用傳統方式寫一次看看


# 假設土銀

# 給一個檔案來源資料夾 src C:\GoogleDrive\Desktop\Landbank
# 給一個目的資料夾 des C:\src\ahc_landbank_html

# 第一部應該是確認檔案

account = {"LandBank": [{"etabs_north": ["db2", "ihs", "was", "wmq"]},
                        {"etabs_south": ["db2", "ihs", "was", "wmq"]}
                        ],
           "CHB": ["eai", "netbank", "payment"]
           }

# for file in src.rglob('*.zip'):  # 靠 土銀的是 zip
