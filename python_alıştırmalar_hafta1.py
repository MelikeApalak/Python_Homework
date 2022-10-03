#GÖREV 2
#verilen ifadenin tüm harflerini büyük harfe çevirmek.
text = "the goal is to turn data into information, and information into insight."
text = text.replace("."," ")
text = text.replace(","," ")
text.upper()
print(text.split(" "))

#GÖREV 3
lst = ["D","A","T","A","S","C","I","E","N","C","E"]
#verilen listenin eleman sayısı
len(lst)
lst[0]
lst[10]
# 8. indexi silmek
del lst[8]
lst
lst.append("R")
lst
new_lst=[]
#8. indexe eleman eklemek
for i in lst[0:4]:
    new_lst.append(i)
new_lst
lst.insert(8,"N")
lst
#insert indexe göre ekler, append sonuna ekler.

#GÖREV 4
dict = {'Christian': ["America",18],
        'Daisy':["England",12],
        'Antonio': ["Spain",22],
        'Dante': ["Italy",25]}

#key değerlerine erişmek
dict.keys()
#value değerlerine erişmek
dict.values()
#key değeri Ahmet value değeri [Turkey,24] olan yeni bir değer eklemek
dict['Ahmet'] = ["Turkey",24]
#Antonio'yu dictionaryden silmek
del dict['Antonio']
dict
#Daisy key'ine 12 değerini 13 olarak güncellemek
dict.update({'Daisy': ["England",13]})
dict

#GÖREV 5
#argüman olarak bir listealan, listenin içindeki tek ve çift sayıları
#ayrı listelere atayan bu listeleri return eden fonksiyon yaz

l = [2,13,18,93,22]
even =[]
odd =[]
def func(list):
    for i in list:
        if i % 2 == 0:
            even.append(i)
        else:
            odd.append(i)
    return even,odd
even_list, odd_list = func(l)
print(even_list,odd_list)

#GÖREV 6
ogrenciler = ["Ali","Veli","Ayşe","Talat","Zeynep","Ece"]
for index,ogrenci in enumerate(ogrenciler,1):
    if index<4:
        print("Mühendislik fakültesi", index, ".", "öğrenci: ", ogrenci )
    else :
        print("Tıp fakültesi", index, ".", "öğrenci: ", ogrenci)

#GÖREV 7
#aşağıdaki 3 listeyi zip kullanarak bilgilerini bastırmak
ders_kodu = ["CMP1005","PSY1001","HUK1005","SEN2204"]
kredi = [3,4,2,4]
kontenjan = [30,75,150,25]
ders_listesi = list(zip(kredi,ders_kodu,kontenjan))
ders_listesi
for i in ders_listesi:
    print("Kredisi", i[0], "olan", i[1], "kodlu dersin kontenjanı",i[2], "kişidir.")

#GÖREV 8
#aşağıda verilen setlerde eğer 1. küme 2. kümeyi kapsıyor ise ortak elemanlarını
#kapsamıyor ise 2. kümenin 1. kümeden farkını yazdıracak fonksiyonu tanımlayın.
kume1= set(["data","python"])
kume2= set(["data","function","qcut","lambda","python","miuul"])
if kume1.issuperset(kume2):
    print(kume1.intersection(kume2))
else:
    print(kume2.difference(kume1))