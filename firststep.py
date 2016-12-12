"""先大概寫個架構."""

# .
# |-lib
# |---tests
# |-docs
# |-source

"""
我先找出所有需要的功能，然後把這些功能寫在一個 BaseClass 裡面
一樣的就寫在 BaseClass 裡面實現
不一樣的就在新類別裡面寫


1. 確認檔案格式。確認一下跟上次拿到的檔案有沒有差別。應該是一堆壓縮檔
2. 解壓縮資料。這個可能有 rar 有 gz 有 tar.gz，也可能有 zip。總之先解壓縮到當前資料夾
3. 後面就有點不知道怎麼分了，怎麼跟我的模版格式兜在一起？
    我的文件分類是
        銀行別 -> 系統別 -> IBM 產品別 -> LPAR

    總之 3 就是正式處理檔案 processor，那我的 copyfile 要放在哪裡？
    還是處理完之後，後面交給 copyfile? 這樣我的 copyfile 就不用每次重寫

4. make html

除了 3. 以外都還好，那再來考略 3 怎麼寫

LPAR 需不需要是一個物件？目前想不到他的 method。
    1. 他幾乎不會變動
    2. 他只是個名字
那 LPAR 只需要是一個 string 就可以了

再來考慮產品別，假設有個 WAS Class 如下

他應該會有
    屬性：當然是 LPAR : list()
    方法：處理 gc 整合  ( 將檔案複製到 source 資料夾這個動作給 BaseTemple 做)

"""


class WASClass(object):
    def __init__(self):
        self.all_lpars = []

    def add_new_lpar(self, hostname):  # TODO 糟糕，每個產品都會有這個函式，那我是不是要有一個 BaseProduct Class? 兩個了喔( 下面的 process)
        """增加一個 LPAR."""
        self.all_lpars.append(hostname)

    def display_all(self):
        """隨便寫個功能看看."""
        for lpar in self.all_lpars:
            print(lpar.hostname)

    def combile_gc(self):
        """把 GC log 弄成一個檔案."""
        pass

    def process(self):
        """產品需要一個執行者函式，處理所有的事"""
        pass


# 至於系統別的 CLASS , 應該就不用放在 lib 裡面了>是可放一個  base 給他辣

class BaseSystem(object):
    def addsytem(self, system):
        self.system = system

class Etabs_North(BaseSystem):
    def __init__(self):
        self.all_product = [ WASClass() ]

# class LandBank():
#     """"""


# 好啦，一個 account 應該長的向這樣
account = {"LandBank": [{"etabs_north": ["db2", "ihs", "was", "wmq"]},
                        {"etabs_south": ["db2", "ihs", "was", "wmq"]}
                        ],
           "CHB": ["eai", "netbank", "payment"]
           }

# "db2" 下面還要分 Lpar，我先從下往上寫好了...

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
        raise NotImplementedError

    def process(self):
        for lpar in self.all_lpars:
            print("處理 DB2")
            print("處理 LPAR: {}".format(lpar))

class WAS_Product(IBM_ProductTemplate):
    """docstring for DB2"""
    def create_gclog(self):
        raise NotImplementedError

    def process(self):
        for lpar in self.all_lpars:
            print("處理 WAS")
            print("處理 LPAR: {}".format(lpar))


DB2 = DB2_Product()
DB2.add_lpar('A1', 'A2')
DB2.display_all()
WAS = WAS_Product()
WAS.add_lpar('A1', 'A2')

# DB2.create_db2diag()

# 好啦，我的產品可以加入 LPAR 了。接下是 System別

class SystemTemplate(object):
    """docstring for SystemTemplate"""
    def __init__(self):
        """某個系統之下有一堆 IBM 產品."""
        self.all_products = []

    def add_product(self, *products):
        """接收多個 product 位置引數, 加入到 all_products list 中."""
        for product in products:
             self.all_products.append(product)

    def process(self):
        for product in self.all_products:
            product.process()


etabs = SystemTemplate()
etabs.add_product(DB2)
etabs.add_product(WAS)
# for prod in etabs.all_products:
#     print(prod.process())
etabs.process()
eai = SystemTemplate()

eai.add_product(DB2_Product('B1', 'B2'))
# for prod in eai.all_products:
#     print(prod.process())

eai.process()
