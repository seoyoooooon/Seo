import streamlit as st
import pandas as pd

# 데이터 로드 및 전처리 함수
@st.cache_data
def load_and_clean_data():
    # CSV 파일 로드
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="euc-kr")

    # 총인구수 숫자형 변환
    df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

    # 연령별 인구 컬럼만 추출
    age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
    rename_dict = {col: col.replace('2025년05월_계_', '') for col in age_columns}

    # 필요한 컬럼 선택 및 이름 변경
    df_cleaned = df[['행정구역', '총인구수'] + age_columns].rename(columns=rename_dict)

    # 총인구수 기준 상위 5개 행정구역 추출
    top5_df = df_cleaned.sort_values(by='총인구수', ascending=False).head(5)

    # 연령별 인구 숫자형 변환
    for col in rename_dict.values():
        if top5_df[col].dtype == 'object':
            top5_df[col] = top5_df[col].str.replace(',', '').astype(int)

    # 선 그래프용 데이터: 연령을 index, 행정구역을 column
    line_df = top5_df.set_index('행정구역').loc[:, list(rename_dict.values())].T
    line_df.index.name = '연령'

    return df, top5_df, line_df

# 데이터 로드
df_original, df_top5, df_line = load_and_clean_data()

# 앱 UI 구성
st.title("2025년 5월 기준 연령별 인구 현황")
st.subheader("총인구수 기준 상위 5개 행정구역의 연령별 인구 변화")
st.line_chart(df_line)

st.subheader("상위 5개 행정구역 데이터")
st.dataframe(df_top5)

st.subheader("전체 원본 데이터")
st.dataframe(df_original)
