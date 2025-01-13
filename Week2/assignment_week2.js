console.log("Task1")
console.log("------------------------------------------------------")
function findAndPrint(messages, currentStation) {
    // 定義路線圖為樹狀結構（使用鄰接表表示）
    const metroMap = {
      Songshan: ["Nanjing Sanmin"],
      "Nanjing Sanmin": ["Taipei Arena"],
      "Taipei Arena": ["Nanjing Fuxing"],
      "Nanjing Fuxing": ["Zongshan"],
      Zongshan: ["Beimen"],
      Beimen: ["Ximen"],
      Ximen: ["Xiaonanmen"],
      Xiaonanmen: ["Chiang Kai-Shek Memorial Hail"],
      "Chiang Kai-Shek Memorial Hail": ["Guting"],
      Guting: ["Taipower Building"],
      "Taipower Building": ["Gongguan"],
      Gongguan: ["Wanlong"],
      Wanlong: ["Jingmei"],
      Jingmei: ["Dapinglin"],
      Dapinglin: ["Qizhang"],
      Qizhang: ["Xindian", "Xindian City Hall", "Xiaobitan"], // Qizhang後分支
      Xiaobitan: [],
      "Xindian City Hall": ["Xindian"],
      Xindian: [],
    };
  
    // 計算兩個車站的距離（基於 BFS）
    function distance(stationA, stationB) {
      if (!(stationA in metroMap) || !(stationB in metroMap)) {
        return Infinity; // 車站無效，返回無窮大距離
      }
  
      // 手動實現 BFS
      const visited = []; // 記錄已訪問的車站
      const queue = [[stationA, 0]]; // 模擬 BFS 隊列，包含 [車站, 距離]
  
      while (queue.length > 0) {
        const [current, dist] = queue.shift(); // 從隊列中取出元素
        if (current === stationB) {
          return dist; // 找到目標車站，返回距離
        }
  
        if (!visited.includes(current)) {
          visited.push(current); // 標記為已訪問
          for (const neighbor of metroMap[current]) {
            if (!visited.includes(neighbor)) {
              queue.push([neighbor, dist + 1]); // 加入鄰近車站
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
    Leslie: "I'm at home near Xiaobitan station.",
    Bob: "I'm at Ximen MRT station.",
    Mary: "I have a drink near Jingmei MRT station.",
    Copper: "I just saw a concert at Taipei Arena.",
    Vivian: "I'm at Xindian station waiting for you.",
  };
  
  // 測試案例
  findAndPrint(messages, "Wanlong"); // 預期輸出: Mary
  findAndPrint(messages, "Songshan"); // 預期輸出: Copper
  findAndPrint(messages, "Qizhang"); // 預期輸出: Leslie
  findAndPrint(messages, "Ximen"); // 預期輸出: Bob
  findAndPrint(messages, "Xindian City Hall"); // 預期輸出: Vivian

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
    let middleNames = [];
    let uniqueNames = [];

    for (let name of data) {
        let length = name.length;
        let middle;

        if (length === 2) {
            middle = name[1];
        } else if (length === 4) {
            middle = name[2];
        } else {
            middle = name[1];
        }

        middleNames.push(middle);
    }

    for (let name of data) {
        if (middleNames.filter(middle => middle === name[1]).length === 1) {
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