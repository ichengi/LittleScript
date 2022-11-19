#
import json
import re
import requests
from bs4 import BeautifulSoup


# 获取公司数据
def get_company_data(key: str, session_no: str):
    '''
    :param key: 查询公司名称
    :param session_no: sessionNo (后续可通过登录获取)
    :return:  网页文件（数据在script里面需要单独解析）
    '''
    url = f"https://www.tianyancha.com/search?key={key}&sessionNo={session_no}"
    req = requests.get(url)
    if req.status_code == 200:
        return req.text
    return None


# 获取公司列表（解析网页，获取需要的数据）
def get_company_list(data: str):
    '''
    :param data: 网页数据
    :return: list
    '''
    if data is None:
        return None
    soup = BeautifulSoup(data, 'html.parser')
    soup = soup.find_all(id="__NEXT_DATA__")[0]
    reg = r"<script id=\"__NEXT_DATA__\" type=\"application/json\">(.*?)</script>"  # 正则匹配
    m = re.search(reg, str(soup))  # 匹配
    company_list = \
    json.loads(m.group(1))["props"]["pageProps"]["dehydratedState"]["queries"][0]['state']['data']['data'][
        'companyList']  # 获取公司列表
    return company_list

# 存储原始数据为json文件（单个公司）
def save_company_data_single(data: dict, file_name: str):
    '''
    :param data: 公司数据
    :param file_name: 文件名
    :return: None
    '''
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    session_no = "1668865133.89743429" # sessionNo (后续可通过登录获取)
    key = "成都优力克信息技术有限公司" # 公司名称
    company_data = get_company_data(key, session_no) # 获取公司数据
    company_list = get_company_list(company_data) # 获取公司列表
    save_company_data_single( company_list[0],f"data/{key}.json") # 存储原始数据为json文件（单个公司）