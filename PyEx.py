from pytube import YouTube
from bs4 import BeautifulSoup
from urllib import parse
from googleapiclient.discovery import build  # API를 호출할 함수 제작
import time
import requests
import tkinter
import os


class PyEx:
    def __init__(self):
        # GUI 세팅
        self.TK = tkinter.Tk()
        self.TK.title("파이익스")
        self.Frame_Container = tkinter.Frame(self.TK)

        self.Listbox_frame = tkinter.Frame(self.Frame_Container)
        self.Selectbox_frame = tkinter.Frame(self.Frame_Container)
        self.check_Value1 = tkinter.BooleanVar()
        self.check_Value2 = tkinter.BooleanVar()

        # 리스트 박스 요소들
        self.List_box = tkinter.Listbox(
            self.Listbox_frame, width=70, height=20)

        self.lbl = tkinter.Label(
            self.Listbox_frame, text="검색어 입력", width=12, pady=5)

        self.txt = tkinter.Entry(self.Listbox_frame, width=46)
        self.txt.bind("<Return>", self.video_search)

        self.btn = tkinter.Button(
            self.Listbox_frame, text="검색", width=9, command=self.video_search, borderwidth=1)

        # 셀렉트 박스 요소들
        self.select_summary = tkinter.Label(
            self.Selectbox_frame, text="추출할 영상을 골라주세요!")
        self.select_entry = tkinter.Entry(
            self.Selectbox_frame, width=25)
        self.select_button = tkinter.Button(
            self.Selectbox_frame, text="영상 선택", width=17, command=self.select_video)
        self.sound_extract_button = tkinter.Button(
            self.Selectbox_frame, text="추출 시작", width=17, height=5, command=self.extract_video)
        self.extract_option_mp3 = tkinter.Checkbutton(
            self.Selectbox_frame, text="음원", var=self.check_Value1)
        self.extract_option_mp4 = tkinter.Checkbutton(
            self.Selectbox_frame, text="영상", var=self.check_Value2)
        self.mp3_success = tkinter.Label(
            self.Selectbox_frame, text="음원 추출 성공!")
        self.mp4_success = tkinter.Label(
            self.Selectbox_frame, text="영상 추출 성공!")

        # 유튜브 API 키
        API_KEY = "AIzaSyAuxoo9kr49sbv4r3lcX6o2BhHPSwEOuRg"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        self.youtube_data = build(YOUTUBE_API_SERVICE_NAME,
                                  YOUTUBE_API_VERSION, developerKey=API_KEY)

        # 영상 목록 딕셔너리
        self.video_dict = {}

    def video_search(self, event=None):
        self.video_dict.clear()
        self.List_box.delete(0, 14)
        user_input = self.txt.get()

        search_response = self.youtube_data.search().list(
            # - q : 검색어
            # - order : 정렬방법
            # - part : 필수 매개변수
            # - maxResults : 결과개수
            # 공식문서 - https://developers.google.com/youtube/v3/docs/search/list?hl=ko

            q=user_input,
            order="relevance",
            part="snippet",
            maxResults=15
        ).execute()

        for number, video in enumerate(search_response["items"]):
            try:
                video_title = video["snippet"]["title"]
                video_id = video["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                self.video_dict[video_title] = video_url
                self.List_box.insert(number, video_title)
            except KeyError:
                pass

    def select_video(self):
        try:
            self.title = self.select_entry.get()
            url = self.video_dict[self.title]
            self.yt = YouTube(url)
        except KeyError:
            pass

    def extract_video(self, route="추출"):
        if self.check_Value1.get() == True:
            self.yt.streams.filter(only_audio=True).first().download(route)
            self.mp4_success.forget()
            self.mp3_success.place(x=52, y=260)

        if self.check_Value2.get() == True:
            self.yt.streams.filter(
                progressive=True, file_extension='mp4').first().download(route)
            self.mp3_success.forget()
            self.mp4_success.place(x=52, y=260)

    def packing(self):
        # GUI 패킹
        self.Frame_Container.pack()
        self.Listbox_frame.pack(side=tkinter.LEFT, padx=10, pady=(10, 4))
        self.List_box.pack()
        self.lbl.pack(side=tkinter.LEFT, pady=(4, 0))
        self.txt.pack(side=tkinter.LEFT, pady=(4, 0))
        self.btn.pack(side=tkinter.RIGHT, pady=(4, 0))
        self.Selectbox_frame.pack()
        self.select_summary.pack(padx=(0, 9), pady=(10, 5))
        self.select_entry.pack(padx=(0, 10))
        self.select_button.pack(pady=10)
        self.sound_extract_button.pack(pady=(40, 0))
        self.extract_option_mp3.pack(
            side=tkinter.LEFT, padx=(36, 0), pady=(10, 16))
        self.extract_option_mp4.pack(
            side=tkinter.LEFT, padx=(14, 0), pady=(10, 16))
        self.TK.mainloop()


# 요청받는 데이터의 딕셔너리 구조
# lists = {
#     'kind': 'youtube#searchListResponse',
#     'etag': 'wABmvKar5aF4C5jvVBaVsBoiLs4',
#     'nextPageToken': 'CAUQAA',
#     'regionCode': 'KR',
#     'pageInfo': {'totalResults': 16728, 'resultsPerPage': 5},
#     'items': [
#         # 동영상 목록들 예시를 들기위해 한 요소만 담고 있음
#         {
#             'kind': 'youtube#searchResult',
#             'etag': 'jbZTRjksYgBh_X6_ucNpKxaLUBo',
#             'id': {'kind': 'youtube#video', 'videoId': 'KT5nEChOISs'},
#             'snippet': {
#                 'publishedAt': '2021-01-05T09:00:11Z',
#                 'channelId': 'UChg_sGDFk1qZf5N97GC8s6w',
#                 'title': '염따(YUMDDA) - 존시나 (feat. Northfacegawd, JUSTHIS, 래원) [Official MV]',
#                 'description': '',
#                 'thumbnails': {
#                     'default': {'url': 'https://i.ytimg.com/vi/KT5nEChOISs/default.jpg', 'width': 120, 'height': 90},
#                     'medium': {'url': 'https://i.ytimg.com/vi/KT5nEChOISs/mqdefault.jpg', 'width': 320, 'height': 180},
#                     'high': {'url': 'https://i.ytimg.com/vi/KT5nEChOISs/hqdefault.jpg', 'width': 480, 'height': 360}
#                 },
#                 'channelTitle': '염따', 'liveBroadcastContent': 'none', 'publishTime': '2021-01-05T09:00:11Z'
#             }
#         },
#     ]
# }


app = PyEx()
app.packing()
