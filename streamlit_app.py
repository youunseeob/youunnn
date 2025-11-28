import streamlit as st
import random
import time

# 1. 페이지 설정 및 디자인 커스터마이징 (CSS)
st.set_page_config(page_title="구구단 풍선 챌린지", page_icon="🎈")

# 버튼 스타일을 풍선처럼 동그랗고 예쁘게 만드는 CSS 코드
st.markdown("""
<style>
    div.stButton > button {
        width: 100%;
        height: 100px;
        font-size: 30px;
        border-radius: 20px;
        background-color: #FFDDC1;
        border: 2px solid #FFABAB;
        color: #D32F2F;
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        background-color: #FFABAB;
        color: white;
    }
    .big-font {
        font-size: 60px !important;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
    }
    .score-board {
        font-size: 25px;
        font-weight: bold;
        color: #43A047;
    }
</style>
""", unsafe_allow_html=True)

# 2. 게임 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'num1' not in st.session_state:
    st.session_state.num1 = 0
    st.session_state.num2 = 0
    st.session_state.answer = 0
    st.session_state.options = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = "" # 정답/오답 메시지 저장용

# 3. 문제 생성 함수
def generate_problem():
    st.session_state.num1 = random.randint(2, 9)
    st.session_state.num2 = random.randint(1, 9)
    st.session_state.answer = st.session_state.num1 * st.session_state.num2
    
    # 보기 생성 (정답 + 오답)
    ans = st.session_state.answer
    options = set([ans]) # 중복 방지를 위해 집합(set) 사용
    
    while len(options) < 4:
        wrong = ans + random.randint(-10, 10)
        if wrong > 0 and wrong != ans:
            options.add(wrong)
            
    st.session_state.options = list(options)
    random.shuffle(st.session_state.options)
    st.session_state.feedback = "" # 피드백 초기화

# 게임 초기 실행 시 문제 생성
if st.session_state.num1 == 0:
    generate_problem()

# ================= 게임 화면 구성 =================

# 4. 승리 화면 (100점 달성 시)
if st.session_state.score >= 100:
    st.balloons() # 풍선 애니메이션 효과!
    st.markdown("<h1 style='text-align: center; color: orange;'>🏆 미션 성공! 🏆</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>축하합니다! 100점을 달성했어요!</h3>", unsafe_allow_html=True)
    
    st.image("https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif", use_container_width=True) # 축하 GIF
    
    if st.button("🔄 처음부터 다시 도전하기"):
        st.session_state.score = 0
        generate_problem()
        st.rerun()

# 5. 진행 중인 게임 화면
else:
    st.title("🎈 구구단 풍선 챌린지")
    
    # 상단 정보창 (점수 & 진행바)
    col_info1, col_info2 = st.columns([3, 1])
    with col_info1:
        # 진행 상황 (Progress Bar)
        progress = st.session_state.score / 100
        st.write(f"**미션 달성률 ({st.session_state.score}/100)**")
        st.progress(progress)
    with col_info2:
        st.markdown(f"<div class='score-board'>점수: {st.session_state.score}</div>", unsafe_allow_html=True)

    st.divider()

    # 문제 표시
    st.markdown(f"<div class='big-font'>{st.session_state.num1} × {st.session_state.num2} = ❓</div>", unsafe_allow_html=True)
    
    st.write("") # 여백
    st.write("") 

    # 피드백 메시지 표시 (정답/오답 알림)
    if st.session_state.feedback == "correct":
        st.info("딩동댕! 정답입니다! ⭕ (+10점)")
    elif st.session_state.feedback == "wrong":
        st.error("땡! 다시 생각해보세요! ❌ (-5점)")

    st.write("") 

    # 보기 버튼 배치 (2x2 그리드 형태)
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    cols = [col1, col2, col3, col4]

    for i, option_val in enumerate(st.session_state.options):
        with cols[i]:
            # 버튼 클릭 로직
            if st.button(f"{option_val}", key=f"btn_{i}"):
                if option_val == st.session_state.answer:
                    # 정답 처리
                    st.session_state.score += 10
                    st.session_state.feedback = "correct"
                    
                    # 100점 달성 즉시 승리 화면으로 가기 위해 바로 리런하지 않고, 
                    # 점수 체크 후 리런
                    if st.session_state.score >= 100:
                        st.rerun()
                    
                    generate_problem() # 새 문제 생성
                    st.rerun()
                else:
                    # 오답 처리
                    if st.session_state.score > 0:
                        st.session_state.score -= 5
                    st.session_state.feedback = "wrong"
                    st.rerun()

    st.divider()
    
    # 게임 리셋 버튼
    if st.button("🔄 게임 다시 시작하기", use_container_width=True):
        st.session_state.score = 0
        generate_problem()
        st.rerun()
