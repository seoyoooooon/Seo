import streamlit as st
import pandas as pd

# CSV 파일 로드 (EUC-KR 인코딩)
@st.cache_data
def load_data():
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="euc-kr")
    return df

df = load_data()

# '총인구수' 추출 및 숫자형으로 변환
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

# 연령별 인구 컬럼만 추출
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]

# 연령 숫자만 컬럼 이름으로 추출
renamed_columns = {col: col.replace('2025년05월_계_', '') for col in age_columns}
df_age = df[['행정구역', '총인구수'] + age_columns].rename(columns=renamed_columns)

# 총인구수 기준 상위 5개 행정구역 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 연령 데이터만 선택
age_only_cols = list(renamed_columns.values())
top5_line_df = top5_df.set_index('행정구역')[age_only_cols].T
top5_line_df.index.name = '연령'
top5_line_df = top5_line_df.apply(lambda x: x.str.replace(',', '') if x.dtype == 'object' else x)
top5_line_df = top5_line_df.astype(int)

# 앱 UI 구성
st.title("2025년 5월 기준 연령별 인구 현황 분석")
st.subheader("총인구수 기준 상위 5개 행정구역의 연령별 인구 분포")

# 선 그래프 시각화
st.line_chart(top5_line_df)

# 원본 데이터 표시
st.subheader("원본 데이터")
st.dataframe(df)
