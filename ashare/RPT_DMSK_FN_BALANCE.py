from spyder_web import spyder_data
from datetime import datetime, timedelta

def balance(code,callback='jQuery112304783925121915804_17664936835648',reportname='RPT_DMSK_FN_BALANCE'):
    
    df = spyder_data(code,callback,reportname)
    return df

    #     'SECUCODE', 'SECURITY_CODE', 'INDUSTRY_CODE', 'ORG_CODE',
    #    'SECURITY_NAME_ABBR', 'INDUSTRY_NAME', 'MARKET', 'SECURITY_TYPE_CODE',
    #    'TRADE_MARKET_CODE', 'DATE_TYPE_CODE', 'REPORT_TYPE_CODE', 'DATA_STATE',
    #    'NOTICE_DATE', 'REPORT_DATE', 'TOTAL_ASSETS', 'FIXED_ASSET',
    #    'MONETARYFUNDS', 'MONETARYFUNDS_RATIO', 'ACCOUNTS_RECE',
    #    'ACCOUNTS_RECE_RATIO', 'INVENTORY', 'INVENTORY_RATIO',
    #    'TOTAL_LIABILITIES', 'ACCOUNTS_PAYABLE', 'ACCOUNTS_PAYABLE_RATIO',
    #    'ADVANCE_RECEIVABLES', 'ADVANCE_RECEIVABLES_RATIO', 'TOTAL_EQUITY',
    #    'TOTAL_EQUITY_RATIO', 'TOTAL_ASSETS_RATIO', 'TOTAL_LIAB_RATIO',
    #    'CURRENT_RATIO', 'DEBT_ASSET_RATIO', 'CASH_DEPOSIT_PBC', 'CDP_RATIO',
    #    'LOAN_ADVANCE', 'LOAN_ADVANCE_RATIO', 'AVAILABLE_SALE_FINASSET',
    #    'ASF_RATIO', 'LOAN_PBC', 'LOAN_PBC_RATIO', 'ACCEPT_DEPOSIT',
    #    'ACCEPT_DEPOSIT_RATIO', 'SELL_REPO_FINASSET', 'SRF_RATIO',
    #    'SETTLE_EXCESS_RESERVE', 'SER_RATIO', 'BORROW_FUND',
    #    'BORROW_FUND_RATIO', 'AGENT_TRADE_SECURITY', 'ATS_RATIO',
    #    'PREMIUM_RECE', 'PREMIUM_RECE_RATIO', 'SHORT_LOAN', 'SHORT_LOAN_RATIO',
    #    'ADVANCE_PREMIUM', 'ADVANCE_PREMIUM_RATIO'

    
def to_str(x):
    
    date_object = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    target_date_str = date_object.strftime('%Y:%m:%d')
    return target_date_str


if __name__ == "__main__":
    
    df = balance(601138)
    df['REPORT_DATE']=df['REPORT_DATE'].map(to_str)
    print(df.columns)
    new_df = df[['REPORT_DATE','SECURITY_CODE','TOTAL_ASSETS','FIXED_ASSET','MONETARYFUNDS','TOTAL_LIABILITIES']]
    
    new_df[['TOTAL_ASSETS','FIXED_ASSET','MONETARYFUNDS','TOTAL_LIABILITIES']]/=1e8
    new_df=new_df.rename(columns={'REPORT_DATE':'时间','SECURITY_CODE':'代码','TOTAL_ASSETS':'总资产','FIXED_ASSET':'固定资产','MONETARYFUNDS':'货币','TOTAL_LIABILITIES':'总负债'})
    print(new_df)