import pandas as pd
from config import config

db = config()
db_name = 'back_testv2'
# อ่านข้อมูลจาก Collection ที่ชื่อว่า 'backtesting'
collection_ref = db.collection(db_name)
docs = collection_ref.stream()

period = '6m'
ema = 'EMA_10'
# อ่านข้อมูลจากไฟล์ CSV
df = pd.read_csv(f'BTCUSD_{period}_ema10.csv')

# คำนวณ EMA สำหรับทุกๆ window ที่ต้องการ (ในที่นี้ใช้ EMA 15 เท่านั้น)
# df[ema] = df['Close'].ewm(span=15, adjust=False).mean()

# ตัวแปรสำหรับบันทึกสถานะและกำไรขาดทุน
in_long_position = False  # ตัวแปรเพื่อเก็บสถานะการถือ long
in_short_position = False  # ตัวแปรเพื่อเก็บสถานะการถือ short
investment = 1000  # จำนวนเงินที่ลงทุน
total_long_profit_percentage = 0
total_short_profit_percentage = 0
buy_price = 0
sell_price = 0
in_position = False

total_profit = 0  # ตัวแปรสำหรับรวมกำไรทั้งหมด

crossover_points = []

for i in range(1, len(df)):
    #Long
    if (df[ema][i - 1] > df['Close'][i - 1]) and (df['Close'][i] > df[ema][i]):
        print(df[ema][i])
        if not in_position:
            buy_price = df['Close'][i]
            in_position = True

    # #Short
    elif (df[ema][i - 1] < df['Close'][i - 1]) and (df['Close'][i] < df[ema][i]):
        # Take profit
        if in_position:
            in_position = False
            sell_price = df['Close'][i]

            # คำนวณจำนวน Bitcoin ที่ซื้อได้
            btc_bought = investment / buy_price

            # คำนวณจำนวนเงินที่ได้จากการขาย
            sell_amount = btc_bought * sell_price

            # คำนวณกำไร
            total_short_profit_percentage = sell_amount - investment
            total_profit += sell_amount - investment

            data = {
                'category': 'spot',
                'bought': btc_bought,
                'amount': sell_amount,
                'profit': sell_amount - investment,
                'period': period,
                'ema':ema
            }

            #  เพิ่มข้อมูลเข้าไปใน Collection 'backtesting'
            db.collection(db_name).add(data)
            print(f"จำนวน Bitcoin ที่ซื้อได้: {btc_bought:.8f} BTC")
            print(f"จำนวนเงินที่ได้จากการขาย: {sell_amount:.2f} บาท")
            print(f"กำไรที่ได้: {total_short_profit_percentage:.2f} บาท")

# print(f'profit: {total_profit}')
# print('OK')