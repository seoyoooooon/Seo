import pandas as pd
import folium
import re

# CSV 파일 불러오기 (EUC-KR 인코딩)
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 총인구수 숫자형 변환
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

# 상위 5개 행정구역 추출
top5_df = df[['행정구역', '총인구수']].sort_values(by='총인구수', ascending=False).head(5).copy()

# 행정구역명에서 괄호 및 내부 숫자 제거
top5_df['행정구역'] = top5_df['행정구역'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', x))

# 행정구역별 수동 좌표 설정 (중심 좌표)
region_coords = {
    '경기도': (37.4138, 127.5183),
    '서울특별시': (37.5665, 126.9780),
    '부산광역시': (35.1796, 129.0756),
    '경상남도': (35.4606, 128.2132),
    '인천광역시': (37.4563, 126.7052),
}

# 지도 생성 (대한민국 중심)
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

# 각 행정구역에 원 표시
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

# HTML 파일로 저장
m.save("상위5_인구지도.html")
