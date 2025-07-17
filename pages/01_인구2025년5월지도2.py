import streamlit as st
import pandas as pd
import folium
import re
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(layout="wide")
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 읽기
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 총인구수 컬럼 정리
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

# 연령별 인구 컬럼 추출
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

# 컬럼 이름 정리
df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# 행정구역명에서 괄호 제거
df_age['행정구역'] = df_age['행정구역'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', x))

# 총인구수 기준 상위 5개 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5).copy()

# ====================
# 📍 지도 시각화 (Folium)
# ====================

st.subheader("🗺 상위 5개 행정구역 인구 분포 지도")

# 행정구역별 좌표 (수동 설정)
region_coords = {
    '경기도': (37.4138, 127.5183),
    '서울특별시': (37.5665, 126.9780),
    '부산광역시': (35.1796, 129.0756),
    '경상남도': (35.4606, 128.2132),
    '인천광역시': (37.4563, 126.7052),
}

# 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

# 원 추가
for _, row in top5_df.iterrows():
    region = row['행정구역']
    population = row['총인구수']
    if region in region_coords:
        lat, lon = region_coords[region]
        folium.Circle(
            location=(lat, lon),
            radius=population / 100,  # 반지름 조정
            color='pink',
            fill=True,
            fill_color='pink',
            fill_opacity=0.4,
            popup=f"{region}: {population:,}명"
        ).add_to(m)

# 지도 표시
st_data = st_folium(m, width=1000, height=600)

# ===========================
# 📊 상위 5개 행정구역 데이터
# ===========================

st.subheader("📊 상위 5개 행정구역 데이터")
st.dataframe(top5_df)

# ================================
# 📈 연령별 인구 변화 선그래프
# ================================

st.subheader("📈 연령별 인구 변화 (선그래프)")

# 연령 컬럼 정렬 (1세 ~ 99세, 100세 이상)
def age_sort_key(label):
    return int(label.replace('세', '')) if label != '100세 이상' else 1000

age_columns_sorted = sorted(top5_df.columns[2:], key=age_sort_key)

# 그래프 출력
for _, row in top5_df.iterrows():
    region = row['행정구역']
    st.write(f"### {region}")
    age_data = row[age_columns_sorted].astype(str).str.replace(',', '').astype(int)
    age_df = pd.DataFrame({
        '연령': age_columns_sorted,
        '인구수': age_data.values
    }).set_index('연령')
    st.line_chart(age_df)
