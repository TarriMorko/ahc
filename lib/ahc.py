"""ahc classes."""

# 架構順序是這樣    銀行別 -> 系統別 -> IBM 產品別 -> LPAR
# TODO 有什麼方法可以


from pathlib import Path
input_dir = None

class CustomerTemplate(object):
    """docstring for CustomerTemplate.

    某家銀行的 template

    似乎要確定
    1. 檔案路徑
    2. 原本有什麼檔案
    3. 輸出路徑
    """

    def __init__(self,  *systems, input_directory='', output_directory=''):
        """某個產品下面有一堆 LPAR."""
        self.systems = []
        if systems:
            self.systems = [system for system in systems]
        global input_dir
        input_dir = Path(input_directory)
        self.output_directory = Path(output_directory)

    def check_file_formation(self):
        """"確認檔案格式。確認一下跟上次拿到的檔案有沒有差別。應該是一堆壓縮檔."""
        raise NotImplementedError

    def unzip_files(self):
        """解壓縮資料。這個可能有 rar 有 gz 有 tar.gz，也可能有 zip。總之先解壓縮到當前資料夾."""
        raise NotImplementedError
        # p = Path(self.input_directory)
        # for file in p.rglob('*.gz'):
        #     print(file.name)
        #     tar = tarfile.open(str(file))
        #     for member in tar.getmembers():
        #         print(member)
        #         member.name = member.name.replace('/tmp/ahc/','')
        #         tar.extract(member, str(file.parent))
        #         print(file.parent)
        #     tar.close()
        #     file.unlink()        

    def display_all(self):
        """隨便寫個功能看看."""
        for system in self.systems:
            system.process()

    def run(self):
        """Run all functions."""
        # self.check_file_formation(self)
        # self.unzip_files(self)
        for system in self.systems:
            print(system)
            system.process()


# 3. 後面就有點不知道怎麼分了，怎麼跟我的模版格式兜在一起？
#     我的文件分類是
#         銀行別 -> 系統別 -> IBM 產品別 -> LPAR

#     總之 3 就是正式處理檔案 processor，那我的 copyfile 要放在哪裡？
#     還是處理完之後，後面交給 copyfile? 這樣我的 copyfile 就不用每次重寫

# 4. make html


class IBM_ProductTemplate(object):
    def __init__(self, *hostnames):
        """某個產品下面有一堆 LPAR."""
        self.all_lpars = []
        if hostnames:
            self.all_lpars = [lpar for lpar in hostnames]

    def add_lpar(self, *hostnames):
        """接收多個 hostname 位置引數, 加入到 all_lpars list 中."""
        for hostname in hostnames:
             self.all_lpars.append(hostname)

    def display_all(self):
        """隨便寫個功能看看."""
        for lpar in self.all_lpars:
            print(lpar)

    def process(self):
        """產品需要一個執行者函式，處理所有的事"""
        pass


class DB2_Product(IBM_ProductTemplate):
    """docstring for DB2"""
    def create_db2diag(self):
        """TODO 1. 處理 db2diag.log , 然後移動到對應資料夾"""
        raise NotImplementedError

    def process(self):
        """TODO 2. 把符合 hostname 的，移動到對應資料夾."""
        for lpar in self.all_lpars:
            print("處理 DB2")
            print(input_dir)            
            print("處理 LPAR: {}".format(lpar))

class WAS_Product(IBM_ProductTemplate):
    """docstring for DB2"""
    def create_gclog(self):
        raise NotImplementedError

    def process(self):
        for lpar in self.all_lpars:
            print("處理 WAS")
            print("處理 LPAR: {}".format(lpar))



class SystemTemplate(object):
    """docstring for SystemTemplate"""
    def __init__(self, name):
        """某個系統之下有一堆 IBM 產品."""
        self.all_products = []
        self._name = name

    def __repr__(self):
        return self._name

    def add_product(self, *products):
        """接收多個 product 位置引數, 加入到 all_products list 中."""
        for product in products:
             self.all_products.append(product)

    def process(self):
        for product in self.all_products:
            product.process()



# DB2 = DB2_Product()
# DB2.add_lpar('A1', 'A2')
# DB2.display_all()
# WAS = WAS_Product()
# WAS.add_lpar('A1', 'A2')

# DB2.create_db2diag()

# 好啦，我的產品可以加入 LPAR 了。接下是 System別

# etabs = SystemTemplate()
# etabs.add_product(DB2)
# etabs.add_product(WAS)
# # for prod in etabs.all_products:
# #     print(prod.process())
# etabs.process()
# eai = SystemTemplate()

# eai.add_product(DB2_Product('B1', 'B2'))
# # for prod in eai.all_products:
# #     print(prod.process())

# eai.process()
# payment = SystemTemplate()

# payment.add_product(DB2_Product('cpdb1', 'cpdb2'))
# payment.add_product(WAS_Product('cpap1', 'cpap2', 'cpap3'))
# CHB = CustomerTemplate(payment)
# CHB.run()
