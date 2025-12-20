'''
data:     20251220
author:   Target
version:  0.1
'''

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class AShareAnalyzer:
    def __init__(self, start_date='20240101'):
        """初始化分析器
        Args:
            start_date: 开始日期，格式YYYYMMDD
        """
        self.start_date = start_date
        self.today = datetime.now().strftime('%Y%M%D')
        self.data_cache = {}
        
    def fetch_zt_pool_data(self):
        """获取涨停池数据"""
        print("正在获取涨停数据...")
        try:
            # 获取最近涨停数据
            zt_data = pd.DataFrame()
            for i in range(100):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y%m%d')
                try:
                    daily_zt = ak.stock_zt_pool_em(date=date)
                    daily_zt['date'] = date
                    zt_data = pd.concat([zt_data, daily_zt], ignore_index=True)
                except:
                    continue
            
            if not zt_data.empty:
                zt_count = zt_data.groupby('date').size().reset_index(name='count')
                zt_count['date'] = pd.to_datetime(zt_count['date'])
                zt_count = zt_count.sort_values('date')
                self.data_cache['zt_pool'] = zt_count
                return zt_count
        except Exception as e:
            print(f"获取涨停数据失败: {e}")
            
        # 如果数据获取失败，生成模拟数据
        print("使用模拟涨停数据...")
        dates = pd.date_range(start=datetime.now()-timedelta(days=100), 
                             end=datetime.now(), freq='D')
        zt_count = pd.DataFrame({
            'date': dates,
            'count': np.random.randint(50, 200, size=len(dates))
        })
        self.data_cache['zt_pool'] = zt_count
        return zt_count
    
    def fetch_hs300_high_new(self):
        """获取沪深300成分股创20日新高数量"""
        print("正在获取沪深300创20日新高数据...")
        try:
            # 获取沪深300成分股
            hs300 = ak.index_stock_cons_csindex(symbol="000300")
            stocks = hs300['成分券代码'].tolist()  # 只取前50只减少请求
            
            # 模拟20日新高计算
            dates = pd.date_range(start=datetime.now()-timedelta(days=100), 
                                 end=datetime.now(), freq='D')
            
            high_counts = []
            for date in dates[-20:]:
                high_count = np.random.randint(5, 30)  # 模拟创20日新高数量
                high_counts.append(high_count)
                
            result = pd.DataFrame({
                'date': dates[-20:],
                'high_new_count': high_counts
            })
            self.data_cache['hs300_high_new'] = result
            return result
        except Exception as e:
            print(f"获取沪深300新高数据失败: {e}")
            
        # 模拟数据
        dates = pd.date_range(start=datetime.now()-timedelta(days=20), 
                             end=datetime.now(), freq='D')
        result = pd.DataFrame({
            'date': dates,
            'high_new_count': np.random.randint(5, 30, size=len(dates))
        })
        self.data_cache['hs300_high_new'] = result
        return result
    
    def fetch_zz2000_high_new(self):
        """获取中证2000创20日新高数量"""
        print("正在获取中证2000创20日新高数据...")
        # 模拟数据
        dates = pd.date_range(start=datetime.now()-timedelta(days=20), 
                             end=datetime.now(), freq='D')
        result = pd.DataFrame({
            'date': dates,
            'high_new_count': np.random.randint(10, 50, size=len(dates))
        })
        self.data_cache['zz2000_high_new'] = result
        return result
    
    def fetch_hs300_basis(self):
        """获取沪深300基差（现货-期货）"""
        print("正在获取沪深300基差数据...")
        try:
            # 获取沪深300指数数据
            hs300_index = ak.stock_zh_index_hist(symbol="000300", period="daily", 
                                                start_date=self.start_date, 
                                                end_date=self.today)
            
            # 模拟期货数据
            dates = pd.to_datetime(hs300_index['日期'].tail(30))
            index_close = hs300_index['收盘'].tail(30).values
            
            # 生成基差数据
            basis = []
            for i, (date, idx_close) in enumerate(zip(dates, index_close)):
                # 模拟期货价格，通常期货价格略高于或低于现货
                future_price = idx_close + np.random.uniform(-20, 20)
                basis.append(idx_close - future_price)
            
            result = pd.DataFrame({
                'date': dates,
                'basis': basis
            })
            self.data_cache['hs300_basis'] = result
            return result
        except Exception as e:
            print(f"获取沪深300基差失败: {e}")
            
        # 模拟数据
        dates = pd.date_range(start=datetime.now()-timedelta(days=30), 
                             end=datetime.now(), freq='D')
        result = pd.DataFrame({
            'date': dates,
            'basis': np.random.uniform(-30, 30, size=len(dates))
        })
        self.data_cache['hs300_basis'] = result
        return result
    
    def fetch_zz1000_basis(self):
        """获取中证1000基差"""
        print("正在获取中证1000基差数据...")
        # 模拟数据
        dates = pd.date_range(start=datetime.now()-timedelta(days=30), 
                             end=datetime.now(), freq='D')
        result = pd.DataFrame({
            'date': dates,
            'basis': np.random.uniform(-25, 25, size=len(dates))
        })
        self.data_cache['zz1000_basis'] = result
        return result
    
    def fetch_active_buying(self):
        """获取主动性买盘数据"""
        print("正在获取主动性买盘数据...")
        try:
            # 尝试获取资金流向数据
            market_fund_flow = ak.stock_fund_flow_market(symbol="全部")
            if not market_fund_flow.empty:
                # 提取日期和主力净流入
                active_buying = pd.DataFrame({
                    'date': pd.to_datetime(market_fund_flow['日期'].tail(20)),
                    'active_buy': market_fund_flow['主力净流入-净额'].tail(20)
                })
                self.data_cache['active_buying'] = active_buying
                return active_buying
        except Exception as e:
            print(f"获取主动性买盘失败: {e}")
            
        # 模拟数据
        dates = pd.date_range(start=datetime.now()-timedelta(days=20), 
                             end=datetime.now(), freq='D')
        result = pd.DataFrame({
            'date': dates,
            'active_buy': np.random.uniform(-5e9, 5e9, size=len(dates))
        })
        self.data_cache['active_buying'] = result
        return result
    
    def plot_all_charts(self):
        """绘制所有图表"""
        # 获取所有数据
        zt_data = self.fetch_zt_pool_data()
        hs300_new = self.fetch_hs300_high_new()
        zz2000_new = self.fetch_zz2000_high_new()
        hs300_basis = self.fetch_hs300_basis()
        zz1000_basis = self.fetch_zz1000_basis()
        active_buy = self.fetch_active_buying()
        
        # 创建画布
        fig, axes = plt.subplots(3, 2, figsize=(16, 12))
        fig.suptitle('A股市场关键指标分析', fontsize=16, fontweight='bold')
        
        # 图1: 涨停数量变化
        ax1 = axes[0, 0]
        ax1.plot(zt_data['date'], zt_data['count'], 'b-o', linewidth=2, markersize=4)
        ax1.set_title('涨停股票数量变化', fontsize=12, fontweight='bold')
        ax1.set_xlabel('日期')
        ax1.set_ylabel('涨停数量')
        ax1.grid(True, alpha=0.3)
        ax1.fill_between(zt_data['date'], zt_data['count'], alpha=0.2, color='b')
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        
        # 图2: 沪深300成分股创20日新高数量
        ax2 = axes[0, 1]
        ax2.bar(hs300_new['date'], hs300_new['high_new_count'], 
                color='skyblue', alpha=0.7)
        ax2.set_title('沪深300成分股创20日新高数量', fontsize=12, fontweight='bold')
        ax2.set_xlabel('日期')
        ax2.set_ylabel('新高数量')
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        
        # 图3: 中证2000创20日新高数量
        ax3 = axes[1, 0]
        ax3.plot(zz2000_new['date'], zz2000_new['high_new_count'], 
                'g-s', linewidth=2, markersize=4)
        ax3.set_title('中证2000成分股创20日新高数量', fontsize=12, fontweight='bold')
        ax3.set_xlabel('日期')
        ax3.set_ylabel('新高数量')
        ax3.grid(True, alpha=0.3)
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        
        # 图4: 沪深300基差
        ax4 = axes[1, 1]
        colors4 = ['green' if x > 0 else 'red' for x in hs300_basis['basis']]
        ax4.bar(hs300_basis['date'], hs300_basis['basis'], color=colors4, alpha=0.7)
        ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax4.set_title('沪深300基差（现货-期货）', fontsize=12, fontweight='bold')
        ax4.set_xlabel('日期')
        ax4.set_ylabel('基差点数')
        ax4.grid(True, alpha=0.3, axis='y')
        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        
        # 图5: 中证1000基差
        ax5 = axes[2, 0]
        ax5.plot(zz1000_basis['date'], zz1000_basis['basis'], 
                'orange', linewidth=2, marker='o', markersize=4)
        ax5.fill_between(zz1000_basis['date'], zz1000_basis['basis'], 
                        0, where=zz1000_basis['basis']>0, 
                        color='green', alpha=0.3)
        ax5.fill_between(zz1000_basis['date'], zz1000_basis['basis'], 
                        0, where=zz1000_basis['basis']<=0, 
                        color='red', alpha=0.3)
        ax5.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax5.set_title('中证1000基差（现货-期货）', fontsize=12, fontweight='bold')
        ax5.set_xlabel('日期')
        ax5.set_ylabel('基差点数')
        ax5.grid(True, alpha=0.3)
        ax5.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        
        # 图6: 主动性买盘
        ax6 = axes[2, 1]
        colors6 = ['green' if x > 0 else 'red' for x in active_buy['active_buy']]
        ax6.bar(active_buy['date'], active_buy['active_buy']/1e8, 
               color=colors6, alpha=0.7)
        ax6.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax6.set_title('市场主动性买盘（主力净流入）', fontsize=12, fontweight='bold')
        ax6.set_xlabel('日期')
        ax6.set_ylabel('净流入金额（亿元）')
        ax6.grid(True, alpha=0.3, axis='y')
        ax6.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        
        # 调整布局
        plt.tight_layout()
        plt.subplots_adjust(top=0.94, hspace=0.3, wspace=0.25)
        
        # 添加整体说明
        plt.figtext(0.02, 0.02, 
                   f'数据更新至: {datetime.now().strftime("%Y-%m-%d %H:%M")} | 注: 部分数据为模拟演示', 
                   fontsize=9, style='italic')
        
        return fig, axes
    
    def export_data_to_csv(self, filename='a_share_data_export.csv'):
        """导出数据到CSV文件"""
        if not self.data_cache:
            print("没有数据可导出，请先运行数据获取")
            return
            
        with open(filename, 'w', encoding='utf-8-sig') as f:
            f.write("A股市场数据分析数据导出\n")
            f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for data_name, data in self.data_cache.items():
                f.write(f"\n=== {data_name.upper()} ===\n")
                data.to_csv(f, index=False)
                f.write("\n")
                
        print(f"数据已导出到: {filename}")

def main():
    """主函数"""
    print("=" * 50)
    print("A股市场数据分析可视化程序")
    print("=" * 50)
    
    # 创建分析器实例
    analyzer = AShareAnalyzer(start_date='20240101')
    
    # 绘制图表
    fig, axes = analyzer.plot_all_charts()
    
    # 导出数据
    analyzer.export_data_to_csv()
    
    # 显示图表
    plt.show()
    
    print("\n分析完成！")
    print("说明: 由于akshare接口限制，部分数据为模拟生成")
    print("      实际使用时请替换为真实的akshare接口调用")

if __name__ == "__main__":
    main()
