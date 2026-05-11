import streamlit as st
import requests
from datetime import datetime

# 페이지 제목 설정
st.set_page_config(page_title="환율 조회 앱", page_icon="💰")
st.title("🏦 수출입은행 실시간 환율 조회")

def get_exim_exchange_rate(api_key, target_keyword):
    url = "https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON"
    today = datetime.now().strftime("%Y%m%d")
    
    params = {
        "authkey": api_key,
        "searchdate": today,
        "data": "AP01"
    }

    try:
        # Streamlit에서는 데이터 로딩 중임을 알리는 스피너를 사용하면 좋습니다.
        with st.spinner('데이터를 불러오는 중...'):
            response = requests.get(url, params=params, verify=False)
            data = response.json()

        if not data:
            st.warning(f"⚠️ {today} 기준 데이터가 없습니다. (주말/공휴일 또는 고시 전 시간)")
            return

        target_keyword_upper = target_keyword.upper()
        found = False

        for item in data:
            cur_unit = item.get("cur_unit", "")
            cur_nm = item.get("cur_nm", "")
            rate = item.get("deal_bas_r", "")

            if (target_keyword_upper in cur_unit) or (target_keyword in cur_nm):
                st.success(f"**{cur_nm} ({cur_unit})**")
                st.metric(label="매매기준율", value=f"{rate} KRW")
                found = True

        if not found:
            st.info(f"'{target_keyword}'에 대한 검색 결과가 없습니다.")

    except Exception as e:
        st.error(f"에러가 발생했습니다: {e}")

# --- UI 레이아웃 ---
MY_API_KEY = "PSnnFDZjnKZmnYoIN6lwQoH067QBpOIC"

user_input = st.text_input("조회할 국가명 또는 통화코드를 입력하세요 (예: 미국, USD)")

if st.button("환율 조회하기"):
    if user_input:
        get_exim_exchange_rate(MY_API_KEY, user_input)
    else:
        st.warning("검색어를 입력해 주세요.")
