import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt  # <--- 이 줄이 반드시 있어야 합니다!

# 1. 사이트 설정 및 제목
st.set_page_config(page_title="KIA Tigers 황코치 트레이닝", layout="wide")
st.title("⚾ 선수별 맞춤형 트레이닝 & 컨디션 로그")

# 2. 구글 스프레드시트 연결 설정
# (주소는 나중에 Streamlit 설정창에서 넣을 거예요!)
conn = st.connection("gsheets", type=GSheetsConnection)
# 기존의 read/update 부분을 이 로직으로 바꿔보세요.
try:
    # 시트에서 데이터를 읽어오되, 만약 실패하면 빈 상자를 만듭니다.
    existing_data = conn.read(worksheet="Sheet1")
    updated_df = pd.concat([existing_data, new_data], ignore_index=True)
    conn.update(worksheet="Sheet1", data=updated_df)
    st.success("✅ 저장 성공!")
except Exception as e:
    # 만약 시트가 비어있어서 에러가 난다면, 아예 새로 써버리는 명령입니다.
    conn.update(worksheet="Sheet1", data=new_data)
    st.success("✅ 시트가 비어있어 새로 생성하여 저장했습니다!")

# 3. 선수용 입력 화면 (사이드바)
st.sidebar.header("선수 정보 입력")
player_name = st.sidebar.selectbox("선수 이름을 선택하세요", ["김도영", "양현종", "나성범", "윤영철"])
phase = st.sidebar.selectbox("현재 주기화 단계", ["Strength", "Power", "Maintenance"])

# 4. 메인 화면 - 훈련 영상 및 큐잉
st.subheader(f"📅 오늘의 루틴 ({phase} 단계)")
col1, col2 = st.columns(2)

with col1:
    st.info("💡 GOATA 핵심 큐잉")
    st.write("- 뒤꿈치 1cm 유지 (Heel Away)\n- 정강이 외회전 (Bow-out)\n- 발 바깥날로 지면 움켜쥐기")
    # 코치님의 유튜브 영상 ID로 교체 가능합니다.
    st.video("https://youtu.be/bHYnDnqWbxA?si=ICuUkfJNMS5v_tYz")

st.subheader("📈 최근 퍼포먼스 트렌드")

# 1. 데이터 준비 (구글 시트에서 가져온 데이터를 쓴다고 가정)
chart_data = pd.DataFrame({
    "날짜": ["01-01", "01-02", "01-03", "01-04", "01-05"],
    "RPE": [5, 7, 4, 8, 6],
    "통증": [0, 1, 0, 2, 1]
})

# 2. 그래프 그리기 시작
fig, ax1 = plt.subplots(figsize=(10, 5))

# X축 이름과 Y축(RPE) 설정
ax1.set_xlabel('훈련 날짜 (Date)')
ax1.set_ylabel('훈련 강도 (RPE)', color='green')
ax1.plot(chart_data['날짜'], chart_data['RPE'], color='green', marker='o', label='강도(RPE)')

# Y축(통증) 하나 더 만들기
ax2 = ax1.twinx()
ax2.set_ylabel('통증 수치 (Pain)', color='red')
ax2.bar(chart_data['날짜'], chart_data['통증'], color='red', alpha=0.3, label='통증(Pain)')

plt.title(f"{player_name} 선수 컨디션 리포트")
st.pyplot(fig) # 화면에 그래프 출력") 

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

import matplotlib.pyplot as plt # 코드 맨 윗줄에 이게 있는지 확인하세요!

st.subheader("📈 최근 퍼포먼스 트렌드")

# 1. 데이터 준비 (구글 시트에서 가져온 데이터를 쓴다고 가정)
chart_data = pd.DataFrame({
    "날짜": ["01-01", "01-02", "01-03", "01-04", "01-05"],
    "RPE": [5, 7, 4, 8, 6],
    "통증": [0, 1, 0, 2, 1]
})

# 2. 그래프 그리기 시작
fig, ax1 = plt.subplots(figsize=(10, 5))

# X축 이름과 Y축(RPE) 설정
ax1.set_xlabel('훈련 날짜 (Date)')
ax1.set_ylabel('훈련 강도 (RPE)', color='green')
ax1.plot(chart_data['날짜'], chart_data['RPE'], color='green', marker='o', label='강도(RPE)')

# Y축(통증) 하나 더 만들기
ax2 = ax1.twinx()
ax2.set_ylabel('통증 수치 (Pain)', color='red')
ax2.bar(chart_data['날짜'], chart_data['통증'], color='red', alpha=0.3, label='통증(Pain)')

plt.title(f"{player_name} 선수 컨디션 리포트")
st.pyplot(fig) # 화면에 그래프 출력

st.divider()
st.subheader("📊 파워 테스트 심층 분석 (Jump Height vs Force Strategy)")

# 1. 가상의 데이터 준비 (나중에는 구글 시트에서 가져오면 됩니다!)
power_data = pd.DataFrame({
    "선수명": ["김도영", "양현종", "나성범", "윤영철", "최형우"],
    "점프높이(cm)": [65, 48, 72, 55, 60],
    "Peak_Force(N)": [3500, 2800, 4200, 3100, 3900],
    "TTPF(ms)": [250, 350, 180, 300, 220]
})

# 2. 그래프 그리기 시작 (3개의 축 만들기)
fig, ax1 = plt.subplots(figsize=(12, 6)) # 기본 축 (Y1: 점프 높이)
ax2 = ax1.twinx() # 두 번째 축 (Y2: Peak Force)
ax3 = ax1.twinx() # 세 번째 축 (Y3: TTPF)

# 3. 세 번째 축의 위치를 오른쪽 바깥으로 밀어내기
ax3.spines["right"].set_position(("axes", 1.15))
ax3.set_frame_on(True) # 프레임 보이게 설정
ax3.patch.set_visible(False) # 배경 투명하게

# --- 그래프 그리기 ---

# [막대] Y1: 점프 높이 (왼쪽 축, 파란색)
bars = ax1.bar(power_data['선수명'], power_data['점프높이(cm)'], color='skyblue', alpha=0.6, label='점프 높이 (cm)')
ax1.set_ylabel('점프 높이 (cm)', color='skyblue', fontsize=12, fontweight='bold')
ax1.tick_params(axis='y', labelcolor='skyblue')
ax1.set_ylim(0, 80) # Y축 범위 설정 (필요시 조절)

# [꺾은선 1] Y2: Peak Force (오른쪽 첫 번째, 빨간색)
line1 = ax2.plot(power_data['선수명'], power_data['Peak_Force(N)'], color='red', marker='o', linewidth=3, label='Peak Force (N)')
ax2.set_ylabel('Peak Force (N)', color='red', fontsize=12, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='red')
ax2.set_ylim(2000, 5000) # Y축 범위 설정

# [꺾은선 2] Y3: TTPF (오른쪽 두 번째, 초록색)
line2 = ax3.plot(power_data['선수명'], power_data['TTPF(ms)'], color='green', marker='s', linestyle='--', linewidth=2, label='TTPF (ms)')
ax3.set_ylabel('TTPF (ms)', color='green', fontsize=12, fontweight='bold')
ax3.tick_params(axis='y', labelcolor='green')
ax3.set_ylim(100, 400) # Y축 범위 설정

# --- 마무리 설정 ---

plt.title("선수별 파워 테스트 결과 비교 분석", fontsize=16)
ax1.set_xlabel("선수명", fontsize=12)

# 범례(Legend) 합치기
lines = [bars] + line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3) # 범례를 그래프 아래로 뺌

plt.tight_layout() # 레이아웃 자동 정리
st.pyplot(fig) # 화면에 출력!
