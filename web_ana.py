import pymysql


def mainpage():
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='news_data', charset='utf8mb4')
    myCursor = conn.cursor()
    sql_total_news = "SELECT count(news_id) FROM newstosection,sectiontoweb where newstosection.news_id >= 4240000 and newstosection.news_id < 4280000 " \
                     "and newstosection.sec_id = sectiontoweb.sec_id group by web_id order by web_id;"
    myCursor.execute(sql_total_news)
    total_news = []
    num_news = myCursor.fetchall()
    for n in num_news:
        total_news.append(n[0])
    sql_total_posi = "select count(news_ana.news_id) from news_ana,newstosection,sectiontoweb " \
                     "where news_ana.news_id = newstosection.news_id and newstosection.sec_id = sectiontoweb.sec_id " \
                     "and news_ana.news_id >= 4240000 and news_ana.news_id < 4280000 and news_ana.senti >= 0.5 " \
                     "group by web_id order by web_id;"
    myCursor.execute(sql_total_posi)
    total_posi = []
    posi_news = list(myCursor.fetchall())
    for n in posi_news:
        total_posi.append(n[0])
    sql_total_nega = "select count(news_ana.news_id) from news_ana,newstosection,sectiontoweb " \
                     "where news_ana.news_id = newstosection.news_id and newstosection.sec_id = sectiontoweb.sec_id " \
                     "and news_ana.news_id >= 4240000 and news_ana.news_id < 4280000 and news_ana.senti <= 0.5 " \
                     "group by web_id order by web_id;"
    myCursor.execute(sql_total_nega)
    total_nega = []
    nega_news = list(myCursor.fetchall())
    for n in nega_news:
        total_nega.append(n[0])
    sql_total_len = "select avg(news_ana.cont_len) from news_ana,newstosection,sectiontoweb " \
                    "where news_ana.news_id = newstosection.news_id and newstosection.sec_id = sectiontoweb.sec_id " \
                    "and news_ana.news_id >= 4240000 and news_ana.news_id < 4280000 group by web_id order by web_id;"
    myCursor.execute(sql_total_len)
    total_len = []
    len_news = myCursor.fetchall()
    for n in len_news:
        total_len.append(float(n[0]))
    senti = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    cont_len = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    date = 420
    while date < 427:
        day1 = date * 100
        day2 = (date + 1) * 100
        sql_total_senti = "select avg(cont_len),avg(senti),web_id from ana_result,sectiontoweb where ana_result.sec_id = sectiontoweb.sec_id " \
                          "and ana_result.re_id >= " + day1.__str__() + " and ana_result.re_id < " + day2.__str__() + " group by web_id;"
        myCursor.execute(sql_total_senti)
        total_senti = myCursor.fetchall()
        for t in total_senti:
            ind = t[2] - 1
            senti[ind][date - 420] = round(t[1], 2)
            cont_len[ind][date - 420] = round(t[0], 2)
        date = date + 1

    return total_news, total_posi, total_nega, total_len, senti, cont_len


def newspage(id):
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='news_data', charset='utf8mb4')
    myCursor = conn.cursor()
    sql_news1 = "select news_title,news_time from news where news_id = " + id.__str__() + ";"
    myCursor.execute(sql_news1)
    news_info = myCursor.fetchall()
    news = news_info[0]
    title = news[0]
    time = news[1]
    sql_divide = "select * from news_divide where news_id = " + id.__str__() + ";"
    myCursor.execute(sql_divide)
    news_divide = myCursor.fetchall()
    divide = news_divide[0]
    sql_ana = "select * from news_ana where news_id = " + id.__str__() + ";"
    myCursor.execute(sql_ana)
    news_ana = myCursor.fetchall()
    ana = news_ana[0]
    senti = ana[1]
    len = ana[2]
    return title, time, divide[1], divide[2], senti, len


def sectionpage(id):
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='news_data', charset='utf8mb4')
    myCursor = conn.cursor()
    sql_news1 = "select news.news_id,news_title,news_time,senti,cont_len from news,newstosection,news_ana where news.news_id = news_ana.news_id " \
                "and news.news_id = newstosection.news_id and sec_id = "+id.__str__()+" and news.news_id >= 4260000 limit 15 ; "
    myCursor.execute(sql_news1)
    news_info = myCursor.fetchall()
    news_data = news_info
    sql_news1 = "select * from ana_result where sec_id = " + id.__str__() + " ; "
    myCursor.execute(sql_news1)
    sec_data = myCursor.fetchall()
    re = sec_data[6]
    return news_data,re


def webpage(id):
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='news_data', charset='utf8mb4')
    myCursor = conn.cursor()
    sql_news1 = "SELECT news_num,cont_len,senti FROM news_data.ana_result,sectiontoweb where ana_result.sec_id = sectiontoweb.sec_id and re_id > 42600 and web_id = " +id.__str__()+" ;"
    myCursor.execute(sql_news1)
    sec_info = myCursor.fetchall()
    n = 0
    for sec in sec_info:
        n+=1
    senti = [] * n
    num = [] * n
    cont = [] * n
    for sec in sec_info:
        num.append(sec[0])
        cont.append(sec[1])
        senti.append(sec[2])
    return num,cont,senti