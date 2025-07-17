import pandas as pd

try:
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="euc-kr")
    print("✅ 파일 로드 성공!")
    print(df.head())
except Exception as e:
    print("❌ CSV 읽기 실패:", e)
