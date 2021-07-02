#----------------------------------
#说明
#此文件用于将flash文件夹下分区/系列/文章的更改应用于数据库
#运行方式：cmd到此文件路径下，python tdatabase.py
#----------------------------------

import include
import os,sys,django
sys.path.append(include.DJANGOROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangowebsite.settings") #应该是在其他目录调用时需要使用
django.setup()
from blog.models import *

ROOTFLASH=include.DJANGOROOT+"flash/docx/"
DESCNAME="__desc__.txt" #描述文件名

block=[]
serie={}
article={}
desc={}

for root1,dir1,file1 in os.walk(ROOTFLASH):
    block=dir1
    break #dir的第一个子目录列表
for i in block: #遍历所有分区文件夹
    for root2,dir2,file2 in os.walk(ROOTFLASH+i):
        serie[i]=dir2
        break #存入系列文件夹名
    for j in serie[i]: #遍历所有系列文件夹
        for root3,dir3,file3 in os.walk(ROOTFLASH+i+"/"+j):
            file=file3
            break #系列文件夹下所有文件，包括文章和系列描述
        if(DESCNAME in file): #如果描述文件存在，存入描述
            with open(ROOTFLASH+i+"/"+j+"/"+DESCNAME,encoding="utf-8",errors="ignore") as f:
                desc[j]=f.read()
        _m=[]
        for k in file:
            if(".docx" in k):
                _m.append(k.replace(".docx","")) #去掉后缀
        article[j]=_m #文章名存入article
#删除
for i in Blocks.objects.all():
    if(i.blocks not in block):
        i.delete()
serie_value=serie.values()
for i in Series.objects.all():
    if(i.series not in serie_value):
        i.delete()
article_value=article.values()
for i in Articles.objects.all():
    if(i.docname not in article_value):
        i.delete()
#新建或更改
for i in block: #创建Blocks对象
    #我倒是想粗暴地get_or_create，但是这个是有时间自动更新的
    if(Blocks.objects.filter(blocks=i).count()==0):
        Blocks.objects.create(blocks=i)
    for j in serie[i]: #按照分区依次创建Series对象
        if(Series.objects.filter(series=j).count()==0):
            if(j in desc.keys()):
                Series.objects.create(series=j,typename=i,introduction=desc[j])
            else:
                Series.objects.create(series=j,typename=i,introduction="")
        else: #如果已经存在此serie，尝试更新
            _serie=Series.objects.get(series=j) 
            flag=True
            if(_serie.typename!=i):
                _serie.typename=i
                flag=False
            if(_serie.introduction!=desc[j]):
                _serie.introduction=desc[j]
                flag=False
            if(not flag):
                _serie.save()
        for k in article[j]: #按照系列依次创建文章对象
            if(Articles.objects.filter(docname=k).count()==0):
                Articles.objects.create(docname=k,setname=j,typename=i)
            else: #如果已经存在此article，尝试更新
                _article=Articles.objects.get(docname=k)
                flag=True
                if(_article.setname!=j):
                    _article.setname=j
                    flag=False
                if(_article.typename!=i):
                    _article.typename=i
                    flag=False
                if(not flag):
                    _article.save()
            
