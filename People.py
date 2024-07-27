from lxml import etree
import random
import requests  # 请求访问网站
import time
import ua_info

# 国际、军事、经济、社会、健康
usl_link = [ "http://world.people.com.cn/GB/157278/index","http://military.people.com.cn/GB/172467/index",
            "http://finance.people.com.cn/GB/70846/index", "http://society.people.com.cn/GB/136657/index",
            "http://health.people.com.cn/GB/415859/index"]
usl_prev = ["http://world.people.com.cn/","http://military.people.com.cn/","http://finance.people.com.cn/",
            "http://society.people.com.cn/","http://health.people.com.cn/"]
link_path = ["//*[@class='ej_bor']/ul/li", "//*[@class='ej_list_box clear']/ul/li","//*[@class='ej_list_box clear']/ul/li",
             "//*[@class='ej_list_box clear']/ul/li","/html/body/div/div[4]/div/div/div[1]/div[2]/ul/div"]
time_path = ["./i","./em","./em","./em","./div"]


def get_Data_link(url):
    # 降低访问速度
    time.sleep(random.random())
    rsp = requests.get(url, headers=ua_info.header)
    return rsp


def people():
    data = []
    sec = 0
    for usl in usl_link:
        for i in range(1, 50):
            rsp_link = get_Data_link(usl + i.__str__() + ".html")
            link_list, page_flag = (ana_Data_link(rsp_link,sec))
            for l in link_list:
                rsp_data = get_Data_link(usl_prev[sec] + l)
                data_one = ana_Data_cont(rsp_data,sec)
                data.append(data_one)
            if page_flag == 0:
                break
        sec+= 1
    while None in data:
        data.remove(None)
    return data


# 返回页面的link链接-people网国际板块
def ana_Data_link(cont, sec):
    # t = time.strftime("%Y-%m-%d", time.localtime())
    link_list = []
    page = 1
    html = etree.HTML(cont.text)
    # 解析当前页面list
    li = html.xpath(link_path[sec])
    for ul in li:
        ti = ul.xpath(time_path[sec]+"/text()")[0]
        if sec == 4:
            t_M = ti[7:9]
            t_D = ti[11:13]
        else:
            ti = ti.split('-')
            t_M = ti[1]
            t_D =ti[2]
        if ua_info.tM in t_M and ua_info.tD in t_D:
            link = ul.xpath("./a/@href")[0]
            link_list.append(link)
            continue
        if ua_info.tY in t_D:
            page = 0
            break
    return link_list, page


# 解析页面数据
def ana_Data_cont(cont,sec):
    cont.encoding = "GB2312"
    html = etree.HTML(cont.text)
    data_one = {}
    try:
        if sec == 4:
            title = html.xpath("//*[@class = 'title']/h2/text()")[0]
            time_t = html.xpath("//*[@class = 'artOri']/text()")[0]
            content = html.xpath("//*[@class = 'artDet']/p/text()")
        else:
            title = html.xpath("//*[@class = 'col col-1 fl']/h1/text()")[0]
            time_t = html.xpath("//*[@class= 'col-1-1 fl']/text()")[0]
            content = html.xpath("//*[@class= 'rm_txt_con cf']/p[not(@class)]/text()")
        t = ''
        data_one["title"] = title
        flag = 0
        for i in time_t:
            if i in '0123456789':
                t += i
                flag += 1
            if flag == 4 or flag == 7:
                t += '/'
                flag += 1
            if flag == 10:
                break
        data_one["time"] = t
        con = ''.join(content)
        data_one["content"] = con
        data_one["section"] = sec + 1
        return data_one
    except:
        return None
