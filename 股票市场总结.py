# -*- coding: utf-8 -*-
"""
股票市场总结.py
用于分析股票市场模拟的交易结果，并进行可视化展示。
"""

from 市场撮合引擎 import 市场撮合引擎
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib

# 设置微软雅黑字体（需本地有该字体）
yahei_font_path = None
for font_path in font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
    if 'msyh' in font_path.lower() or 'msyh.ttc' in font_path.lower() or '微软雅黑' in font_path:
        yahei_font_path = font_path
        break
if yahei_font_path:
    yahei_font = font_manager.FontProperties(fname=yahei_font_path, size=12)
    matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
else:
    yahei_font = font_manager.FontProperties(size=12)
    matplotlib.rcParams['font.sans-serif'] = ['Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

# 市场总结分析函数
def 市场总结分析(引擎, 股票名称列表):
    print("\n===== 股票市场总结与分析 =====")
    总成交量 = 0
    总成交金额 = 0
    股票成交统计 = {名称: {'量': 0, '金额': 0, '价格': []} for 名称 in 股票名称列表}
    for 记录 in 引擎.最近成交列表:
        总成交量 += 记录['成交数量']
        总成交金额 += 记录['成交数量'] * 记录['成交价格']
        股票成交统计[记录['股票名称']]['量'] += 记录['成交数量']
        股票成交统计[记录['股票名称']]['金额'] += 记录['成交数量'] * 记录['成交价格']
        股票成交统计[记录['股票名称']]['价格'].append(记录['成交价格'])
    print(f"总成交量: {总成交量}")
    print(f"总成交金额: {总成交金额:.2f}")
    for 名称 in 股票名称列表:
        print(f"{名称} 总成交量: {股票成交统计[名称]['量']}, 总成交金额: {股票成交统计[名称]['金额']:.2f}")
    # 最新价格
    for 名称 in 股票名称列表:
        最新价 = 引擎.最新成交价(名称)
        print(f"{名称} 最新成交价: {最新价}")

    # 可视化：各股票成交量柱状图
    plt.figure(figsize=(10, 5))
    plt.bar(股票名称列表, [股票成交统计[n]['量'] for n in 股票名称列表], color=['orange','blue','green'])
    plt.title('各股票总成交量', fontproperties=yahei_font)
    plt.ylabel('成交量', fontproperties=yahei_font)
    plt.xlabel('股票名称', fontproperties=yahei_font)
    plt.tight_layout()
    plt.show()

    # 可视化：各股票成交金额柱状图
    plt.figure(figsize=(10, 5))
    plt.bar(股票名称列表, [股票成交统计[n]['金额'] for n in 股票名称列表], color=['orange','blue','green'])
    plt.title('各股票总成交金额', fontproperties=yahei_font)
    plt.ylabel('成交金额', fontproperties=yahei_font)
    plt.xlabel('股票名称', fontproperties=yahei_font)
    plt.tight_layout()
    plt.show()

    # 可视化：各股票价格动态走势
    plt.figure(figsize=(10, 5))
    for 名称 in 股票名称列表:
        plt.plot(股票成交统计[名称]['价格'], label=名称)
    plt.title('各股票成交价格动态走势', fontproperties=yahei_font)
    plt.ylabel('成交价格', fontproperties=yahei_font)
    plt.xlabel('成交序号', fontproperties=yahei_font)
    plt.legend(prop=yahei_font)
    plt.tight_layout()
    plt.show()

    # 可视化：各股票成交量动态走势
    plt.figure(figsize=(10, 5))
    for 名称 in 股票名称列表:
        # 生成每一时刻的累计成交量序列
        累计量 = []
        累计 = 0
        for 价格 in 股票成交统计[名称]['价格']:
            索引 = 股票成交统计[名称]['价格'].index(价格)
            累计 += 引擎.最近成交列表[索引]['成交数量'] if 引擎.最近成交列表[索引]['股票名称'] == 名称 else 0
            累计量.append(累计)
        plt.plot(累计量, label=名称)
    plt.title('各股票成交量动态走势', fontproperties=yahei_font)
    plt.ylabel('累计成交量', fontproperties=yahei_font)
    plt.xlabel('成交序号', fontproperties=yahei_font)
    plt.legend(prop=yahei_font)
    plt.tight_layout()
    plt.show()

    print("\n【说明】如果股票价格长期不发生变化，可能原因如下：")
    print("1. 买卖双方的委托价格始终无法成交（买价低于卖价），导致没有实际成交，价格停滞。")
    print("2. 市场参与者行为过于保守或出价机制设置不合理，导致撮合失败。")
    print("3. 发行人或股民的信心值、资金、持仓等参数未能驱动价格波动。")
    print("4. 可以检查主循环和委托生成逻辑，确保有足够的价格浮动和成交")
