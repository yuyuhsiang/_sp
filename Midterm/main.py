import time
import requests
from threading import Thread
from bs4 import BeautifulSoup
import re

results = {}

def find_submarine_time(url, submarine_name):
    try:
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }

        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'

        soup = BeautifulSoup(res.text, 'html.parser')
        submarine = soup.find('a', {'title': submarine_name})

        if submarine:
            submarine_tr = submarine.find_parent('tr')

            time_th = None
            for table_element in submarine_tr.find_all_previous():
                if table_element.name == 'th':
                    time_element = re.compile(r'\d+:\d+:\d+')
                    if time_element.search(table_element.get_text()):
                        time_th = table_element
                        break

            if time_th:
                time_text = time_th.get_text().strip()
                result_str = f"艦艇名稱：{submarine_name}\n時間：{time_text}\n{'=' * 50}\n"
            else:
                result_str = f"艦艇名稱：{submarine_name}\n 無時間資料\n{'=' * 50}\n"
        else:
            result_str = f"艦艇名稱：{submarine_name}\n 無此艦艇\n{'=' * 50}\n"

        results[submarine_name] = result_str

    except Exception as e:
        results[submarine_name] = f"艦艇名稱：{submarine_name} 抓取失敗：{e}\n"


if __name__ == '__main__':
    print("請輸入要抓取的艦艇名稱（多個艦艇請用逗號分隔）：")
    user_input = input().strip()

    submarine_name_input = [name.strip() for name in user_input.split(',') if name.strip()]

    if not submarine_name_input:
        print("未輸入任何艦艇名稱，程式結束。")
        exit()

    target_url = "https://wiki.biligame.com/blhx/%E5%BB%BA%E9%80%A0%E6%97%B6%E9%97%B4"
    threads = []

    for i, submarine_name in enumerate(submarine_name_input, start=1):
        print(f"[{i}/{len(submarine_name_input)}] 正在抓取艦艇：{submarine_name}...")

        thread = Thread(target=find_submarine_time, args=(target_url, submarine_name))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    for name in submarine_name_input:
        print(results.get(name, f"{name} 沒有取得資料"))
