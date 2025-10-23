import requests
from bs4 import BeautifulSoup
from datetime import datetime
import yfinance as yf

symbols = [
    ("ユカリア", "286A.T"),
    ("グリーンエナジー＆カンパニー", "1436.T"),
    ("CAICA DIGITAL", "2315.T"),
    ("デジタルホールディングス", "2389.T"),
    ("システム・ロケーション", "2480.T"),
    ("ボルテージ", "3639.T"),
    ("イーサポートリンク", "2493.T"),
    ("アステリア", "3853.T"),
    ("プロパスト", "3236.T"),
]

def get_stock_data(symbol):
    data = {}
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        info = ticker.info

        data["始値"] = hist['Open'].iloc[-1]
        data["高値"] = hist['High'].iloc[-1]
        data["安値"] = hist['Low'].iloc[-1]
        data["終値"] = hist['Close'].iloc[-1]
        data["出来高"] = hist['Volume'].iloc[-1]
        data["売買代金"] = data["終値"] * data["出来高"]

        data["PER"] = info.get('forwardPE', None)
        data["PBR"] = info.get('priceToBook', None)
        data["ROE"] = info.get('returnOnEquity', None)
        data["自己資本比率"] = info.get('debtToEquity', None)
        data["配当利回り"] = info.get('dividendYield', None)

        if data["終値"] > data["始値"]:
            data["トレンド"] = "上昇"
        elif data["終値"] < data["始値"]:
            data["トレンド"] = "下降"
        else:
            data["トレンド"] = "横ばい"

        url = f"https://finance.yahoo.co.jp/quote/{symbol}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        news = [n.get_text().strip() for n in soup.select(".topicsList_item")[:3]]
        data["好材料"] = news

    except Exception as e:
        data["error"] = str(e)

    return data

def main():
    print(f"=== 株価取得実行 {datetime.now()} ===\n")
    for name, symbol in symbols:
        stock_data = get_stock_data(symbol)
        print(f"## {name} ({symbol})")
        for k, v in stock_data.items():
            print(f"- {k}: {v}")
        print("\n----------------------\n")

if __name__ == "__main__":
    main()
