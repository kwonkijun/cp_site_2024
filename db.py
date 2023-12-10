import sqlite3
import pandas as pd

# SQLite 데이터베이스 연결
conn = sqlite3.connect('myblog.db')
cursor = conn.cursor()

# 블로그 테이블 생성
cursor.execute('''CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    price INTEGER NOT NULL,
    original_price INTEGER,
    discount_label INTEGER,
    new_label TEXT,
    rating REAL,
    rating_count INTEGER,
    image_path TEXT
)''')

# 데이터 프레임 생성 
df = pd.read_excel('coupang.xlsx')

# df를 products 테이블에 삽입
df.to_sql('products', conn, if_exists='append', index=False)

# 테이블에 변경 내용 저장
conn.commit()

# 연결 종료
conn.close()