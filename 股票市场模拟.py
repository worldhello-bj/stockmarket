import random
from time import sleep

class 股民:  
    def __init__(self, name, free_money, confidence):
        self.name = name
        self.free_money = free_money
        self.confidence = confidence
        self.资产 = {}  # 资产：{股票名: 持有数量}

    def buying(self, stock, buy_amount, 买入信号):
        if not 买入信号:
            print(f"{self.name}买入信号未触发，未买入：{stock.name}")
            return False
        if buy_amount * stock.price <= self.free_money and buy_amount > 0:
            self.free_money -= buy_amount * stock.price
            self.资产[stock.name] = self.资产.get(stock.name, 0) + buy_amount
            print(f"{self.name}买入股票：{stock.name} 买入数量：{buy_amount} 买入金额：{buy_amount * stock.price}")
            return True
        else:
            print(f"{self.name}买入股票金额超过可用资金或买入数量为0，买入失败：{stock.name}")
            return False

    def consider(self, stock, price_dict):
        买入信号 = False
        buy_amount = 0
        持仓市值 = 0
        for name, num in self.资产.items():
            持仓市值 += num * price_dict.get(name, 0)
        all_money = self.free_money + 持仓市值
        if all_money == 0:
            all_money = self.free_money
        if 100 * self.free_money / all_money > 100 - self.confidence:
            买入信号 = True
            buy_amount = int(random.randint(int(self.confidence), 100) * 0.01 * self.free_money / stock.price)
            print(f"{self.name}考虑买入股票：{stock.name} 买入数量：{buy_amount}")
        return 买入信号, buy_amount, stock.name

    def selling(self, stock, sell_amount, 卖出信号):
        if not 卖出信号:
            print(f"{self.name}卖出信号未触发，未卖出：{stock.name}")
            return False
        持有数量 = self.资产.get(stock.name, 0)
        if sell_amount > 0 and 持有数量 >= sell_amount:
            self.free_money += sell_amount * stock.price
            self.资产[stock.name] -= sell_amount
            print(f"{self.name}卖出股票：{stock.name} 卖出数量：{sell_amount} 卖出金额：{sell_amount * stock.price}")
            if self.资产[stock.name] == 0:
                del self.资产[stock.name]
            return True
        else:
            print(f"{self.name}卖出失败，持有数量不足或卖出数量为0：{stock.name}")
            return False

    def show_assets(self):
        print(f"{self.name}当前自由资金：{self.free_money}")
        print(f"{self.name}当前持仓：{self.资产}")

# 创建股民列表，分配编号
股民列表 = [股民(f"股民{i+1}", free_money=random.randint(10000, 50000), confidence=random.randint(50, 100)) for i in range(10)]

# 其余代码保持不变


class 股票:  
    def __init__(self, name, price, amount):  
        self.name = name  
        self.price = price  
        self.amount = amount

# 假设有多只股票
股票列表 = [
    股票("地产股", random.randint(50, 150), random.randint(100, 1000)),
    股票("科技股", random.randint(80, 200), random.randint(50, 500)),
    股票("医药股", random.randint(60, 180), random.randint(80, 800))
]
ticks=0
while ticks<1000:
    # 随机更新每只股票的价格和数量
    price_dict = {}
    for stock in 股票列表:
        stock.price = random.randint(50, 200)
        stock.amount = random.randint(50, 1000)
        price_dict[stock.name] = stock.price

    # 每个股民都进行买入/卖出决策
    for 当前股民 in 股民列表:
        当前股票 = random.choice(股票列表)
        买入信号, buy_amount, stock_name = 当前股民.consider(当前股票, price_dict)
        卖出信号 = random.choice([True, False])  # 示例：随机生成卖出信号

        if 买入信号:
            当前股民.buying(当前股票, buy_amount, 买入信号)
        else:
            print("买入信号未触发，未买入股票")

        持有数量 = 当前股民.资产.get(当前股票.name, 0)
        if 持有数量 > 0:
            当前股民.selling(当前股票, 持有数量 // 2, 卖出信号)
        else:
            print("没有持仓，无需卖出")
        当前股民.show_assets()
    ticks=ticks+1
    for 当前股民 in 股民列表:
        当前股民.show_assets()
