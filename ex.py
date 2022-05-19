from packages import kline

# GMOコインの現在のローソク足を取得する関数
# current_kline = kline.get_kline_gmo("BTC_JPY","15min")
# print(current_kline)

# GMOコインの終値を指定個数取得する関数
closes = kline.get_closes_gmo("BTC_JPY","15min",20)
print(closes)
# 価格が少数の場合はdecimal=Trueとする
closes = kline.get_closes_gmo("XRP_JPY","15min",20,decimal=True)
print(closes)
