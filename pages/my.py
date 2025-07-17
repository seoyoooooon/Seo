import streamlit as st
import pandas as pd

# Streamlit 앱 제목
st.title("🚌 노선번호별 승차승객수 합계 시각화")

# CSV 파일 업로드
uploaded_file = st.file_uploader("📂 CSV 파일을 업로드하세요 (EUC-KR 인코딩)", type="csv")

if uploaded_file is not None:
    # 파일 읽기
    df = pd.read_csv(uploaded_file, encoding="euc-kr")

    st.subheader("📋 원본 데이터 미리보기")
    st.dataframe(df.head())

    # '노선번호' 열 존재 확인
    if '노선번호' not in df.columns:
        st.error("❌ '노선번호' 열이 존재하지 않습니다.")
    else:
        # '승차승객수'가 들어간 열만 필터링
        승차_열들 = [col for col in df.columns if '승차승객수' in col]

        if not 승차_열들:
            st.warning("⚠️ '승차승객수' 열이 없습니다.")
        else:
            # 승차 데이터 숫자로 변환
            df[승차_열들] = df[승차_열들].apply(pd.to_numeric, errors='coerce')

            # 노선번호별로 승차승객수 합계 계산
            df_grouped = df.groupby('노선번호')[승차_열들].sum()
            df_grouped['총합승차'] = df_grouped.sum(axis=1)

            # 시각화용 데이터 준비
            chart_data = df_grouped['총합승차'].sort_index()

            st.subheader("📈 노선번호별 총 승차승객수")
            st.line_chart(chart_data)

            st.success("✅ 분석이 완료되었습니다.")
else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
