import streamlit as st
import random
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="구구단 풍선 터뜨리기", page_icon="🎈")

st.title("🎈 구구단 풍선 터뜨리기 🎈")
st.subheader("정답 풍선을 터뜨려 점수를 얻으세요!")

# 2. 게임 상태(변수) 초기화 (점수, 문제 등)
# Streamlit은 버튼을 누를 때마다 코드가 재실행되므로, 변수를 기억하기 위해 session_state를 씁니다.
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'num1' not in st.session_state:
    st.session_state.num1 = 0
    st.session_state.num2 = 0
    st.session_state.answer = 0
    st.session_state.options = []

# 3. 문제 출제 함수
def generate_problem():
    # 2단 ~ 9단 사이 랜덤 생성
    n1 = random.randint(2, 9)
    n2 = random.randint(1, 9)
    ans = n1 * n2
    
    # 보기 생성 (정답 1개 + 오답 3개)
    options = [ans]
    while len(options) < 4:
        # 정답 주변의 숫자로 오답 생성 (난이도 조절)
        wrong = ans + random.randint(-10, 10)
        if wrong > 0 and wrong not in options: # 중복 방지 및 음수 방지
            options.append(wrong)
    
    random.shuffle(options) # 보기 순서 섞기
    
    # 상태 저장
    st.session_state.num1 = n1
    st.session_state.num2 = n2
    st.session_state.answer = ans
    st.session_state.options = options

# 처음에 문제가 없으면 생성
if st.session_state.num1 == 0:
    generate_problem()

# 4. 화면 레이아웃 구성
# 현재 점수 표시
st.metric(label="현재 점수", value=f"{st.session_state.score} 점")

# 문제 표시 (크고 잘 보이게)
st.markdown(f"""
    <div style='text-align: center; font-size: 50px; font-weight: bold; margin: 20px;'>
        {st.session_state.num1} × {st.session_state.num2} = ❓
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# 5. 풍선(보기) 버튼 배치
# 4개의 컬럼으로 나누어 버튼을 가로로 배치
cols = st.columns(4)

for i, option_val in enumerate(st.session_state.options):
    with cols[i]:
        # 버튼 클릭 시 동작
        if st.button(f"🎈 {option_val}", use_container_width=True):
            if option_val == st.session_state.answer:
                # 정답일 경우
                st.success(f"정답입니다! {st.session_state.answer} 맞아요! 🎉")
                st.session_state.score += 10 # 10점 추가
                time.sleep(1) # 축하 메시지를 1초 보여주고
                generate_problem() # 새 문제 생성
                st.rerun() # 화면 새로고침
            else:
                # 오답일 경우
                st.error(f"아니에요! {st.session_state.num1} × {st.session_state.num2} 은 {option_val}이 아니에요. 💥")
                if st.session_state.score > 0:
                    st.session_state.score -= 5 # 5점 감점

# 6. 리셋 버튼
st.write("---")
if st.button("🔄 게임 다시 시작하기"):
    st.session_state.score = 0
    generate_problem()
    st.rerun()
