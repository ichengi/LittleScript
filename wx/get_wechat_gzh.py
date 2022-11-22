#获取微信公众号文章列表   包含：标题、简介、地址、封面图
#需求  BeautifulSoup #解析网页   selenium  # 模拟登录   psycopg # 存储数据 
#chromedriver_win32  # 谷歌浏览器驱动，selenium需要
# 注意，这里的链接是长链接，需要去文章地址获取短链接，这样微信小程序才能直接跳转
# 获取公众号图标地址  https://open.weixin.qq.com/qr/code?username={公众号的微信号}
def get_gzh(token,fakeid,count,total)->list:
  # '"name","type","synopsis", "thumb", "time", "web_url","create_time","update_time"' 
    res = []
    chro_options = Options()
    chro_options.add_experimental_option("debuggerAddress", "127.0.0.1:1557") 
    driver = webdriver.Chrome(r'chromedriver.exe', options=chro_options) # 驱动需要和电脑安装的谷歌浏览器版本一致
    for i in range(0,int(total/count)):
        sleep(1) # 避免太过频繁访问
        begin = 0 + i * 5
        url = f'https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin={begin}&count={count}&fakeid={fakeid}&type=9&query=&token={token}&lang=zh_CN&f=json&ajax=1'
        driver.get(url)
        html = driver.page_source
        sleep(1)
        soup = BeautifulSoup(html, 'lxml')
        b = soup.find(id='jfContent_pre').get_text()
        res.append[json.loads(b)]
    return res

if __name__=='__main__':
  pass
