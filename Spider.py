import People
import GuangMing
import ChinaNews
import Sina
import GuanChaZhe
import pymysql.cursors
import ua_info
import PengPai
import time


# 保存数据
def saveData(data):
    connection = pymysql.connect(host='localhost', user='root', password='123456', db='news_data', charset='utf8mb4')
    try:
        with connection.cursor() as cursor:
            sql1 = "insert into news(news_id,news_time,news_title,news_content) values(%s,%s,%s,%s)"
            sql2 = "insert into newstosection(news_id,sec_id) values(%s,%s)"
            for di in data:
                cursor.execute(sql1, (ua_info.newsid.__str__(), di["time"], di["title"], di["content"]))
                cursor.execute(sql2,(ua_info.newsid.__str__(),di["section"]+ua_info.sec))
                ua_info.newsid += 1
            connection.commit()
    finally:
        connection.close()


def settime():
    # t = time.strftime("%m-%d", time.localtime())
    # tM = int(t[0:2])
    # tD = int(t[3:5]) - 1
    # tY = tD - 1
    # newsid = tM * 1000000 + tD * 10000
    # tM = tM.__str__()
    # tD = tD.__str__()
    # tY = tY.__str__()
    # ua_info.tM = tM
    # ua_info.tD = tD
    # ua_info.tY = tY
    # ua_info.newsid = newsid
    ua_info.tM = "4"
    ua_info.tD = "05"
    ua_info.tY = "04"
    ua_info.newsid = 4050000


def spider():
    settime()
    start = time.perf_counter()
    data = People.people()
    saveData(data)
    data.clear()
    ua_info.sec += 5
    data = ChinaNews.chinanews()
    saveData(data)
    data.clear()
    ua_info.sec += 6
    data = GuangMing.guangming()
    saveData(data)
    data.clear()
    ua_info.sec += 7
    data = GuanChaZhe.guanchazhe()
    saveData(data)
    data.clear()
    ua_info.sec += 6
    data = PengPai.pengpai()
    saveData(data)
    data.clear()
    ua_info.sec += 4
    data = Sina.sina()
    saveData(data)
    end = time.perf_counter()
    print("新闻爬取条数:", ua_info.newsid)
    print("爬虫运行耗时：", end - start)