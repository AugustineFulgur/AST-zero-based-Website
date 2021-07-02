from pydocx import PyDocX
import re
def reImage(html):
    #这个函数用来替换html文档里的<>符号 start$$$ $$$end
    html=html.replace("start$$$","<").replace("$$$end",">")
    html=html.replace("class=\"pydocx-center\"","class=\"pydocx-center\" style=\"display:block;\"")
    return html
def docx2html(filedocx):
    #要注意的是这个函数的参数不包括后缀
    rem=PyDocX.to_html(filedocx+".docx")
    return rem
def writeHtml(nextname,html):    
    #这个方法的参数也不包括后缀
    a=open(nextname+".html","w",encoding="utf-8")#open在写入中文时会自动用GBK
    a.write(html)
    a.close()
def inHtml(template,bodydocx):
    #这个方法用来将html嵌入模版html中 如此:
    # 1 模版中应该带有一对空的<style></style>
    # 2 模版中文章的部分应该有一个空的<br class="replace">
    style=re.search(r'<style>(.*)</style>',bodydocx).group(1)
    style=re.sub(r'body {.*}','',style)#去掉body的部分
    body=re.search(r'<body>(.*)</body>',bodydocx).group(1)
    template=template.replace("<style>","<style>"+style)
    template=template.replace('<br class="replace">',body)        
    return template
def docx2template(tempname,docxname,template):
    #template 模版文件名
    #docxname docx文件名
    #tempname html文件名
    #这个函数将docx文件一条龙转换成html
    temp=open(template,"r",encoding="utf-8").read()
    rem=docx2html(docxname)
    rem=reImage(rem)
    writeHtml(tempname,inHtml(temp,rem))