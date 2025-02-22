console.log("Task1")
console.log("------------------------------------------------------")
function findAndPrint(messages, currentStation) {
  // 定義路線圖為雙向鄰接表
  const metroMap = {
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
      "Qizhang": ["Dapinglin", "Xindian City Hall", "Xiaobitan"], // Qizhang後分支
      "Xiaobitan": ["Qizhang"],
      "Xindian City Hall": ["Qizhang", "Xindian"],
      "Xindian": ["Xindian City Hall"]
  };

  // 計算兩個車站的距離（BFS 實現）
  function distance(stationA, stationB) {
      if (!(stationA in metroMap) || !(stationB in metroMap)) {
          return Infinity; // 車站無效，返回無窮大距離
      }

      const visited = new Set(); // 用於記錄已訪問的車站
      const queue = [[stationA, 0]]; // 模擬 BFS 隊列，包含 [車站, 距離]

      while (queue.length > 0) {
          const [current, dist] = queue.shift(); // 從隊列中取出元素

          if (current === stationB) {
              return dist; // 找到目標車站，返回距離
          }

          if (!visited.has(current)) {
              visited.add(current); // 標記為已訪問
              for (const neighbor of metroMap[current]) {
                  if (!visited.has(neighbor)) {
                      queue.push([neighbor, dist + 1]);
                  }
              }
          }
      }

      return Infinity; // 如果無法到達，返回無窮大
  }

  let closestFriend = null;
  let minDistance = Infinity;

  // 遍歷每個朋友的訊息
  for (const [name, location] of Object.entries(messages)) {
      let friendStation = null;

      // 從訊息中提取車站名稱
      for (const station in metroMap) {
          if (location.includes(station)) {
              friendStation = station;
              break;
          }
      }

      if (!friendStation) {
          console.log(`未找到 ${name} 的車站資訊，跳過`);
          continue; // 如果朋友的描述中沒有有效的車站名稱，跳過
      }

      // 計算距離，並更新最短距離的朋友
      const dist = distance(currentStation, friendStation);
      if (dist < minDistance) {
          minDistance = dist;
          closestFriend = name;
      }
  }

  // 印出最近的朋友
  if (closestFriend) {
      console.log(closestFriend);
  } else {
      console.log("未找到任何最近的朋友");
  }
}

// 測試資料
const messages = {
  "Leslie": "I'm at home near Xiaobitan station.",
  "Bob": "I'm at Ximen MRT station.",
  "Mary": "I have a drink near Jingmei MRT station.",
  "Copper": "I just saw a concert at Taipei Arena.",
  "Vivian": "I'm at Xindian station waiting for you."
};

// 測試案例
findAndPrint(messages, "Wanlong"); // 預期結果：Mary
findAndPrint(messages, "Songshan"); // 預期結果：Copper
findAndPrint(messages, "Qizhang"); // 預期結果：Leslie
findAndPrint(messages, "Ximen"); // 預期結果：Bob
findAndPrint(messages, "Xindian City Hall"); // 預期結果：Vivian
findAndPrint(messages, "Dapinglin"); // 預期結果：Mary


  console.log("=====================================================")
  console.log("Task2")
  console.log("------------------------------------------------------")

  function book(consultants, hour, duration, criteria) {
    let availability = [];

    for (let consultant of consultants) {
        consultant.bookings = consultant.bookings || [];
        let isAvailable = consultant.bookings.every(([start, end]) => !(start < hour + duration && hour < end));
        
        if (isAvailable) {
            availability.push(consultant);
        }
    }

    if (availability.length === 0) {
        console.log("No Service");
        return;
    }

    let best;
    if (criteria === "price") {
        best = availability.reduce((prev, curr) => (prev.price < curr.price ? prev : curr));
    } else if (criteria === "rate") {
        best = availability.reduce((prev, curr) => (prev.rate > curr.rate ? prev : curr));
    }

    best.bookings.push([hour, hour + duration]);
    console.log(best.name);
}

const consultants = [
    { name: "John", rate: 4.5, price: 1000, bookings: [] },
    { name: "Bob", rate: 3, price: 1200, bookings: [] },
    { name: "Jenny", rate: 3.8, price: 800, bookings: [] }
];

book(consultants, 15, 1, "price");  // Jenny
book(consultants, 11, 2, "price");  // Jenny
book(consultants, 10, 2, "price");  // John
book(consultants, 20, 2, "rate");  // John
book(consultants, 11, 1, "rate");  // Bob
book(consultants, 11, 2, "rate");  // No Service
book(consultants, 14, 3, "price");  // John

console.log("=====================================================")
console.log("Task3")
console.log("------------------------------------------------------")

function func(...data) {
    const middleNames = [];

    // 提取每個名字的中間字
    for (const name of data) {
        const length = name.length;
        let middle;

        if (length === 2) {
            // 兩個字，取最後一個字
            middle = name[1];
        } else if (length === 4) {
            // 四個字，取第 3 個字
            middle = name[2];
        } else if (length > 5) {
            // 超過五個字，取最接近中間的字
            middle = name[Math.floor((length - 1) / 2)];
        } else {
            // 其他情況，取第 2 個字
            middle = name[1];
        }

        middleNames.push(middle);
    }

    // 檢查每個名字的中間字是否唯一
    for (const name of data) {
        const length = name.length;
        let middle;

        if (length === 2) {
            middle = name[1];
        } else if (length === 4) {
            middle = name[2];
        } else if (length > 5) {
            middle = name[Math.floor((length - 1) / 2)];
        } else {
            middle = name[1];
        }

        // 檢查中間字是否唯一
        if (middleNames.filter(m => m === middle).length === 1) {
            console.log(name);
            return;
        }
    }

    console.log("沒有");
}


func("彭大牆", "陳王明雅", "吳明");  // print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花");  // print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花");  // print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆");  // print 夏曼藍波安
func("陳大明雅", "彭大牆", "吳明"); // 印出 彭大牆

console.log("=====================================================")
console.log("Task4")
console.log("------------------------------------------------------")
function getNumber(index) {
    // 起始值為 0
    let currentNumber = 0;
    
    // 根據索引計算數列的值
    for (let i = 1; i <= index; i++) {
        if (i % 3 === 0) {  // 如果是 3 的倍數，減 1
            currentNumber -= 1;
        } else {  // 否則加 4
            currentNumber += 4;
        }
    }
    
    console.log(currentNumber);
}

// 測試
getNumber(1);  // print 4
getNumber(5);  // print 15
getNumber(10); // print 25
getNumber(30); // print 70



console.log("=====================================================")
console.log("Task5")
console.log("------------------------------------------------------")
function find(spaces, stat, n) {
    let bestCar = -1;
    let minSpace = Infinity;
    
    for (let i = 0; i < spaces.length; i++) {
        let space = spaces[i];
        let status = stat[i];
        
        if (status === 1 && space >= n) {
            if (space < minSpace) {
                minSpace = space;
                bestCar = i;
            }
        }
    }

    console.log(bestCar);
}

// 測試
find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2);  // print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4);  // print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4);  // print 2
