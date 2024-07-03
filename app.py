import pandas as pd

def calculate_ema(df, column, window):
    ema_column = f'EMA_{window}'
    df[ema_column] = df[column].ewm(span=window, adjust=False).mean()
    return df

# อ่านข้อมูลจากไฟล์ CSV
df = pd.read_csv('BTC-USD_6m.csv')

# ลูปคำนวณ EMA สำหรับทุกๆ window ที่ต้องการ (1 ถึง 30)
# for i in range(1, 31):
# คำนวณ EMA สำหรับ window ปัจจุบัน i
for i in range(10,31):
    df = calculate_ema(df, 'Close', i)

    # เลือกเฉพาะคอลัมน์ที่ต้องการแสดงผลและบันทึก
    # selected_columns = df[['Date', 'Close'] + [f'EMA_{j}' for j in range(1, i + 1)]]
    selected_columns = df[['Date', 'Close',f'EMA_{i}']]

    # แสดงผลลัพธ์ 5 แถวแรก
    print(selected_columns.head())

    # บันทึกผลลัพธ์ลงในไฟล์ CSV
    output_file = f'BTCUSD_6m_ema{i}.csv'
    selected_columns.to_csv(output_file, index=False)
    print(f"ผลลัพธ์ถูกบันทึกลงในไฟล์ {output_file} แล้ว")
