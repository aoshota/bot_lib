import requests
import datetime

# 現在のローソク足情報を取得(現在の値なので変動する可能性あり)
# symnol:GMOコインAPIの通貨名称
# interval:GMOコインAPIのインターバルを文字列で渡す(min,hourも含む)
# 日本時間6:00に新しい日付に変わる
def get_kline_gmo(symbol,interval):
	now_time = datetime.datetime.now().hour # 現在の時刻を取得
	if now_time < 6 : # 6時前は前日を指定する
		now_date = str((datetime.date.today()) - datetime.timedelta(days=1)).replace("-","")
	else: # 6時以降は当日を指定する
		now_date = str(datetime.date.today()).replace("-","")
	endPoint = 'https://api.coin.z.com/public'
	path     = '/v1/klines?symbol=' + symbol + '&interval=' + interval + '&date=' + now_date

	response = requests.get(endPoint + path)
	res = response.json()["data"][-1] # APIのレスポンスから最新のデータを取得
	opentime = datetime.datetime.fromtimestamp(int(response.json()["data"][-1]["openTime"][:-3])) # unixtimeをJSTに変換
	res["openTime"] = str(opentime)

	return res

# GMOコインの終値を最新のものから指定した個数取得する関数
# symnol:GMOコインAPIの通貨名称
# interval:GMOコインAPIのインターバルを文字列で渡す(min,hourも含む)
# quantity:取得する個数
# decimal:価格が所数の場合はTrue、デフォルトでFalse
def get_closes_gmo(symbol,interval,quantity,decimal=False):
	cnt = quantity
	closes = []

	now_time = datetime.datetime.now().hour
	if now_time < 6 :
		now_date = str((datetime.date.today()) - datetime.timedelta(days=1)).replace("-","")
	else:
		now_date = str(datetime.date.today()).replace("-","")
	endPoint = 'https://api.coin.z.com/public'
	path     = '/v1/klines?symbol=' + symbol + '&interval=' + interval + '&date=' + now_date

	response = requests.get(endPoint + path)
	res = response.json()["data"]
	length = len(res)
	for i in range(length):
		if decimal:
			closes.append(float(res[-1 - i]["close"]))
		else:
			closes.append(int(res[-1 - i]["close"]))
		cnt -= 1
		if cnt == 0: break
	if cnt != 0:
		now_date - datetime.timedelta(days=1)

		path     = '/v1/klines?symbol=' + symbol + '&interval=' + interval + '&date=' + now_date
		response = requests.get(endPoint + path)
		res = response.json()["data"]
		length = len(res)
		for i in range(length):
			if decimal:
				closes.append(float(res[-1 - i]["close"]))
			else:
				closes.append(int(res[-1 - i]["close"]))
			cnt -= 1
			if cnt == 0: break

	return closes
