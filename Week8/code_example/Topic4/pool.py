from mysql.connector import pooling

# 配置連線池參數
dbconfig = {
    "user": "root",
    "password": "8745",
    "host": "localhost",
    "database": "pool"
}

# 創建連線池
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",  # 池名稱
    pool_size=5,  # 池中最大連線數
    **dbconfig
)

# 確認連線池創建成功
print("Connection Pool Created!")

# 從連線池中獲取一個連線
connection = connection_pool.get_connection()

# 使用該連線執行 SQL 操作
cursor = connection.cursor()
cursor.execute("SELECT * FROM test_pool")

# 取得結果
result = cursor.fetchall()
for row in result:
    print(row)

# 完成操作後，關閉游標和將連線歸還給池中
cursor.close()
connection.close()

print("Connection returned to pool")
