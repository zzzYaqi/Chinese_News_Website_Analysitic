import pymysql
from snownlp import SnowNLP
from jieba import analyse
import jieba
import time
import wordcloud
import ua_info
import os


def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        unicodedata.numeric(s)  # 把一个表示数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
    return False

# 去除停用词
def stopwords(cont):
    re = []
    file = "./resource/stopwords.txt"
    with open(file, "r", encoding="utf-8") as fp:
        stopword = fp.readlines()
    for c in cont:
        if c not in stopword:
            re.append(c)
    return re


def settime():
    t = time.strftime("%m-%d", time.localtime())
    tM = int(t[0:2])
    tD = int(t[3:5]) - 1
    re_id = tM * 10000 + tD * 100
    ua_info.re_id = re_id


def ana():
    # t = time.strftime("%m-%d", time.localtime())
    # tM = int(t[0:2])
    # tD = int(t[3:5]) - 1
    # day_id = tM * 100 + tD

    #
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='news_data', charset='utf8mb4')
    myCursor = conn.cursor()

    # sql_web_num = "SELECT web_id,count(news_id) FROM newstosection,sectiontoweb where news_id >= "+\
    #             newsid.__str__()+" and newstosection.sec_id = sectiontoweb.sec_id group by web_id;" # 各个网站新闻总量
    # myCursor.execute(sql_web_num)
    # web_count = myCursor.fetchall()

    # sql_sec_num = "SELECT sec_id,count(news_id) FROM newstosection where news_id >= " + \
    #               "4100000" + " group by sec_id order by sec_id;" # 各个板块新闻总量
    # myCursor.execute(sql_sec_num)
    # sec_count = myCursor.fetchall()
    # sql0 = "select sec_id,news_content from newstosection,news where newstosection.news_id = news.news_id and
    # news.news_id >= 4080000 and news.news_id < 4090000; "

    # start_ana = time.perf_counter()
    # sql_cont = "select news_id,news_content from news where news_id >=" + " 4260000 and news_id < 4270000;"
    # myCursor.execute(sql_cont)
    # data = myCursor.fetchall()  # 提取单日所有新闻
    # data_divide = []  # 存放news_divide表的所有结果
    # data_ana = []  # 存放news_ana表的所有结果
    # for d in data:  # 对当日所有单条新闻进行所有分析
    #     divide_one = {}  # 单条分词数据
    #     ana_one = {}  # 单条情感分析数据
    #     divide_one["news_id"] = d[0]
    #     ana_one["news_id"] = d[0]
    #     cont = d[1]  # 文本内容
    #     cont = cont.replace(' ', '')  # 去除噪音
    #     cont = cont.replace('\n', '')
    #     cont = cont.replace('\t', '')
    #     cont = "".join(cont)
    #     cont_len = 0
    #     for s in cont:  # 统计文字数量
    #         if '\u4e00' <= s <= '\u9fff':
    #             cont_len += 1
    #     ana_one["cont_len"] = cont_len  # 保存文字数量
    #     if cont_len != 0:
    #         divide = list(jieba.cut(cont, cut_all=False))  # 分词处理
    #         divide = stopwords(divide)  # 去除停用词
    #         re = ",".join(divide)
    #         divide_one["news_divide"] = re  # 保存分词结果
    #         keywords = jieba.analyse.extract_tags(re, topK=5, withWeight=True, allowPOS=('n', 'nr', 'ns'))  # 关键词提取
    #         key = ""
    #         for k in keywords:
    #             key += k[0] + ','
    #             key += str(round(k[1], 2)) + ','
    #         divide_one["keywords"] = key  # 保存关键词
    #         s = SnowNLP(re)  # 情感分析
    #         senti = s.sentiments  # 情感数值
    #         senti = round(senti, 4)
    #         ana_one["senti"] = senti  # 保存情感数值
    #         data_divide.append(divide_one)
    #         data_ana.append(ana_one)
    #         re = re.replace('的', '')
    # 提取所有单日新闻进行分析并保存数据

            # w = wordcloud.WordCloud(font_path="msyh.ttc",
            #                         width=400, height=400, background_color="white")   # 设置词云
            # w.generate(re) # 生成词云
            # w.to_file("./resource/News/" + d[0].__str__() + ".png")  # 保存词云图片

    # end_ana = time.perf_counter()
    # print("分析运行耗时：", end_ana - start_ana)
    # #  保存单条新闻数据
    # saveCursor = conn.cursor()
    # for di in data_divide:
    #     sql_save1 = "insert into news_divide(news_id,news_divide,keywords) values(%s,%s,%s)"
    #     saveCursor.execute(sql_save1, (di["news_id"],di["news_divide"],di["keywords"]))
    # for an in data_ana:
    #     sql_save2 = "insert into news_ana(news_id,senti,cont_len) values(%s,%s,%s)"
    #     saveCursor.execute(sql_save2, (an["news_id"], an["senti"], an["cont_len"]))
    # conn.commit()

    # dayid = 420
    # date = 20
    # # 对整个板块数据进行分析
    # while dayid < 427:
    #     n = 34  # 共34个板块
    #     sec_num = [0] * n
    #     sec_cont_len = [0] * n
    #     sec_senti = [0] * n
    #     # 查询各个板块的新闻数量
    #     sqlid0 = dayid*10000
    #     sqlid1 = (dayid+1)*10000
    #     sql_num = "select count(news_id),sec_id from newstosection where news_id >= "+sqlid0.__str__()+" and news_id < "+sqlid1.__str__()+\
    #               " group by sec_id order by sec_id;"
    #     myCursor.execute(sql_num)
    #     news_num = myCursor.fetchall()
    #     for num in news_num:
    #         sec_num[num[1]-1] += int(num[0])
    #     # 查询各个板块的平均文本长度
    #     sql_len = "select avg(cont_len),sec_id from news_ana,newstosection where news_ana.news_id = newstosection.news_id " \
    #               "and news_ana.news_id >= "+sqlid0.__str__()+" and news_ana.news_id <"+sqlid1.__str__()+" group by sec_id order by sec_id;"
    #     myCursor.execute(sql_len)
    #     news_cont = myCursor.fetchall()
    #     for cont in news_cont:
    #         sec_cont_len[cont[1]-1] = cont[0]
    #     # 查询各个板块的平均情感指数
    #     sql_senti = "select avg(senti),sec_id from news_ana,newstosection where news_ana.news_id = newstosection.news_id " \
    #                 "and news_ana.news_id >= "+sqlid0.__str__()+" and news_ana.news_id < "+sqlid1.__str__()+ " group by sec_id order by sec_id;"
    #     myCursor.execute(sql_senti)
    #     news_senti = myCursor.fetchall()
    #     for s in news_senti:
    #         sec_senti[s[1]-1] = s[0]
    #     saveCursor = conn.cursor()
    #     day = "2022-04-"+date.__str__()
    #     for i in range(0,34):
    #         re = dayid*100+i+1
    #         sql_save0 = "insert into ana_result(re_id,sec_id,time,news_num,cont_len,senti) values(%s,%s,%s,%s,%s,%s)"
    #         saveCursor.execute(sql_save0, (re,i+1,day,sec_num[i],sec_cont_len[i],sec_senti[i]))
    #     conn.commit()
    #     date = date +1
    #     dayid = 400 + date

    sql_num = "select keywords,sec_id from news_divide,newstosection where news_divide.news_id = newstosection.news_id " \
              "and news_divide.news_id >= 4260000 order by sec_id;"
    myCursor.execute(sql_num)
    data_divide = myCursor.fetchall()
    # 制作板块词云
    sec_key_cont = [""] * 34
    for d in data_divide:
        sec = d[1] - 1
        sp = d[0].split(',')
        for s in sp:
            if is_number(s):
                continue
            sec_key_cont[sec] = sec_key_cont[sec] +","+ s
    count = 1
    for wc in sec_key_cont:
        w = wordcloud.WordCloud(font_path="msyh.ttc",
                                width=800, height=400, background_color="white")   # 设置词云
        w.generate(wc) # 生成词云
        w.to_file("./resource/Sec/426" + count.__str__() + ".png")  # 保存板块词云图片
        count = count+1

    conn.close()


