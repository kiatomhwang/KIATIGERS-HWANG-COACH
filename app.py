import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. 사이트 설정 및 제목
st.set_page_config(page_title="KIA Tigers 황코치 트레이닝", layout="wide")
st.title("⚾ 선수별 맞춤형 트레이닝 & 컨디션 로그")

# 2. 구글 스프레드시트 연결 설정
# (주소는 나중에 Streamlit 설정창에서 넣을 거예요!)
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. 선수용 입력 화면 (사이드바)
st.sidebar.header("선수 정보 입력")
player_name = st.sidebar.selectbox("이름을 선택하세요", ["김도영", "양현종", "나성범", "윤영철"])
phase = st.sidebar.selectbox("현재 주기화 단계", ["Strength", "Power", "Maintenance"])

# 4. 메인 화면 - 훈련 영상 및 큐잉
st.subheader(f"📅 오늘의 루틴 ({phase} 단계)")
col1, col2 = st.columns(2)

with col1:
    st.info("💡 GOATA 핵심 큐잉")
    st.write("- 뒤꿈치 1cm 유지 (Heel Away)\n- 정강이 외회전 (Bow-out)\n- 발 바깥날로 지면 움켜쥐기")
    # 코치님의 유튜브 영상 ID로 교체 가능합니다.
    st.video("https://www.youtube.com/watch?v=WVobz_eTNKk") 

with col2:
    st.subheader("📝 훈련 결과 기록")
    rpe = st.slider("오늘 운동이 얼마나 힘들었나요? (1~10)", 1, 10, 5)
    pain = st.slider("통증 수치 (0: 없음, 10: 극심)", 0, 10, 0)
    note = st.text_area("특이 사항 (예: 왼쪽 햄스트링 타이트함)", placeholder="오늘의 몸 상태를 적어주세요.")

    # [중요] 저장 버튼 클릭 시 로직
    if st.button("훈련 일지 저장하기"):
        # 저장할 데이터 한 줄 만들기
        new_data = pd.DataFrame([{
            "날짜": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "선수명": player_name,
            "단계": phase,
            "RPE": rpe,
            "통증": pain,
            "메모": note
        }])
        
        # 구글 시트에 데이터 추가 (가장 마지막 줄에 붙여넣기)
        try:
            # 기존 데이터를 읽어옴
            existing_data = conn.read(worksheet="Sheet1") # 시트 하단 탭 이름이 'Sheet1'인지 확인하세요!
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            # 시트에 다시 씀
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success("✅ 저장 완료! 구글 시트를 확인해보세요.")
        except Exception as e:
            st.error(f"❌ 저장 실패: 시트 이름을 확인하거나 설정을 다시 확인해주세요. ({e})")
