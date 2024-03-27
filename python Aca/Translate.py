# import tkinter as tk
# from tkinter import ttk
# import requests
# import json

# # LibreTranslate API 호출 함수
# def translate_text(input_text):
#     api_url = "https://libretranslate.de/translate"
#     data = {
#         "q": input_text,
#         "source": "ko",
#         "target": "en",
#         "format": "text"
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     response = requests.post(api_url, headers=headers, data=json.dumps(data))
#     if response.status_code == 200:
#         return response.json().get("translatedText", "")
#     else:
#         return "Translation Error"

# # 애플리케이션 UI 구성
# class TranslationApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Real-time Korean to English Translation App")

#         # 입력 텍스트 영역
#         self.input_text = tk.Text(self.root, height=5, width=50)
#         self.input_text.pack(pady=10)

#         # 번역 버튼
#         self.translate_button = tk.Button(self.root, text="Translate", command=self.translate)
#         self.translate_button.pack(pady=5)

#         # 번역 결과 표시 영역
#         self.translated_text = tk.Text(self.root, height=5, width=50, state='disabled')
#         self.translated_text.pack(pady=10)

#     def translate(self):
#         # 입력 텍스트 가져오기
#         input_text = self.input_text.get("1.0", "end-1c")
#         # 번역 함수 호출
#         translated = translate_text(input_text)
#         # 번역 결과 표시
#         self.translated_text.config(state='normal')
#         self.translated_text.delete("1.0", "end")
#         self.translated_text.insert("1.0", translated)
#         self.translated_text.config(state='disabled')

# # 애플리케이션 실행
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = TranslationApp(root)
#     root.mainloop()

# import tkinter as tk
# import requests
# from threading import Thread

# # LibreTranslate API 호출 함수
# def translate_text(input_text, source_lang="ko", target_lang="en"):
#     api_url = "https://libretranslate.com/translate"
#     params = {
#         "q": input_text,
#         "source": source_lang,
#         "target": target_lang,
#         "format": "text"
#     }
#     response = requests.post(api_url, data=params)
#     if response.status_code == 200:
#         return response.json().get("translatedText", "")
#     else:
#         return "Translation Error"

# # 실시간 번역 및 UI 업데이트를 위한 함수
# def update_translation(event=None):
#     text = input_text.get("1.0", "end-1c").strip()
#     if text:
#         Thread(target=lambda: translate_and_update(text)).start()

# def translate_and_update(text):
#     translated = translate_text(text)
#     translated_text.config(state='normal')
#     translated_text.delete("1.0", "end")
#     translated_text.insert("1.0", translated)
#     translated_text.config(state='disabled')

# # 애플리케이션 UI 구성
# root = tk.Tk()
# root.title("Real-time Korean to English Translation App")

# input_text = tk.Text(root, height=5, width=50)
# input_text.pack(pady=10)
# input_text.bind("<KeyRelease>", update_translation)

# translated_text = tk.Text(root, height=5, width=50, state='disabled')
# translated_text.pack(pady=10)

# root.mainloop()


import tkinter as tk
from tkinter import messagebox
import requests
from threading import Thread
import time
import re

# 마지막 키 입력 시각을 추적하기 위한 변수
last_key_press_time = time.time()

# 입력 지연 시간 (초)
input_delay = 0.5

# LibreTranslate API 호출 함수
def translate_text(input_text, source_lang="ko", target_lang="en"):
    api_url = "https://libretranslate.com/translate"
    params = {
        "q": input_text,
        "source": source_lang,
        "target": target_lang,
        "format": "text"
    }
    try:
        response = requests.post(api_url, data=params)
        if response.status_code == 200:
            return response.json().get("translatedText", "")
        else:
            return "Translation Error"
    except requests.RequestException:
        return "API Request Failed"

# 입력 검증 및 실시간 번역
def update_translation(event=None):
    global last_key_press_time
    last_key_press_time = time.time()
    text = input_text.get("1.0", "end-1c").strip()
    
    # 한글 검증
    if not re.match(r'^[\uac00-\ud7a3]+$', text.replace(" ", "")):
        messagebox.showerror("입력 에러", "한글만 입력해주세요.")
        return

    if text:
        Thread(target=lambda: debounce_translate(text)).start()

def debounce_translate(text):
    global last_key_press_time
    time.sleep(input_delay)
    if time.time() - last_key_press_time >= input_delay:
        translated = translate_text(text)
        translated_text.config(state='normal')
        translated_text.delete("1.0", "end")
        translated_text.insert("1.0", translated)
        translated_text.config(state='disabled')

# 애플리케이션 UI 구성
root = tk.Tk()
root.title("Real-time Korean to English Translation App")

input_text = tk.Text(root, height=5, width=50)
input_text.pack(pady=10)
input_text.bind("<KeyRelease>", update_translation)

translated_text = tk.Text(root, height=5, width=50, state='disabled')
translated_text.pack(pady=10)

root.mainloop()