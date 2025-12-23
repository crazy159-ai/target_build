##########
# date:20251222
# 业绩报表
##########

import requests
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import json
import matplotlib.pyplot as plt
import time
import random

class Constant:
    jQuery_Version = "1.7.2"

def get_current_timestamp() -> int:
    return int(round(time.time() * 1000))

def jquery_mock_callback() -> str:
    "jQuery" + (Constant.jQuery_Version + str(random.random())).replace(".", "") + "_" + str(get_current_timestamp() - 1000)


def spyder_data(code,call_back,report_name):
   
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    
    
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'datacenter-web.eastmoney.com',
        'Referer': f'https://data.eastmoney.com/bbsj/yjbb/{code}.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0', # 重要：模拟真实浏览器[1](@ref)
        'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'callback': call_back,
        'sortColumns': 'REPORT_DATE',
        'sortTypes': '-1',
        'pageSize': '50',
        'pageNumber': '1',
        'columns': 'ALL',
        'filter': f'(SECURITY_CODE="{code}")', 
        'reportName': report_name, 
    }

    try:
       
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()  

        
        raw_text = response.text
        
        json_start = raw_text.find('(') + 1
        json_end = raw_text.rfind(')')
        json_str = raw_text[json_start:json_end]

        
        data_dict = json.loads(json_str)
        
        data_list = data_dict['result']['data']
        df = pd.DataFrame(data_list)

        return df
    
    except requests.exceptions.RequestException as e:
        print(f"网络请求出错: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON数据解析出错: {e}")
        print("响应的原始文本可能是:", response.text)
        return None
    except Exception as e:
        print(f"发生未知错误: {e}")
        return None

if __name__ == "__main__":
    # df=spyder_data(601138,'jQuery112306833715972715027_1766327583678','RPT_LICO_FN_CPD')
    df=spyder_data(601138,'jQuery112307327050002384555_'+str(get_current_timestamp()),'RPT_DMSK_FN_BALANCE')
    
    print(df)



