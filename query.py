from config import config
import pandas as pd

db = config()

db_name = 'back_testv2'

collection_ref = db.collection(db_name)
docs = collection_ref.stream()

# กำหนดเงื่อนไขการค้นหา
query = collection_ref.where('category', '==', 'spot').where('period', '==', '5y')

# ใช้ stream() เพื่อดึงข้อมูลที่ตรงกับเงื่อนไข
docs = query.stream()

# สร้าง DataFrame จากข้อมูลที่ได้
data = []
for doc in docs:
    data.append(doc.to_dict())

df = pd.DataFrame(data)
# print(df)

# หาผลรวมของคอลัมน์ 'profit'
total_profit = df['profit'].sum()

print("Total profit:", total_profit)