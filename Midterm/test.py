import time
import requests
from threading import Thread, Lock
from bs4 import BeautifulSoup
import re

results = {}
lock = Lock() # 儲存抓取結果&安全鎖

# 每個目標的抓取執行緒
def fetch_submarine_time(url, submarine_name):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        submarine_link = soup.find('a', {'title': submarine_name}) # 尋找包含指定艦艇名稱的連結
        
        if submarine_link:
            current_tr = submarine_link.find_parent('tr') # 向上尋找包含時間的 th 元素，先找到包含艦艇的 tr，然後找前面的th
            
            time_th = None
            for prev_element in current_tr.find_all_previous():
                if prev_element.name == 'th':
                    time_pattern = re.compile(r'\d+:\d+:\d+')
                    if time_pattern.search(prev_element.get_text()):
                        time_th = prev_element
                        break # 在當前頁面中向上尋找包含時間的 th
            
            if time_th:
                time_text = time_th.get_text().strip()
                result_str = f"艦艇名稱：{submarine_name}\n時間：{time_text}\n{'=' * 50}\n"
            else:
                result_str = f"艦艇名稱：{submarine_name}\n找不到對應的時間資料\n{'=' * 50}\n"
        else:
            result_str = f"艦艇名稱：{submarine_name}\n在頁面中找不到此艦艇\n{'=' * 50}\n"

        with lock:
            results[submarine_name] = result_str # 寫入共享字典

    except Exception as e:
        with lock:
            results[submarine_name] = f"艦艇名稱：{submarine_name} 抓取失敗：{e}\n"


if __name__ == '__main__':
    print("請輸入要抓取的艦艇名稱（多個艦艇請用逗號分隔）：")
    user_input = input().strip() # 輸入要抓取的艦艇名稱
    
    submarine_names = [name.strip() for name in user_input.split(',') if name.strip()] # 解析用戶輸入的艦艇名稱
    
    if not submarine_names:
        print("未輸入任何艦艇名稱，程式結束。")
        exit()
    
    target_url = "https://wiki.biligame.com/blhx/%E5%BB%BA%E9%80%A0%E6%97%B6%E9%97%B4" # 使用固定網址
    
    req_info_list = []
    for submarine_name in submarine_names:
        req_info_list.append({"url": target_url, "submarine_name": submarine_name}) # 建立要抓取的艦艇清單

    threads = []
    total = len(req_info_list)

    for i, req_info in enumerate(req_info_list, start=1):
        url = req_info.get("url")
        submarine_name = req_info.get("submarine_name")

        print(f"[{i}/{total}] 正在抓取艦艇：{submarine_name}...") # 在主執行緒立即顯示排程進度

        req_thread = Thread(
            target=fetch_submarine_time,
            args=(url, submarine_name)
        )
        req_thread.start()
        threads.append(req_thread)

    for t in threads:
        t.join() # 等待所有執行緒完成

    for info in req_info_list:
        submarine_name = info["submarine_name"]
        print(results.get(submarine_name, f"{submarine_name} 沒有取得資料")) # 最後統一輸出結果