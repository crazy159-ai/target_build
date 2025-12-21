import requests
import pandas as pd
from akshare.utils.tqdm import get_tqdm


import requests
import pandas as pd
import json

def crawl_eastmoney_financial():
   
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    
    
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'datacenter-web.eastmoney.com',
        'Referer': 'https://data.eastmoney.com/bbsj/yjbb/000651.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0', # 重要：模拟真实浏览器[1](@ref)
        'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    
    params = {
        'callback': 'jQuery112306833715972715027_1766327583678',
        'sortColumns': 'REPORTDATE',
        'sortTypes': '-1',
        'pageSize': '50',
        'pageNumber': '1',
        'columns': 'ALL',
        'filter': '(SECURITY_CODE="000651")', 
        'reportName': 'RPT_LICO_FN_CPD', 
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
        print(df.describe()                      )
    
    except requests.exceptions.RequestException as e:
        print(f"网络请求出错: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON数据解析出错: {e}")
        print("响应的原始文本可能是:", response.text[:500])
        return None
    except Exception as e:
        print(f"发生未知错误: {e}")
        return None


if __name__ == "__main__":
    crawl_eastmoney_financial()