import re  # 正则表达式提取文本
import requests  # 爬虫发送请求
import jieba
import matplotlib.pyplot as plt
import copy
import numpy as np
import heapq
from wordcloud import WordCloud
head={"User-Agent":"Mozilla/5.0"}
def gethtmltext(url):#得到网页文本
    try:
        r=requests.get(url,timeout=300,headers=head)
        r.raise_for_status()
        #r.encoding=r.apparent_encoding
        return r.text
    except:
        return''
def dbcomment(lst:list,url):#取出评论
    pat=r'''allstar([\d]{2})[\s\S]+?"short">(.+?)</span>'''
    for i in re.findall(pat,gethtmltext(url)):
        lst.append(i)
def gethaoping(lst:list):#获得好评
    tmplst=[]
    for i in lst:
        if (i[0]=='40' or i[0]=='50'):
            tmplst.append(i[1])
    return tmplst
def getchaping(lst:list):#获得差评
    tmplst=[]
    for i in lst:
        if (i[0]=='10' or i[0]=='20' or i[0]=='30'):
            tmplst.append(i[1])
    return tmplst
def fenci(lst:list,num:int):#分词
    tmplst=[]
    for i in lst:
        tmplst+=jieba.lcut(i)
    deep=copy.deepcopy(tmplst)
    for i in deep:#删除长度为1的词
        if len(i)==1:
            tmplst.remove(i)
    dic=dict()
    for i in tmplst:
        dic[i]=dic.get(i,0)+1
    lst1=heapq.nlargest(num,dic.items(),key=lambda x:x[1])
    return lst1
def wcloud(lst1,title:str):
    a=''
    for i in lst1:
        a=a+' '+i[0]
    wc=WordCloud(
        font_path='d:/p_train/simfang.ttf',
        width=600,height=450,
        scale=1,
        background_color='white',
        mode="RGB",
        max_font_size=100,
        min_font_size=20,
        max_words=50,
        random_state=None,
        prefer_horizontal=0.8,
        #colormap="hot"
    )
    wc_img=wc.generate(a)
    plt.imshow(wc_img)
    plt.show()
    wcimg=wc_img.to_image()
    wcimg.save(title+'.jpg')
def showcp(lst1):
    count=1
    for i in fenci(getchaping(lst1),3):
        for j in getchaping(lst1):
            if i[0] in j:
                print(str(count)+'.'+j)
                count+=1
def showhp(lst1):
    for i in fenci(gethaoping(lst1),3):
        for j in gethaoping(lst1):
            if i[0] in j:
                print(j)
def draw(lst:list,title:str):#画图
    tmplst=[0,0,0,0,0]
    for i in lst:
        if i[0]=='50':
            tmplst[0]+=1
        elif i[0]=='40':
            tmplst[1]+=1
        elif i[0]=='30':
            tmplst[2]+=1
        elif i[0]=='20':
            tmplst[3]+=1
        elif i[0]=='10':
            tmplst[4]+=1
    x = np.array(tmplst)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']#设置字体
    plt.pie(x,labels=['五星', '四星', '三星', '二星','一星'],explode=[0.1,0,0,0,0.1])# 设置饼图标签，以列表形式传入)
    plt.title(title)
    plt.savefig('{}.jpg'.format(title))
    #plt.show()
    plt.clf()
r1 = requests.get(url="https://book.douban.com/subject/2567698/comments/?start=220&limit=20&status=P&sort=score", headers=head)
lst1=[]#存放分数和评论
lst2=[]#存放分数和评论
lst3=[]#存放分数和评论
lst4=[]

url1='https://book.douban.com/subject/2567698/comments/?start={}&limit=20&status=P&sort=score'#三体一短评
url2='https://book.douban.com/subject/3066477/comments/?start={}&limit=20&status=P&sort=score'#三体二短评
url3='https://book.douban.com/subject/5363767/comments/?start={}&limit=20&status=P&sort=score'#三体三短评
url4='https://movie.douban.com/subject/34444648/comments?start={}&limit=20&status=P&sort=new_score'#三体动漫短评

#dbcomment(lst,url)
#draw(lst4,'三体一')
#wcloud(fenci(getchaping(lst4)))
showhp(lst4)
def total(url1,str1):
    lst1=[]
    for i in range(10):
        url=url1.format(str(i*20))
        dbcomment(lst1,url)
    draw(lst1,str1+'评分')
    wcloud(fenci(getchaping(lst1),100),str1+'差评')#修改参数中的getchaping函数为gethaoping可以绘制好评词汇词云图
    wcloud(fenci(gethaoping(lst1),100),str1+'好评')
    print(str1)
    showcp(lst1)
    showhp(lst1)
total(url1,'三体第一部')
total(url2,'三体第二部')
total(url3,'三体第三部')
total(url4,'三体动漫')
    
    
    
    
    
    
    