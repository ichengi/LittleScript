# 天气信息  从网页控制台f12获取的，好多人说免费无限制使用，不管了，先用着
time_st = round(time.time())
url = f"http://d1.weather.com.cn/sk_2d/{city_id}.html?_={time_st}"

# 这里不加headers 会出现403，把请求头对比了一遍发现多了这个参数
temp_r = requests.get(url,headers={"Referer":"https://m.weather.com.cn"}) 
temp_r.encoding = "utf-8"

print(temp_r.text)

# 城市id可以从这里获取，里面有sql文件，改一下就直接入库了
# 也可以直接用里面的json数据
# http://81.70.62.148/weather_api.zip
