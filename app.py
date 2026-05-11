import requests
from datetime import datetime
import urllib3

# SSL 경고 메시지 무시 (필요한 경우에만 사용)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_exim_exchange_rate(api_key, target_keyword):
    url = "https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON"
    
    # 1. 오늘 날짜를 YYYYMMDD 형식으로 추출
    today = datetime.now().strftime("%Y%m%d")
    
    params = {
        "authkey": api_key,
        "searchdate": today, # 날짜 파라미터 추가
        "data": "AP01"
    }

    try:
        # SSL 인증서 검증 이슈가 있다면 verify=False 추가
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()

        data = response.json()

        # API 응답 결과가 리스트가 아닌 에러 메시지(dict)일 경우 처리
        if isinstance(data, dict):
             print(f"⚠️ API 서버 응답 오류: {data.get('errMsg', '알 수 없는 에러')}")
             return

        if not data:
            print(f"\n[알림] {today} 날짜의 데이터를 찾을 수 없습니다.")
            print("원인: 주말/공휴일이거나, 영업시간(오전 11시 이전) 전일 수 있습니다.")
            return

        print(f"\n✅ {today} 기준 수출입은행 환율 정보를 정상적으로 받아왔습니다.")
        print("-" * 50)

        target_keyword_upper = target_keyword.upper()
        found = False

        for item in data:
            cur_unit = item.get("cur_unit", "")
            cur_nm = item.get("cur_nm", "")
            # 결과값에 콤마(,)가 포함되어 문자열로 오므로 숫자로 계산할 땐 처리가 필요합니다.
            rate = item.get("deal_bas_r", "") 

            if (target_keyword_upper in cur_unit) or (target_keyword in cur_nm):
                print(f"💰 현재 {cur_unit} ({cur_nm}) = {rate} KRW (매매기준율)")
                found = True

        if not found:
            print(f"'{target_keyword}'에 대한 정보를 찾을 수 없습니다.")

    except Exception as e:
         print(f"실행 중 에러가 발생했습니다: {e}")

# 실행 부분
if __name__ == "__main__":
    # 보안을 위해 실제 서비스 시에는 환경 변수 등을 활용하세요!
    MY_API_KEY = "PSnnFDZjnKZmnYoIN6lwQoH067QBpOIC"

    print("--- 환율 조회 프로그램 ---")
    user_input = input("국가명 또는 통화코드(예: 미국, USD): ")
    get_exim_exchange_rate(MY_API_KEY, user_input)
