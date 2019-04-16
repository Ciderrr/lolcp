import requests
import json
from bs4 import BeautifulSoup
import re
from tkinter import _flatten
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def getHTMLText(url):
    try:
        r = requests.get(url,timeout=20)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getSummonerName(urlName,kv,nlist):
    try:
        r = requests.get(urlName,headers=kv,timeout=20)
        r.raise_for_status()
        entries = r.json()['entries']    # 读取json格式的数据
        for i in range(len(entries)):
            names = entries[i]['summonerName']        # 获得summonerName属性的所有内容
            nlist.append(names)
        return nlist
    except:
        return ""

def divideGroup(oldList,newList,num):        # 将一个list分为num个为一组的二维list
    try:
        for i in range(0,len(oldList),num):    # range()的三个参数：start end **step
            newList.append(oldList[i:i+num])
        return newList
    except:
        return ""

def getMatchResult(html,rlist):    # 获取游戏结果 返回结果为二维数组
    try:
        soup = BeautifulSoup(html,'html.parser')
        results = soup.find_all("div",attrs={"class":"GameResult"})    # 找到所有的GameResult标签
        for result in results:                                           #  不可以直接用正则表达式匹配Victory Defeat Remake信息 因为html中Remake信息在标签中重复出现了
            rr = re.findall(r'Victory|Defeat|Remake',result.get_text())    # 用正则表达式过滤find_all方法获取的标签信息
            rlist.append(rr)
        return rlist
    except:
        return ""

def getMatchChampions(html,clist):
    try:
        soup = BeautifulSoup(html,"html.parser")
        allResult = soup.find_all("div",attrs={"class":"ChampionImage"})
        lst = []
        for results in allResult:       # 先得到粗略的数据 并删除其中值为空的列表
            text = results.get_text()
            if not text == "":
                lst.append(text)
        for i in lst:          # 注意到使用get_text()方法后会有换行符\n\n的存在 除去换行符
            #if i == "\n\n":
                #lst.remove(i)
            i.strip()        # 这里使用更方便的方法去除空格,换行符：str.strip()方法
        nlist = []
        for names in lst:       # 通过正则表达式匹配英雄的名称 除去正常英文名 需要注意的特例：Xin Zhao , Kai'Sa , LeBlanc , Jarvan IV , Lulu , Dr.Mundo , Nunu & Willump
            a = re.findall(r'[A-Z][a-zA-Z.\'& ]*', names)
            nlist.append(a)
        nlist = list(_flatten(nlist))    # 将二维列表直接转换为一维列表 便于下面对重复元素的去除
        for i in range(0, len(nlist), 2):       # 发现英雄名字是成对出现的 我们把偶数序号的值赋给clist达到除去相邻重复元素的目的
            clist.append(nlist[i])
        return clist
    except:
        return ""
    
def getChampionList(filePath="G:\\1.txt"):   #从txt文件中获得所有英雄的英文名list
    names = []                              #txt文件来源：https://na.leagueoflegends.com/en/game-info/champions/
    with open(filePath,'r') as f :
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')         #除去换行符\n
            names.append(line)
        f.close()
    return names


def digitalTransform(rlist,result_index,cclist,index):
    #将比赛结果 英雄名称与序号一一对应
    try:
        winResult = []
        for result in rlist :
            winResult.append(result_index[result])
        #print(winResult)
        
        cchampionResult = []
        for names in cclist :
            left_half = names[:5]
            for name in left_half :
                cchampionResult.append(index[name])
            right_half = names[5:]
            for name in right_half :
                cchampionResult.append(index[name]+143)
        championResult = []
        divideGroup(cchampionResult,championResult,10)
        return winResult,championResult
    except:
        return "?"
    #print(championResult)
    #得到数字表示的胜负list:winResult 英雄list:championResult
    #每运行一次获得20个label，200个features


def main():
    # 初始化：
    kv = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": "RGAPI-93c31cad-b5f7-4b9c-9714-b72e053b9a66",           # 头文件 记得改这里的api_key
        "Accept-Language": "zh,zh-CN;q=0.9,zh-HK;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
            }
    api_key = "RGAPI-93c31cad-b5f7-4b9c-9714-b72e053b9a66"    # api_key每天更新
    urlName = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    
    nlist = []          # 用来记录召唤师名字的list
    clist = []          # 用来记录选用英雄的list
    rlist = []          # 用来记录胜负关系的list
    cclist = []         # 用来记录分组之后英雄的二维list
    championNames = []          # 用来记录初始英雄名字文本的list
    #变量初始化声明结束
    
    
    """
    在一场lol比赛中，10个人被均分为两队，称为红色方和蓝色方，但他们基本上只决定了双方出生位置的不同，
    整体来说是平衡的。所以不妨简单认为成我方和敌方
    截止目前，lol中共有143个英雄，我将他们标记为从1-143的数字
    在此算法中，我使用特征向量 feature vector X 属于 R^286 (我方英雄序号1-143，敌方144-286)
    所以我们可以得到特征向量的表达式：
        Xi = 1 , if a number of our team played as the hero with id i
           = 0 , otherwise
    同理我们也可以得到标签label y 属于 R ：
        Yi = 1 , if our team won the game
           = 0 , otherwise
        
    """
    

    # 将英雄英文名字与序号一一对应：
    championNames = getChampionList()
    count_champ = 1
    count_index = 1
    champ = {}   # 初始化 序号：英雄 对应的字典 作用是输入序号获得英雄名字
    index = {}   # 初始化 英雄：序号 对应的字典 作用是输入英雄名字获得序号
    result = {1:"Victory",0:"Defeat"}  # 初始化 1/0 ：Victory/Defeat 的字典 作用是输入1/0获取胜负字符串
    result_index = {"Victory":1,"Defeat":0,'Remake':0} # 初始化 Victory/Defeat ：0/1 的字典 作用是输入V/D获取对应的1/0数字 把Remake看做Defeat
    for cp in championNames :
        champ[count_index] = cp
        count_champ = count_champ +1
        index[cp] = count_champ
        count_index = count_index +1
    #print(champ)
    #print(index)
    # 英雄名字 序号对应字典创建结束

   
    num = 50  # 每次获取 num*20个feature和label   num不可大于300！！！
    names = getSummonerName(urlName, kv, nlist)
    names = names[:num]
    for i in range(len(names)):
        url = "https://www.op.gg/summoner/userName=" + names[i]
        
        #获取召唤师名字和比赛英雄记录
        html = getHTMLText(url)
        getMatchResult(html,rlist)
        rlist = list(_flatten(rlist))  # 将记录结果的二维数组拆解为一维数组 得到rlist最终结果
        #print(rlist)
        getMatchChampions(html,clist)
        divideGroup(clist,cclist,10)  # 每num个一组进行分组
        #print(cclist)      
        #获取召唤师名字和比赛记录结束
        
        
        #将比赛结果 英雄名称与序号一一对应
        winResult = []
        championResult = []
        winResult,championResult = digitalTransform(rlist,result_index,cclist,index)
        #print(winResult,championResult)
        #得到数字表示的胜负list:winResult 英雄list:championResult

        
        #将结果输出到.csv文件中
        wr = np.array(winResult)
        cr = np.array(championResult)
        np.savetxt('G:\\data\\w{}.txt'.format(i),wr,fmt = '%d',delimiter = ',')
        np.savetxt('G:\\data\\c{}.txt'.format(i),cr,fmt = '%d',delimiter = ',')

        print("已经进行了{}次".format(i+1))
        
        #清空列表 以便下一次打印
        rlist.clear()
        clist.clear()
        cclist.clear()
        winResult.clear()
        championResult.clear()
        wr = np.array([])
        cr = np.array([])
        
    print("Print End")
    #结果输出结束
    
if __name__ == '__main__':
    main()