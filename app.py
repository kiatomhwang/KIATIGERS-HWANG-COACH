import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# [1] 페이지 설정 (Tigers 테마)
st.set_page_config(page_title="KIA Tigers 파워 분석", layout="wide")
st.title("⚾ KIA Tigers 선수단 파워 성능 데이터보드")

# [2] 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# [3] 사이드바: 선수 선택 및 입력
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/c/c9/KIA_Tigers_logo.svg/1200px-KIA_Tigers_logo.svg.png", width=100)
    st.header("선수단 관리")
    player_name = st.selectbox("선수 선택", ["김도영", "양현종", "나성범", "윤영철", "박찬호"])
    
    st.divider()
    st.subheader("오늘의 테스트 기록")
    jump_h = st.number_input("점프 높이 (cm)", 0, 100, 50)
    peak_f = st.number_input("Peak Force (N)", 0, 6000, 3000)
    ttpf = st.number_input("TTPF (ms)", 0, 500, 250)
    
    if st.button("🚀 데이터 저장 및 업데이트"):
        new_row = pd.DataFrame([{
            "날짜": datetime.now().strftime("%Y-%m-%d"),
            "선수명": player_name,
            "점프높이": jump_h,
            "Peak_Force": peak_f,
            "TTPF": ttpf
        }])
        try:
            df = conn.read(worksheet="Sheet1")
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success("데이터가 시트에 저장되었습니다!")
            st.balloons()
        except:
            st.error("저장 실패. 시트 설정을 확인하세요.")

# [4] 메인 화면: 그래프 분석 (Plotly 활용)
st.subheader("📊 파워 테스트 추세 분석 (Jump Height vs Force)")

# 시트에서 데이터 불러오기 (실패 시 샘플 데이터 사용)
try:
    display_data = conn.read(worksheet="Sheet1")
except:
    # 데이터가 없을 때를 대비한 샘플
    display_data = pd.DataFrame({
        "선수명": ["김도영", "양현종", "나성범", "윤영철", "박찬호"],
        "점프높이": [65, 48, 72, 55, 60],
        "Peak_Force": [3500, 2800, 4200, 3100, 3900],
        "TTPF": [240, 320, 190, 280, 210]
    })

# --- Plotly 콤보 그래프 생성 ---
fig = make_subplots(specs=[[{"secondary_y": True}]])

# 1. 막대 그래프 (Jump Height) - 블랙/다크 그레이
fig.add_trace(
    go.Bar(
        x=display_data['선수명'], 
        y=display_data['점프높이'], 
        name="점프 높이 (cm)",
        marker_color='#060606', # Tigers Black
        opacity=0.8
    ),
    secondary_y=False,
)

# 2. 꺾은선 1 (Peak Force) - 타이거즈 레드
fig.add_trace(
    go.Scatter(
        x=display_data['선수명'], 
        y=display_data['Peak_Force'], 
        name="Peak Force (N)",
        line=dict(color="#EA0029", width=4), # Tigers Red
        mode='lines+markers'
    ),
    secondary_y=True,
)

# 3. 꺾은선 2 (TTPF) - 실버/그레이
fig.add_trace(
    go.Scatter(
        x=display_data['선수명'], 
        y=display_data['TTPF'], 
        name="TTPF (ms)",
        line=dict(color="#A5A8AA", width=2, dash='dot'), # Silver Gray
        mode='lines+markers'
    ),
    secondary_y=True,
)

# 레이아웃 꾸미기
fig.update_layout(
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    paper_bgcolor="white",
    plot_bgcolor="#F8F9FA", # 연한 그레이 배경
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# [5] 데이터 테이블 확인
st.divider()
st.subheader("📋 전체 테스트 로그")
st.dataframe(display_data.style.highlight_max(axis=0, color='#FFD7D7'))

# [5단계] 저장 버튼 (여기서 위에서 정의한 player_name을 사용합니다)
# [최종 저장 코드 조각]
if st.button("훈련 일지 저장하기"):
    new_data = pd.DataFrame([{
        "날짜": datetime.now().strftime("%Y-%m-%d"),
        "선수명": player_name,
        "단계": phase,
        "RPE": rpe,
        "통증": pain,
        "메모": note
    }])
    
    try:
        # 서비스 계정 설정이 완료되면 이제 이 명령어가 작동합니다!
        conn.update(worksheet="Sheet1", data=new_data)
        st.success("✅ 마스터키 인증 성공! 구글 시트에 저장되었습니다.")
    except Exception as e:
        st.error(f"❌ 여전히 문제가 있어요: {e}")

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
