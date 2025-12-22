import akshare as ak
from datetime import datetime, timedelta
import requests
import pandas as pd
from akshare.utils.tqdm import get_tqdm


import requests
import pandas as pd
import json

def crawl_eastmoney_financial():
    """
    爬取东方财富网指定股票的财务数据（本例为格力电器000651的业绩报表）
    """
    # 1. 定义请求的URL和请求头
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    
    # 精心构造的请求头，模拟浏览器行为，降低被反爬的风险[1,6](@ref)
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'datacenter-web.eastmoney.com',
        'Referer': 'https://data.eastmoney.com/bbsj/yjbb/000651.html', # 重要：指明请求来源[4](@ref)
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0', # 重要：模拟真实浏览器[1](@ref)
        'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    # 2. 定义查询参数
    params = {
        'callback': 'jQuery112306833715972715027_1766327583678', # JSONP回调函数名，可从原URL复制或留空
        'sortColumns': 'REPORTDATE',
        'sortTypes': '-1',
        'pageSize': '50',
        'pageNumber': '1',
        'columns': 'ALL',
        'filter': '(SECURITY_CODE="000651")', # 股票代码
        'reportName': 'RPT_LICO_FN_CPD', # 报表名称
    }

    try:
        # 3. 发送GET请求
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()  # 如果请求失败（如4xx或5xx），将抛出异常

        # 4. 处理响应：从JSONP格式转换为纯JSON
        # 响应文本通常是 jQueryxxx(...) 格式，需要去掉回调函数名和括号
        raw_text = response.text
        # 查找第一个左括号和最后一个右括号，提取其中的JSON字符串
        json_start = raw_text.find('(') + 1
        json_end = raw_text.rfind(')')
        json_str = raw_text[json_start:json_end]

        # 5. 解析JSON字符串
        data_dict = json.loads(json_str)
        
        # 6. 检查API是否成功返回数据
        if data_dict.get('result') is not None:
            # 提取核心数据列表
            data_list = data_dict['result']['data']
            print(f"成功获取到 {len(data_list)} 条数据。")
            
            # 7. 使用pandas创建DataFrame，便于查看和保存
            df = pd.DataFrame(data_list)
            
            # 8. 保存为CSV文件
            csv_filename = "格力电器_000651_业绩报表.csv"
            df.to_csv(csv_filename, index=False, encoding='utf-8-sig') # 使用utf-8-sig避免Excel打开中文乱码
            print(f"数据已成功保存到文件: {csv_filename}")
            
            # 9. 在控制台简单显示数据（可选）
            print("\n数据预览（前5行）:")
            print(df.head().to_string(index=False)) # 使用to_string美化输出
            return df
            
        else:
            print("请求成功，但API返回的数据结构异常。")
            print("原始响应:", data_dict)
            return None

    except requests.exceptions.RequestException as e:
        print(f"网络请求出错: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON数据解析出错: {e}")
        print("响应的原始文本可能是:", response.text[:500]) # 打印前500字符帮助调试
        return None
    except Exception as e:
        print(f"发生未知错误: {e}")
        return None

# 执行函数
if __name__ == "__main__":
    crawl_eastmoney_financial()