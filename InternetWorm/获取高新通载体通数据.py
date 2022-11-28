import json
from time import sleep

import requests

# 获取载体通数据
def get_data():
    '''
    :return: list
    '''
    res = []
    url = "https://www.cdhtqyfw.cn/policydata/apartmentbase.html" # 这个地址 通过手机抓包获得
    form_data = { "pageNumber":1,"pageSize":12}
    req = requests.post(url, data=form_data)
    total = 1
    if req.status_code == 200:
        data_temp = req.json()
        total = data_temp["data"]['totalPage']
    for i in range(total):
        sleep(0.05)
        form_data = {"pageNumber": i + 1, "pageSize": 12}
        req = requests.post(url, data=form_data)
        if req.status_code == 200:
            data_temp = req.json()
            res.extend(data_temp["data"]['list'])
    with open(rf'data/高新通载体通数据.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)

def tran_excel():
    import pandas as pd
    with open(rf'data/高新通载体通数据.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df.to_excel(rf'data/高新通载体通数据.xlsx', index=False)

if __name__ == '__main__':
    get_data()
    tran_excel()