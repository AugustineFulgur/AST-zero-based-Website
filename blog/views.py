from django.shortcuts import redirect,render
from django.http import HttpResponse,Http404,JsonResponse
from djmodel.readdoc import docx2template
from djmodel.readqueryset import query2json
from djmodel.include import *
from blog.models import *
from django.views.decorators.csrf import csrf_exempt#csrf跨域
import json
import os.path
import datetime
import re

TEMPLATE=DJANGOROOT+"/flash/template.html"#这个是文章模版的路径
DOC_ROOT=DJANGOROOT+"/flash/docx/"#docx文件的父路径
HTML_ROOT="/blog/templates/blog/article/" #中间路径 article用
time=datetime.datetime.now()
# Create your views here.
def index(request):
    if(request.method=='GET'):#当发送的请求是HTTPGET时
        diary={"diary":ZoneDiary.objects.all()[:10],"article":Articles.objects.all()[:10],"blocks":Blocks.objects.all()}
        return render(request,ROOTTHEME+"theme.html",diary)#结合一个给定的模板和一个给定的上下文字典, 并返回一个渲染后的HttpResponse对象
    return HttpResponse(status=404)    
def search(request):#处理搜索
    if(request.method=='POST' and 'search' in request.POST):
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
        result={"result":Articles.objects.filter(docname__contains=cop.sub("",request.POST['search'])),"key":request.POST['search']}
        return render(request,ROOTTHEME+"search.html",result)
def prefer(request,article_id):
    if(request.method=='GET'):
        prefers=Prefers.objects.get(article=article_id)
        prefers.prefer+=1
        prefers.save()
        return HttpResponse(status=200)          
def blocklist(request,block_name):
    if(Blocks.objects.filter(blocks=block_name).count()!=0):
        result={"serie":Series.objects.filter(typename=block_name),"blocks":block_name}
        return render(request,ROOTTHEME+"block.html",result)
def serienil(request,block_name):
    if(Blocks.objects.filter(blocks=block_name).count()!=0):
        result={"article":Articles.objects.filter(typename=block_name),"blocks":block_name}
        return render(request,ROOTTHEME+"serienil.html",result)        
def serielist(request,serie_name):
    if(Series.objects.filter(series=serie_name)!=None):
        result={"article":Articles.objects.filter(setname=serie_name),"serie":serie_name,"introduction":Series.objects.get(series=serie_name).introduction}
        return render(request,ROOTTHEME+"serie.html",result)                 
@csrf_exempt        
def ajax(request,request_type,request_arg):#处理所有blog的ajax请求
    if(request.method=='POST' and request_type=="article"):
        re=Articles.objects.all()
        if(re.count()>int(request_arg)):
        #没有人这么变态交字符串恶心人吧？没有吧没有吧？
            return JsonResponse(query2json(re[int(request_arg):int(request_arg)+10]),safe=False)
    elif(request.method=='POST' and request_type=="diary"):
        re=ZoneDiary.objects.all()
        if(re.count()>int(request_arg)):
            return JsonResponse(query2json(re[int(request_arg):int(request_arg)+10]),safe=False)    
    return HttpResponse(status=404)    
@csrf_exempt
def comment(request,request_meta):
    if(request.method=='POST'and request.POST['name']!=None and re.match(r'^([\w]+\.*)([\w]+)\@[\w]+\.\w{3}(\.\w{2}|)$', request.POST['mail'])):
        Comments.objects.create(article=int(request_meta),name=request.POST['name'],
        email=request.POST['mail'],comment=request.POST['comment'],user=request.META['HTTP_USER_AGENT'])
        return redirect('/article/'+request_meta)
    else:
        return redirect('/article/'+request_meta)       
def article(request,article_id):
    #因为这个链接里用到了变量 当查询不到的时候需要返回404
    if(article_id.isdigit()):
       if(Prefers.objects.filter(article=article_id).count()==0): #找不到文章的爱心数（也就是未生成）
            Prefers.objects.create(article=article_id,prefer=0,explore=0,id=Prefers.objects.all().count()+1)    
       comDirectory={"comments":Comments.objects.using("comment").filter(article=int(article_id)),"article":Articles.objects.get(id=int(article_id)),
       "ex_pr":Prefers.objects.get(article=article_id)}
       artic=Articles.objects.get(id=int(article_id))
       #先去查找html存不存在 如果html不存在则寻找docx 都不存在返回404
       #构造一下docx文件的路径便于后续取用
       docroot=DOC_ROOT+"/"+artic.typename+"/"+artic.setname+"/"+artic.docname
       if(os.path.exists(DJANGOROOT+HTML_ROOT+artic.docname+".html")):
            prefer=Prefers.objects.get(article=article_id)
            prefer.explore+=1
            prefer.save()
            return render(request,ROOTARTICLE+artic.docname+".html",comDirectory)
       elif(os.path.exists(docroot+".docx")):
           artic.save()#直接存储一次 这样最后一次修改时间重置
           docx2template(DJANGOROOT+HTML_ROOT+artic.docname,docroot,TEMPLATE)
           prefer=Prefers.objects.get(article=article_id)
           prefer.explore+=1
           prefer.save()
           return render(request,ROOTARTICLE+artic.docname+".html",comDirectory)
       else:
           return HttpResponse("查询的文章不存在哦。",status=404)    
    else:    
        return HttpResponse("url不合法。",status=404)