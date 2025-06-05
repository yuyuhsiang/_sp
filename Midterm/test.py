import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import requests
from threading import Thread, Lock
from bs4 import BeautifulSoup
import re

class SubmarineSearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("艦艇建造時間查詢工具")
        self.root.geometry("800x600")
        
        self.results = {}
        self.lock = Lock() # 儲存結果&鎖
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S)) # 主框架
        
        input_frame = ttk.LabelFrame(main_frame, text="輸入艦艇名稱", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(input_frame, text="請輸入要查詢的艦艇名稱（多個艦艇請用逗號分隔）：").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.input_entry = ttk.Entry(input_frame, width=70)
        self.input_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.search_button = ttk.Button(input_frame, text="開始查詢", command=self.start_search)
        self.search_button.grid(row=1, column=1) # 輸入條
        
        
        self.progress_var = tk.StringVar()
        self.progress_var.set("準備就緒")
        
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(progress_frame, text="狀態：").grid(row=0, column=0, sticky=tk.W)
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0)) # 進度條
        
        result_frame = ttk.LabelFrame(main_frame, text="查詢結果", padding="10")
        result_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.result_text = scrolledtext.ScrolledText(result_frame, width=80, height=25, wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S)) # 結果顯示框
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky=tk.E)
        
        ttk.Button(button_frame, text="清除結果", command=self.clear_results).grid(row=0, column=0, padx=(0, 10)) # 清除結果按鈕
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        input_frame.columnconfigure(0, weight=1)
        progress_frame.columnconfigure(1, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1) # 設定網格權重
        
    def fetch_submarine_time(self, url, submarine_name):
        """抓取單個艦艇的建造時間"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            res = requests.get(url, headers=headers, timeout=10)
            res.encoding = 'utf-8'
            
            soup = BeautifulSoup(res.text, 'html.parser')
            
            submarine_link = soup.find('a', {'title': submarine_name}) # 尋找包含指定艦艇名稱的連結
            
            if submarine_link:
                current_tr = submarine_link.find_parent('tr') # 向上尋找包含時間的 th 元素
                
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

            with self.lock:
                self.results[submarine_name] = result_str # 寫入字典

        except requests.exceptions.Timeout:
            with self.lock:
                self.results[submarine_name] = f"艦艇名稱：{submarine_name}\n抓取失敗：連線逾時\n{'=' * 50}\n"
        except Exception as e:
            with self.lock:
                self.results[submarine_name] = f"艦艇名稱：{submarine_name}\n抓取失敗：{e}\n{'=' * 50}\n"
    
    def update_progress(self, current, total, submarine_name):
        """更新進度條和狀態"""
        progress = (current / total) * 100
        self.progress_bar['value'] = progress
        self.progress_var.set(f"正在查詢：{submarine_name} ({current}/{total})")
        self.root.update_idletasks()
    
    def search_thread(self, submarine_names):
        """背景執行緒進行搜尋"""
        target_url = "https://wiki.biligame.com/blhx/%E5%BB%BA%E9%80%A0%E6%97%B6%E9%97%B4"
        
        self.results.clear() # 清空之前的結果
        
        req_info_list = []
        for submarine_name in submarine_names:
            req_info_list.append({"url": target_url, "submarine_name": submarine_name}) # 建立要抓取的艦艇清單

        threads = []
        total = len(req_info_list)
        
        self.progress_bar['maximum'] = total # 初始化進度條
        
        for i, req_info in enumerate(req_info_list, start=1):
            url = req_info.get("url")
            submarine_name = req_info.get("submarine_name")

            self.root.after(0, self.update_progress, i, total, submarine_name) # 更新進度

            req_thread = Thread(
                target=self.fetch_submarine_time,
                args=(url, submarine_name)
            )
            req_thread.start()
            threads.append(req_thread)

        for t in threads:
            t.join() # 等待所有執行緒完成

        self.root.after(0, self.display_results, req_info_list) # 在主執行緒中更新UI
    
    def display_results(self, req_info_list):
        """顯示搜尋結果"""
        self.result_text.delete(1.0, tk.END)
        
        for info in req_info_list:
            submarine_name = info["submarine_name"]
            result = self.results.get(submarine_name, f"{submarine_name} 沒有取得資料\n{'=' * 50}\n")
            self.result_text.insert(tk.END, result)
        
        self.progress_var.set(f"查詢完成！共處理 {len(req_info_list)} 個艦艇")
        self.progress_bar['value'] = self.progress_bar['maximum']
        self.search_button['state'] = 'normal' # 更新狀態
        
        self.result_text.see(1.0) # 自動滾動到頂部
    
    def start_search(self):
        """開始搜尋"""
        user_input = self.input_entry.get().strip()
        
        if not user_input:
            messagebox.showwarning("警告", "請輸入要查詢的艦艇名稱！")
            return
        
        submarine_names = [name.strip() for name in user_input.split(',') if name.strip()]
        
        if not submarine_names:
            messagebox.showwarning("警告", "未輸入任何有效的艦艇名稱！")
            return # 解析用戶輸入的艦艇名稱
        
        self.search_button['state'] = 'disabled' # 禁用搜尋按鈕避免連點
        
        self.result_text.delete(1.0, tk.END) # 清空結果區域
        
        search_thread = Thread(target=self.search_thread, args=(submarine_names,))
        search_thread.daemon = True
        search_thread.start() # 開始背景搜尋
    
    def clear_results(self):
        """清除結果"""
        self.result_text.delete(1.0, tk.END)
        self.progress_var.set("準備就緒")
        self.progress_bar['value'] = 0

def main():
    root = tk.Tk()
    app = SubmarineSearchGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()