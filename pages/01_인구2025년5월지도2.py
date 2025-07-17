import streamlit as st
import pandas as pd
import folium
import re
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("2025년 5월 기준 연령별 인구 현황")

# CSV 불러오기
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 총인구수 숫자형으로 변환
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

# 연령별 인구 컬럼 추출 및 이름 정리
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

# 전처리된 데이터프레임 생성
df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# 괄호 제거 (행정구역명에서 (숫자) 제거)
df_age['행정구역'] = df_age['행정구역'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', x))

# 상위 5개 행정구역 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5).copy()

# 지도용 좌표 지정
region_coords = {
    '경기도': (37.4138, 127.5183),
    '서울특별시': (37.5665, 126.9780),
    '부산광역시': (35.1796, 129.0756),
    '경상남도': (35.4606, 128.2132),
    '인천광역시': (37.4563, 126.7052),
}

# 🗺 지도 시각화
st.subheader("🗺 상위 5개 행정구역 인구 분포 지도 (Folium)")

m = folium.Map(location=[36.5, 127.8], zoom_start=7)

for _, row in top5_df.iterrows():
    region = row['행정구역']
    population = row['총인구수']
    if region in region_coords:
        lat, lon = region_coords[region]
        folium.Circle(
            location=(lat, lon),
            radius=population / 100,  # 반지름 조정 가능
            color='pink',
            fill=True,
            fill_color='pink',
            fill_opacity=0.4,
            popup=f"{region}: {population:,}명"
        ).add_to(m)

# 지도 표시
st_data = st_folium(m, width=1000, height=600)

# 원본 데이터 출력
st.subheader("📊 원본 데이터 (상위 5개 행정구역)")
st.dataframe(top5_df)

# 선그래프 출력
st.subheader("📈 상위 5개 행정구역 연령별 인구 변화")
age_columns_only = top5_df.columns[2:]

for index, row in top5_df.iterrows():
    st.write(f"### {row['행정구역']}")
    age_data = row[2:].astype(str).str.replace(',', '').astype(int)
    age_df = pd.DataFrame({
        '연령': age_columns_only,
        '인구수': age_data.values
    }).set_index('연령')
    st.line_chart(age_df)
