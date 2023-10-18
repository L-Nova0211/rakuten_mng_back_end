def calc_sell_price(buy_price: float, count_set: int, shipping_fee: int, point:int=1, profit=500):
    sell_price = int((profit + buy_price*1.1*count_set + shipping_fee)/(0.9-point/100))
    return sell_price
