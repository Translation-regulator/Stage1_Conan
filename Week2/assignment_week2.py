print("Task 1")
print("-------------------------------------------")
def find_and_print(messages, current_station):
    # 定義路線圖為雙向鄰接表
    metro_map = {
        "Songshan": ["Nanjing Sanmin"],
        "Nanjing Sanmin": ["Songshan", "Taipei Arena"],
        "Taipei Arena": ["Nanjing Sanmin", "Nanjing Fuxing"],
        "Nanjing Fuxing": ["Taipei Arena", "Songjiang Nanjing"],
        "Songjiang Nanjing": ["Nanjing Fuxing", "Zongshan"],
        "Zongshan": ["Songjiang Nanjing", "Beimen"],
        "Beimen": ["Zongshan", "Ximen"],
        "Ximen": ["Beimen", "Xiaonanmen"],
        "Xiaonanmen": ["Ximen", "Chiang Kai-Shek Memorial Hail"],
        "Chiang Kai-Shek Memorial Hail": ["Xiaonanmen", "Guting"],
        "Guting": ["Chiang Kai-Shek Memorial Hail", "Taipower Building"],
        "Taipower Building": ["Guting", "Gongguan"],
        "Gongguan": ["Taipower Building", "Wanlong"],
        "Wanlong": ["Gongguan", "Jingmei"],
        "Jingmei": ["Wanlong", "Dapinglin"],
        "Dapinglin": ["Jingmei", "Qizhang"],
        "Qizhang": ["Dapinglin", "Xindian City Hall", "Xiaobitan"],  # Qizhang後分支
        "Xiaobitan": ["Qizhang"],
        "Xindian City Hall": ["Qizhang", "Xindian"],
        "Xindian": ["Xindian City Hall"],
    }

    # 計算兩個車站的距離（BFS 實現）
    def distance(station_a, station_b):
        if station_a not in metro_map or station_b not in metro_map:
            return float('inf')  # 車站無效，返回無窮大距離

        visited = set()  # 用於記錄已訪問的車站
        queue = [(station_a, 0)]  # 模擬 BFS 隊列，包含 (車站, 距離)

        while queue:
            current, dist = queue.pop(0)
            if current == station_b:
                return dist  # 找到目標車站，返回距離

            if current not in visited:
                visited.add(current)  # 標記為已訪問
                for neighbor in metro_map[current]:
                    if neighbor not in visited:
                        queue.append((neighbor, dist + 1))

        return float('inf')  # 如果無法到達，返回無窮大

    closest_friend = None
    min_distance = float('inf')

    # 遍歷每個朋友的訊息
    for name, location in messages.items():
        friend_station = None

        # 從訊息中提取車站名稱
        for station in metro_map:
            if station in location:
                friend_station = station
                break

        if not friend_station:
            print(f"未找到 {name} 的車站資訊，跳過")
            continue  # 如果朋友的描述中沒有有效的車站名稱，跳過

        # 計算距離，並更新最短距離的朋友
        dist = distance(current_station, friend_station)
        if dist < min_distance:
            min_distance = dist
            closest_friend = name

    # 印出最近的朋友
    if closest_friend:
        print(closest_friend)
    else:
        print("未找到任何最近的朋友")


# 測試資料
messages = {
    "Leslie": "I'm at home near Xiaobitan station.",
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Vivian": "I'm at Xindian station waiting for you."
}

# 測試案例
find_and_print(messages, "Wanlong")  # 預期結果：Mary
find_and_print(messages, "Songshan")  # 預期結果：Copper
find_and_print(messages, "Qizhang")  # 預期結果：Leslie
find_and_print(messages, "Ximen")  # 預期結果：Bob
find_and_print(messages, "Xindian City Hall")  # 預期結果：Vivian
find_and_print(messages, "Dapinglin")  # 預期結果：Mary




print("=====================================================")
print("Task2")
print("------------------------------------------------")
def book(consultants, hour, duration, criteria):
    availability = []

    for consultant in consultants:
        consultant.setdefault("bookings", [])
        is_available = all(
            not (start < hour + duration and hour < end)
            for start, end in consultant["bookings"]
        )
        if is_available:
            availability.append(consultant)

    if not availability:
        print("No Service")
        return

    if criteria == "price":
        best = min(availability, key=lambda c: c["price"])
    elif criteria == "rate":
        best = max(availability, key=lambda c: c["rate"])

    best["bookings"].append((hour, hour + duration))
    print(best["name"])

consultants = [
    {"name": "John", "rate": 4.5, "price": 1000},
    {"name": "Bob", "rate": 3, "price": 1200},
    {"name": "Jenny", "rate": 3.8, "price": 800}
]
book(consultants, 15, 1, "price")  # Jenny
book(consultants, 11, 2, "price")  # Jenny
book(consultants, 10, 2, "price")  # John
book(consultants, 20, 2, "rate")  # John
book(consultants, 11, 1, "rate")  # Bob
book(consultants, 11, 2, "rate")  # No Service
book(consultants, 14, 3, "price")  # John

print("=====================================================")
print("Task3")
print("--------------------------------------")
def func(*data):
    middle_names = []
    
    # 依據每個名字的長度來提取中間字符
    for name in data:
        length = len(name)
        if length == 2:  # 兩個字名字取最後一個字
            middle = name[1]
        elif length == 4:  # 四個字名字取第 3 個字
            middle = name[2]
        elif length > 5:  # 超過五個字，取最接近中間的字
            middle = name[(length - 1) // 2]  # 中間字（長度為奇數）或偏左中間字（長度為偶數）
        else:  # 其他情況取第 2 個字
            middle = name[1]
        middle_names.append(middle)
    
    # 檢查每個名字的中間字符是否唯一
    for name in data:
        length = len(name)
        if length == 2:
            middle = name[1]
        elif length == 4:
            middle = name[2]
        elif length > 5:
            middle = name[(length - 1) // 2]
        else:
            middle = name[1]
        if middle_names.count(middle) == 1:
            print(name)
            return
    
    print("沒有")


func("彭大牆", "陳王明雅", "吳明")  # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花")  # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花")  # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆")  # print 夏曼藍波安
func("陳大明雅", "彭大牆", "吳明")  # print 彭大牆

print("================================================")

print("Task4")
print("------------------------------------------------")
def get_number(index):
    # 起始值為 0
    current_number = 0
    
    # 根據索引計算數列的值
    for i in range(1, index + 1):
        if i % 3 == 0:  # 如果是 3 的倍數，減 1
            current_number -= 1
        else:  # 否則加 4
            current_number += 4
    
    print(current_number)


# 測試
get_number(1)  # print 4
get_number(5)  # print 15
get_number(10) # print 25
get_number(30) # print 70


print("================================================")

print("Task5")
print("------------------------------------------------")
def find(spaces, stat, n):
    best_car = -1
    min_space = float('inf')
    
    for i, (space, status) in enumerate(zip(spaces, stat)):
        if status == 1 and space >= n:
            if space < min_space:
                min_space = space
                best_car = i

    print(best_car)

find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2)  # print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4)  # print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4)  # print 2
