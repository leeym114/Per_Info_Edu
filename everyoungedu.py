# streamlit run ./streamlit/everyoungedu.py

import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
import time

def playTime_display(playstatus, playtime):
    hours = int(playtime // 3600)
    minutes = int((playtime % 3600) // 60)
    seconds = int(playtime % 60)

    if hours > 0:
        st.text(f"{playstatus} 시간은: {hours}시간 {minutes}분 {seconds}초 입니다.")
    else:
        st.text(f"{playstatus} 시간은: {minutes}분 {seconds}초 입니다.")

def play_persInformation():

    st.header("개인정보보호 유튜브 영상 재생")
    st.subheader("중장년층 개인정보보호 교육")
    # st.text("중장년층 개인정보보호 교육")

    # service = Service('d:/sw/pythonpractice/streamlit/chromedriver.exe')
    
    # ChromeOptions 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=3')                                   # 3 -- ERROR만 표시
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 불필요한 에러메세지 삭제

    driver = webdriver.Chrome(options=options)  # Chrome 브라우저 열기
    play_time = 0

    try:
        youtube_video_id = 'JFcj-KQAHeA'  # 2024년 에버영 개인정보보호 교육 영상
        youtube_url = f'https://www.youtube.com/watch?v={youtube_video_id}'

        driver.get(youtube_url)  # 영상 재생
        time.sleep(3)            # 영상 로딩 대기

        # 현재 재생 시간과 총 재생 시간을 가져오기
        current_time = driver.execute_script("return document.querySelector('.video-stream').currentTime")
        total_time = driver.execute_script("return document.querySelector('.video-stream').duration")
        prev_time = current_time

        playTime_display("재생", total_time)  # 총 재생시간 표시

        # 현재 재생 시간과 총 재생 시간 비교
        while True:
            interval = current_time - prev_time

            # 정상 Play의 경우(0 <= interval < 2초)만 Play_time 누적
            if interval >= 0 and interval < 2:  # 정상 Play 중..
                play_time += current_time - prev_time

            prev_time = current_time

            # 현재 재생 시간이 총 재생 시간에 도달하면 종료
            if total_time - current_time < 1:  # 1초 미만 차이로 종료
                st.text("영상이 끝까지 재생되었습니다.")
                break
            
            current_time = driver.execute_script("return document.querySelector('.video-stream').currentTime")

            # 1초마다 재생 상태 확인
            time.sleep(1)

    except NoSuchWindowException:
        if play_time == 0:
            st.text("재생 없이 브라우저가 닫혔습니다.")
        else:
            st.text("재생 중에 브라우저가 닫혔습니다.")
    except WebDriverException:
        st.text("교육 영상이 열리기 전에 브라우저가 닫혔습니다.")
    except Exception as e:
        st.text(f"알 수 없는 Error로 브라우저를 닫습니다. ({e})")
    finally:
        playTime_display("시청", play_time)  # 총 시청시간 표시
        driver.quit()                        # Chrome 브라우저 닫기
    
st.title("에버영코리아 4대 법정 의무교육")
if st.button('2024년 중장년층 개인정보보호 교육'):
    play_persInformation()












