from flask import Flask, render_template
import web_ana

app = Flask(__name__)


def return_img_stream(img_local_path):
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream


@app.route('/')
def mainpage():
    total_news, total_posi, total_nega, avr_len, senti,cont_len = web_ana.mainpage()
    return render_template("index.html", total_news=total_news, total_posi=total_posi, total_nega=total_nega,
                           avr_len=avr_len, senti=senti,cont_len=cont_len)


@app.route('/web_<int:web_id>/sec_<int:sec_id>')
def section(web_id,sec_id):
    web_list = ['人民网', '中国新闻网', '光明网', '观察者网', '澎湃新闻', '新浪网']
    sec_list = ["国际","军事","经济","社会","健康","国际","时事","财经","体育","娱乐","社会","国际","军事","科技","经济","教育",
                "体育","娱乐","国际","财经","产经","科技","汽车","时事","思想","生活","财经","军事","科技","国际","社会","娱乐","体育"]
    img_path = 'static/Sec/426' + sec_id.__str__() + '.png'
    img_stream = return_img_stream(img_path)
    data,re = web_ana.sectionpage(sec_id)
    name = web_list[web_id-1]
    return render_template("section.html",img_stream=img_stream,web_name=name,sec_name = sec_list[sec_id-1],
                           news_data=data,sec_data=re)


@app.route('/web_<int:web_id>')
def web(web_id):
    web_list = ['人民网', '中国新闻网', '光明网', '观察者网', '澎湃新闻', '新浪网']
    sec_list = [[["国际",1],[ "军事",2],["经济",3],[ "社会",4],[ "健康",5]],
                [ ["国际",6],["时事",7],["财经",8],["体育",9],[ "娱乐",10],[ "社会",11]],
                [["国际",12], ["军事",13], ["科技",14],["经济",15], ["教育",16], ["体育",17],["娱乐",18]],
                [["国际",19],["军事",20],["财经",21],["产经",22],["科技",23], ["汽车",24]],
                [["时事",25],["思想",26], ["生活",27], ["财经",28]],
                [ ["军事",29],["科技",30],["国际",31], ["社会",32],["娱乐",33],["体育",34]]]
    sec_name = [["国际", "军事", "经济", "社会", "健康"],["国际","时事", "财经","体育", "娱乐","社会"],
                ["国际","军事",  "科技",  "经济",  "教育",  "体育",  "娱乐"],
                ["国际","军事","财经", "产经", "科技","汽车"],
                ["时事","思想", "生活", "财经"],
                ["军事", "科技", "国际", "社会","娱乐","体育"]]
    web_link = ['http://www.people.com.cn/', 'www.chinanews.com.cn', 'www.gmw.cn', 'www.guancha.cn', 'www.thepaper.cn', 'www.sina.com.cn']
    num,cont,senti = web_ana.webpage(web_id)
    name = sec_name[web_id-1]
    return render_template("website.html", id= web_id,web_name=web_list[web_id-1], web_link=web_link[web_id-1], sec_list=sec_list[web_id-1],sec_name=name,
                           sec_num=num,sec_cont=cont,sec_senti=senti)


@app.route('/news_<int:news_id>')
def news(news_id):
    img_path = 'static/News/' + news_id.__str__() + '.png'
    img_stream = return_img_stream(img_path)
    title,time,divide,keywords,senti,len = web_ana.newspage(news_id)
    return render_template("news.html",img_stream=img_stream,title=title,time=time,
                           divide=divide,keywords=keywords,senti=senti,len=len)