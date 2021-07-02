from django.db import models
from datetime import date

# Create your models here.

class Articles(models.Model):
    # Articles表 docname文章名 datecreate创建日期 datelast最后一次修改日期 id文章id setname文章所属的系列名 typename文章所属的分区名
    # docname并不包括后缀 也就是docname其实就是文章标题
    docname=models.CharField(max_length=40,blank=False)
    datecreate=models.DateTimeField(auto_now_add=True)#设置date字段为创建日期
    datelast=models.DateTimeField(auto_now=True)#设置datelast为最后一次修改日期
    objects=models.Manager()
    setname=models.CharField(blank=True,max_length=100)
    typename=models.CharField(blank=False,max_length=10)
    class Meta():#倒序排列
        ordering=('-datecreate',)
    #id=models.AutoField(primary_key=True) id会被自动创建
    def __str__(self):#返回描述信息
        return self.docname
class Comments(models.Model):
    #Comments表 name评论者名字 email评论者邮箱 comment评论内容 article文章id datecreate创建时间
    _database="comment"#指定使用的数据库文件
    article=models.IntegerField(blank=False)
    name=models.CharField(max_length=30,blank=False)
    email=models.EmailField()
    comment=models.CharField(max_length=1000)#最大应该是500字
    datecreate=models.DateTimeField(auto_now_add=True)
    user=models.CharField(max_length=300,blank=False)
    objects=models.Manager()
    def __str__(self):
        return self.name       
class ZoneDiary(models.Model):
    #ZoneDiary表 text内容 date发表时间 img图片列表
    _database="comment" 
    text=models.TextField()
    time=models.DateTimeField(auto_now_add=True)
    img=models.TextField(null=True)
    class Meta():#倒序排列
        ordering=('-time',)
    def __str__(self):
        return self.text
class Series(models.Model):
    #Series表 series系列名 typename类别名 time创建时间 introduction介绍
    series=models.TextField(max_length=30,blank=False)
    time=models.DateTimeField(auto_now_add=True)
    typename=models.TextField(max_length=10,blank=False) 
    introduction=models.TextField(max_length=200,blank=False)
    objects=models.Manager()
    def __str__(self):
        return self.series       
class Blocks(models.Model):
    #Blocks表 用来存储分区名
    blocks=models.TextField(max_length=20,blank=False)
    objects=models.Manager()
    def __str__(self):
        return self.blocks

class Prefers(models.Model):
    #Prefers表 prefer点赞数 explore浏览数 article所属文章
    _database="comment"
    prefer=models.PositiveIntegerField()
    explore=models.PositiveIntegerField()
    article=models.IntegerField(blank=False)       