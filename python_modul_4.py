## İŞ PROBLEMİ

#Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama
#stratejileri belirlemek istiyor.

#veri seti = online_retail.csv
#ingiltere merkezli bir mağazanın 2009-2011 arasındaki satışlarını içeriyor.

#veri setindeki değişkenler:

#InvoiceNo : Fatura numarası. Her işleme yani faturaya ait eşssiz numara. C ile başlıyorsa iptal edilen işlem.
#StockCode : Ürün kodu. Her bir ürün için eşsiz numara.
#Description : Ürün ismi
#Quantity : Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını gösterir.
#InvoiceDate : Fatura tarihi ve zamanı
#UnitPrice : Ürün fiyatı (sterlin)
#CustomerID : Eşsiz müşteri numarası
#Country : müşterinin yaşadığı ülke ismi.

## 2. Veriyi Anlama (Data Understanding)
import datetime as dt
import pandas as pd
pd.set_option('display.max_columns',None) # bütün sütunları gör
#pd.set_option('display.max_rows', None)  # bütün satırları gör
pd.set_option('display.float_format',lambda x: '%.3f' % x) #sayısal değişk. virgülden sonra kaç basamağı görünsün ?

df_ = pd.read_excel('C:/Users/MSI/Downloads/crm_analytics-220908-141436/crm_analytics/datasets/online_retail_II.xlsx',sheet_name="Year 2009-2010")
#orijinal df yi bozmadan üzerinde çalışmamız için aşağıdaki kodu ekleriz.
df = df_.copy() #bir sonraki çalışmalarda uzun okuma yapmayı engellemek için.

df.head()
df.shape #veri seti boyutu (gözlem birimi ve değişken)
df.isnull().sum() #hangi değişkende kaç tane eksik değer var?

df["Description"].nunique() #eşsiz ürün sayısı

df["Description"].value_counts().head() #her bir üründen kaç tane satıldı bilgisi

df.groupby("Description").agg({"Quantity": "sum"}).head()  #en çok sipariş edilen ürün

#sıralama
df.groupby("Description").agg({"Quantity":"sum"}).sort_values("Quantity",ascending=False).head()

df["Invoice"].nunique() #eşsiz fatura sayısı

df["TotalPrice"]= df["Quantity"]*df["Price"]
df.groupby("Invoice").agg({"TotalPrice":"sum"}).head()#fatura başına toplam kaç para kazanılmıştır?
df.head()

## 3. VERİ HAZIRLAMA
df.shape
df.isnull().sum()
df.dropna(inplace=True) # eksik değerleri silmek için kullanılır.
df.describe().T

#c'yi barındıranların dışındakileri getirir.
#iade olan ürünler veri setini bozduğu için onları tespit edip kaldıracağız.
df = df[~df["Invoice"].str.contains("C",na=False)]


#RFM METRİKLERİNİN HESAPLANMASI
#(RECENY, FREQUENCY, MONETARY)
df.head()

#ilgili hesaplamaları yapmak için analizin yapıldığı dönemi tanımlamak gerekiyor.
df["InvoiceDate"].max()

today_date= dt.datetime(2010,12,11)
type(today_date)

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda InvoiceDate:(today_date - InvoiceDate.max()).days, # InvoiceDate.max() kullanıcının son alışveriş zamanı
                                     'Invoice': lambda Invoice:Invoice.nunique(), #imvoice lerin eşsiz değerini hesapla.
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()}) #total priceların sum ını al
#groupby ile müşterileri tekilleştirdik.
#daha sonra recency ,eşsiz fatura sayısı, toplam ödediği rakam değerlerini çıkardık.
rfm.columns = ['recency','frequency','monetary']
rfm.head()
rfm.describe().T #verileri betimliyoruz.

rfm = rfm[rfm["monetary"]>0]
rfm.shape

#yukarıdaki uygulamayla metrik sonuçlarını elde ettik. Bunları skora dönüştüreceğiz.

## 5. RFM Skorlarının Hesaplanması
#recency ters, frequency ve monetary düz şekilde skora dönüşecek.

#qcut : çeyrek değerlere göre bölme işlemi yapan bir methoddur. bir değişken ver ve
#bu değişkeni kaç parçaya bölmek istediğini ver daha sonra labelları ver.
#değişkeni küçükten büyüğe doğru sıralar daha sonra eşit parçalara ayırır.

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
#küçük değerlere 5 skoru vererek başlıyor. array sırasını o şekilde tanımladık.

rfm["monetary_score"] = pd.qcut(rfm['monetary'],5,labels=[1,2,3,4,5])

rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"),5,labels=[1,2,3,4,5])

#iki ayrı değişkende olan integer değerleri önce string değere çevirdik
#sonra birleştirip gösterdik.
rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str)+
                    rfm['frequency_score'].astype(str))

rfm.describe().T

rfm[rfm["RFM_SCORE"]=="55"] #champions müşteriler
rfm[rfm["RFM_SCORE"]== "11"] #görece önemi daha düşük olan müşteriler

## 6. RFM SEGMENTLERİNİN OLUŞTURULMASI VE ANALİZ EDİLMESİ

#RFM isimlendirilmesi
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]':'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]':  'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}
rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map,regex=True)
rfm[["segment","recency","frequency","monetary"]].groupby("segment").agg(["mean","count"])

rfm[rfm['segment'] == "cant_loose"].head()
rfm[rfm['segment'] == "cant_loose"].index #id ler gelir.

new_df = pd.DataFrame()
new_df["new_customer_id"] = rfm[rfm["segment"] == "new_customers"].index
new_df["new_customer_id"] = new_df["new_customer_id"].astype(int)
new_df.to_csv("new_customers.csv")
rfm.to_csv("rfm.csv")

## 7. TÜM SÜRECİN FONKSİYONLAŞTIRILMASI

def create_rfm(dataframe,csv=False):

    #veriyi hazırlama
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    dataframe.dropna(inplace=True) # eksik değerleri silmek için kullanılır.
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]

    #rfm metrikleri hesaplanması
    today_date = dt.datetime(2010, 12, 11)
    rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                         # InvoiceDate.max() kullanıcının son alışveriş zamanı
                                         'Invoice': lambda Invoice: Invoice.nunique(),
                                         # imvoice lerin eşsiz değerini hesapla.
                                         'TotalPrice': lambda
                                             TotalPrice: TotalPrice.sum()})  # total priceların sum ını al

    rfm.columns = ['recency', 'frequency', 'monetary']
    rfm = rfm[rfm["monetary"] > 0]

    #rfm skorlarının hesaplanması
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])
    rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

    #cltv_df skorları kategorik değere dönüştürülüp df'e eklendi.
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                        rfm['frequency_score'].astype(str))

    #segmentlerin isimlendirilmesi
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }
    rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
    rfm = rfm[["recency","frequency","monetary","segment"]]
    rfm.index = rfm.index.astype(int)
    if csv:
        rfm.to_csv("rfm.csv")
    return rfm

df = df_.copy()

rfm_new = create_rfm(df,csv=True)

### CUSTOMER LIFETIME VALUE

# 1. VERİ HAZIRLAMA

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
pd.set_option('display.max_columns',20)
#pd.set_option('display.max_rows',20)
pd.set_option('display.float_format', lambda x : '%.5f' % x)

df_ = pd.read_excel("C:/Users/MSI/Downloads/crm_analytics-220908-141436/crm_analytics/datasets/online_retail_II.xlsx",sheet_name="Year 2009-2010")
df = df_.copy()
df.head()
df.shape
df.isnull().sum()

#gözlem birimindeki invoice değişkeninde c varsa iptal edilen ürün demektir.
# başında c olan ürünleri silmemiz gerekir.

df = df[~df["Invoice"].str.contains("C",na=False)]
df.describe().T

df = df[(df["Quantity"] > 0)]
#customerID deki eksik değerleri yok ediyoruz.
df.dropna(inplace=True)

df["TotalPrice"] = df["Quantity"] * df["Price"]

cltv_c = df.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                        'Quantity':lambda x : x.sum(),
                                        'TotalPrice': lambda x : x.sum()})

cltv_c.columns = ['total_transaction','total_unit','total_price']