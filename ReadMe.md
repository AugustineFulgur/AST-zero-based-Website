# 本文是中文版的README文档 this README is written in Chinese #

## 1 项目自述 ##

### 1.1项目自述 ###
--------------------------------------------------------------
* by AugustFlugur
* 本项目基于`python3.6 amd64`、`django 3.1.4`、`pydocx 0.9.10`，是一个网站前后端的模版。
* 项目提供了一个基于django models与pydocx的docx文件转换功能，可以让用户在只需要书写word文档的情况下产出自己的博客。
* 用户可以将html内容嵌入docx文档内，但是需要将`<`与`>`替换成`start$$$`与`$$$end`。可以以此方式嵌入图片和代码，详情请看项目flash/docx下的实例docx文档。
* 项目为`pre标签`提供了一个稍微美化的css类，可以用来嵌入代码。
* 项目提供了一个博客文章的前端模版（可以直接使用），和一个简单的的网站首页模版 **（这个也是可以直接使用的，但是不建议，因为这个很丑）**。
* 本项目的一个实例是[AugustTheodor的个人博客](https://www.theodor.top)，欢迎来看。

### 1.2项目文章分区与系列 ###
--------------------------------------------------------------
在本项目中，博客有若干个分区，每个分区下有若干个系列，每个系列下有若干个文章。
分区与系列是一对多的形式，系列与文章也是一对多的形式。
分区、系列和文章名都存储在项目的数据库文件中。

因为带有一定的傻瓜性质，所以笔者简单地写了一个py文件`tdatabase.py`，用于在不使用命令行或者直接修改数据库的情况下更新数据。
这个文档在`djmodel/tdatabase.py`。
在使用时，需要在flash/docx下建立分区文件夹，然后在分区文件夹下建立对应的系列文件夹，在系列文件夹下，存放有两类文件：
1. 是作为父系列文件夹的系列描述的__desc__.txt
2. 是作为博客文档的*.docx文件。
若要给系列创建一个描述，请在系列文件夹下创建__desc__.txt文件并写入描述。
需要注意的是，所有系列文件夹下的文件名中都**不能**出现 **.docx**（扩展名除外），这是因为脚本采用了非常粗暴的替换方式，而含有.docx会导致错误替换。
在修改完毕后，直接运行tdatabase.py即可将改动上传至数据库。

## 2 项目文件构成 ##

### 2.1 项目文件构成1 静态资源 ###
--------------------------------------------------------------
+ flash/docx/ 下存放所有待转换的docx文档。
    根据1.2可知docx下一级的文件夹为分区文件夹，再下一级的文件夹为系列文件夹。

+ static/ 下存放所有静态文件，比如图片。
    由于本项目使用django搭建，所以html文档内书写（docx内是一样的）静态文件路径的方式也使用了django的方式。
    比如，引用static/A/B.jpg： 
    在html文档内可以写成`<img src={% static 'A/B.jpg' %}>`
    在docx文档内可以写成`start$$$img src={% static 'A/B.jpg' %} $$$end`

+ blog/templates/blog/article/ 下存放的是所有经过转换的docx文档
    如果更新了docx文档就需要到此目录下手动删除对应的html文档。
    当然，删除源docx文档也是一种更新，即使对于使用者而言不删除对应的html文件短期内也不会有什么坏结果。

+ blog/templates/blog/ 目录下的文件是网站一些特定页面的模板：
    **由于混杂了django的template语言，修改时请看清。**
    + theme.html 是网站的首页
    + block.html 是分区下文章系列显示的页面
    + serie.html 是系列下文章集合显示的页面
    + serienil.html 是无系列的文章集合显示的页面
    + search.html 是搜索结果的显示页面
    + \_template_.html 是docx文章转换的模版

### 2.2 项目文件构成2 数据库 ###
--------------------------------------------------------------
本项目设置了两个数据库comment.sqlite3与db.sqlite3，前者用于存储评论，后者用于存储文章分区等其他数据。
由于django Model的特性，用户可以在命令行对数据库中的数据进行修改，详情请参考django官方教程。
如果需要直接编辑数据库或者查看数据库，建议使用`SQLiteSpy`，因为它很轻量级。

## 3 项目的使用 ##
---------------------------------------------------------------
这个部分的3.2为**对django一窍不通的使用者**而设计。

### 3.1启动项目之前 ###
---------------------------------------------------------------
由于此项目仅仅是一个模板，在真正使用之前还需要在模板上填上一些属于使用者自己的东西，也就是所谓的DIY。
本节提供了需要更改的文件，并且在需要更改的内容上做了标记。
便于使用者查找，标记格式为`#@SIGN@#`+`应该填写的内容`，使用者只需要在文件中查找标记`#@SIGN@#`即可。
- **请先预览博客，也就是运行一遍项目**
- 删去flash/docx 文件夹下的内容
- 删去blog/templates/blog/article 文件夹下的所有内容
- 修改blog/templates/blog/theme.html 中标记的内容
- 修改templates/\__template__.html中标记的内容

### 3.2启动项目 ###
---------------------------------------------------------------
首先，笔者要建议使用者在有能力的情况下使用apache或者nginx等软件部署此项目，因为django自带的服务器并**不够安全**。
当然，如果使用者只是在很小的范围内使用此项目，并且愿意承担后果，可以直接启动项目，这也就是本节使用的方式。

在项目根目录（此文档所在位置）下打开命令行，输入`python manage.py runserver 0.0.0.0:80 --insecure`

在运行状态下报错的话，打开djangowebsite/settings.py，将其中的DEBUG设置为True，然后重复报错页面，就会有django自带的报错提示。
**排除完错误之后，切记将DEBUG设置回False。**
