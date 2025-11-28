import streamlit as st
import random
import time
import requests
from streamlit_lottie import st_lottie

# ==========================================
# 1. 설정 및 리소스 로딩
# ==========================================
st.set_page_config(page_title="풍선 팡팡 구구단", page_icon="🎈", layout="centered")

# Lottie 애니메이션 파일을 웹에서 불러오는 함수
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# 애니메이션 로딩 (성공 시 폭죽, 시작 화면 풍선)
lottie_success = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_u4yrau.json") # 팡 터지는 효과
lottie_balloon = load_lottieurl("https://lottie.host/9d8b3564-9d51-4148-8951-64d99905c3c0/o7S4O4r0D9.json") # 둥둥 뜨는 풍선

# ==========================================
# 2. CSS 스타일링 (풍선 디자인 & 움직임)
# ==========================================
st.markdown("""
<style>
    /* 둥둥 떠다니는 애니메이션 정의 */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    /* 버튼을 풍선처럼 꾸미기 */
    div.stButton > button {
        width: 100%;
        height: 120px;
        font-size: 35px;
        font-weight: bold;
        border-radius: 50%; /* 완전 둥글게 */
        background: radial-gradient(circle at 30% 30%, #ff7e5f, #feb47b); /* 입체감 그라데이션 */
        border: none;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
        animation: float 3s ease-in-out infinite; /* 둥둥 뜨는 효과 적용 */
        text-shadow: 2px 2px 4px #000000;
    }
    
    /* 버튼에 마우스 올렸을 때 */
    div.stButton > button:hover {
        transform: scale(1.1); /* 커짐 */
        background: radial-gradient(circle at 30% 30%, #feb47b, #ff7e5f);
        cursor: pointer;
    }

    /* 점수판 스타일 */
    .score-container {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 상태 관리 (Session State)
# ==========================================
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'num1' not in st.session_state:
    st.session_state.num1 = 0 
if 'show_celebration' not in st.session_state:
    st.session_state.show_celebration = False # 정답 맞췄을 때 잠깐 이펙트 보여주기용

# 문제 생성 함수
def generate_problem():
    st.session_state.num1 = random.randint(2, 9)
    st.session_state.num2 = random.randint(1, 9)
    st.session_state.answer = st.session_state.num1 * st.session_state.num2
    
    ans = st.session_state.answer
    options = set([ans])
    while len(options) < 4:
        wrong = ans + random.randint(-10, 10)
        if wrong > 0 and wrong != ans:
            options.add(wrong)
            
    st.session_state.options = list(options)
    random.shuffle(st.session_state.options)

# 초기 문제 생성
if st.session_state.num1 == 0:
    generate_problem()

# ==========================================
# 4. 화면 구현 (시작 화면 vs 게임 화면)
# ==========================================

# [A] 시작 화면 (Intro)
if not st.session_state.game_started:
    st.markdown("<h1 style='text-align: center;'>🎪 풍선 팡팡 구구단 🎪</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: gray;'>100점을 향해 풍선을 터뜨려보세요!</h3>", unsafe_allow_html=True)
    
    # 중앙에 큰 풍선 이모지
    st.markdown("<div style='text-align: center; font-size: 150px;'>🎈🎈🎈</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("")
        if st.button("🚀 게임 시작하기", key="start_btn", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()

# [B] 게임 화면 (Game Loop)
else:
    # 1. 승리 화면 (100점 달성)
    if st.session_state.score >= 100:
        st.balloons()
        st.markdown("<h1 style='text-align: center; color: #FF9800;'>🏆 미션 컴플리트! 🏆</h1>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 80px;'>🎉🎊🎉</div>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>축하합니다! 모든 풍선을 터뜨렸어요!</h3>", unsafe_allow_html=True)
        
        if st.button("🔄 처음으로 돌아가기"):
            st.session_state.score = 0
            st.session_state.game_started = False
            generate_problem()
            st.rerun()

    # 2. 플레이 화면
    else:
        # 상단바: 홈버튼 / 진행바 / 점수
        c1, c2, c3 = st.columns([1, 6, 2])
        with c1:
            if st.button("🏠"): # 홈 버튼
                st.session_state.game_started = False
                st.session_state.score = 0
                st.rerun()
        with c2:
            st.write(f"**목표 달성 ({st.session_state.score}/100)**")
            st.progress(st.session_state.score / 100)
        with c3:
             st.markdown(f"<div class='score-container'>⭐ {st.session_state.score}점</div>", unsafe_allow_html=True)

        st.divider()

        # 정답 축하 이펙트
        if st.session_state.show_celebration:
            st.success("🎉 정답입니다! +10점")
            st.session_state.show_celebration = False # 한 번 보여주고 끄기
            time.sleep(0.8) # 이펙트 감상 시간

        # 문제 표시
        st.markdown(f"<div style='font-size: 60px; text-align: center; font-weight: bold; margin-bottom: 30px;'>"
                    f"{st.session_state.num1} × {st.session_state.num2} = ❓</div>", unsafe_allow_html=True)

        # 보기 버튼 (풍선)
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        cols = [col1, col2, col3, col4]

        for i, option_val in enumerate(st.session_state.options):
            with cols[i]:
                # 버튼을 누르면
                if st.button(f"{option_val}", key=f"balloon_{i}"):
                    if option_val == st.session_state.answer:
                        # 정답!
                        st.session_state.score += 10
                        st.session_state.show_celebration = True # 이펙트 트리거 켜기
                        generate_problem() # 다음 문제 생성
                        st.rerun()
                    else:
                        # 오답!
                        st.toast("💥 앗! 풍선이 터지지 않았어요. 다시 해보세요!", icon="❌")
                        if st.session_state.score >= 5:
                            st.session_state.score -= 5
                        st.rerun()
