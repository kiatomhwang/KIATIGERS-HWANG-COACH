import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 사이트 설정
st.set_page_config(page_title="GOATA & NSCA 야구단 관리시스템", layout="wide")

# 1. 사이드바 (로그인 및 설정)
st.sidebar.title("🏃‍♂️ 선수 관리 패널")
player_name = st.sidebar.selectbox("선수 선택", ["김투수", "이타자", "박야수"])
phase = st.sidebar.radio("주기화 단계", ["Strength", "Power", "Maintenance"])

# 2. 메인 화면 - 오늘의 루틴
st.title(f"⚾ {player_name} 선수의 오늘의 트레이닝")
st.info(f"현재 단계: **{phase}** | 목표: **건(Tendon) 탄성 극대화 및 부상 방지**")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📺 트레이닝 가이드")
    # GOATA 핵심 큐잉과 영상 배치
    st.video("https://www.youtube.com/watch?v=WVobz_eTNKk") # 실제 코치님 영상 링크
    st.warning("💡 GOATA 체크: 뒤꿈치를 지면에서 1cm 띄우고(Heel Away), 발 바깥날로 지면을 움켜쥐세요.")

with col2:
    st.subheader("📊 컨디션 로그 입력")
    rpe = st.slider("오늘의 훈련 강도 (RPE)", 1, 10, 5)
    pain = st.slider("통증 수치 (Pain Level)", 0, 10, 0)
    note = st.text_area("특이 사항 (예: 햄스트링 타이트함)")
    
    if st.button("훈련 일지 저장"):
        st.success("데이터가 구글 시트로 전송되었습니다!")

# 3. 데이터 시각화 (코치 전용 뷰)
st.divider()
st.subheader("📈 최근 퍼포먼스 트렌드")
# 가상 데이터 생성 및 차트 출력
chart_data = pd.DataFrame({"Day": range(1, 11), "RPE": [6,7,8,5,9,7,8,6,9,7]})
st.line_chart(chart_data.set_index("Day"))
