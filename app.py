import requests

def get_exim_exchange_rate(api_key, target_keyword):
    # 1. 한국수출입은행 API 주소 및 파라미터
    url = "https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON"
    params = {
        "authkey": api_key,
        "data": "AP01"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if not data:
            print("\n[알림] 텅 빈 데이터를 받았습니다!")
            print("원인: 오늘이 주말/공휴일이거나, 아직 오늘의 환율이 고시되지 않은 시간입니다.")
            return

        print("\n✅ 성공! 수출입은행 환율 정보를 정상적으로 받아왔습니다.")
        print("-" * 50)

        # 2. 회원님이 입력한 검색어(target_keyword)로 데이터 뒤지기
        # (영어를 입력했을 경우를 대비해 대문자로 변환해서 비교)
        target_keyword_upper = target_keyword.upper()
        found = False

        for item in data:
            cur_unit = item.get("cur_unit", "") # 예: USD, JPY(100)
            cur_nm = item.get("cur_nm", "")     # 예: 미국 달러, 일본 옌
            rate = item.get("deal_bas_r", "")   # 예: 1,300.50

            # 입력한 글자가 '영어 코드'에 있거나 '한국어 이름'에 포함되어 있다면 출력!
            if (target_keyword_upper in cur_unit) or (target_keyword in cur_nm):
                print(f"💰 현재 {cur_unit} ({cur_nm}) = {rate} KRW (매매기준율) 입니다.")
                found = True

        print("-" * 50)

        # 3. 목록을 다 뒤졌는데도 못 찾았을 때의 안내문
        if not found:
            print(f"'{target_keyword}'에 대한 환율 정보를 목록에서 찾을 수 없습니다.")
            print("팁: '미국', '일본', '유로' 또는 'USD', 'JPY' 등으로 다시 검색해 보세요.")

    except Exception as e:
         print(f"실행 중 에러가 발생했습니다: {e}")

# ==========================================
# 실행 부분
# ==========================================
if __name__ == "__main__":
    MY_API_KEY = "PSnnFDZjnKZmnYoIN6lwQoH067QBpOIC"

    # 코랩 실행 시 사용자에게 입력을 받는 창을 띄웁니다.
    print("원하시는 국가의 환율을 검색해 드립니다.")
    user_input = input("조회하고 싶은 나라 이름(예: 미국, 일본)이나 통화 코드(예: USD, EUR)를 입력하세요: ")

    # 사용자가 입력한 검색어를 함수에 전달합니다.
    get_exim_exchange_rate(MY_API_KEY, user_input)
