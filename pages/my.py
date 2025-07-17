import streamlit as st
import pandas as pd

st.title("🚌 노선별 총 승차승객수 시각화")

uploaded_file = st.file_uploader("📂 CSV 파일을 업로드하세요 (EUC-KR 인코딩)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding="euc-kr")
    except Exception as e:
        st.error(f"❌ 파일 로드 실패: {e}")
    else:
        st.subheader("📋 원본 데이터 (상위 10행)")
        st.dataframe(df.head(10))

        # '노선번호' 열이 있는지 확인
        if '노선번호' not in df.columns:
            st.error("❌ '노선번호'라는 이름의 열이 존재하지 않습니다.")
        else:
            # 승차승객수 관련 열만 필터링
            승차_열들 = [col for col in df.columns if '승차승객수' in col]

            if not 승차_열들:
                st.warning("⚠️ '승차승객수' 관련 열이 존재하지 않습니다.")
            else:
                # 승차승객수를 숫자로 변환
                df[승차_열들] = df[승차_열들].apply(pd.to_numeric, errors='coerce')

                # 노선번호별로 승차승객수 총합 계산
                df_grouped = df.groupby('노선번호')[승차_열들].sum()
                df_grouped['총합승차'] = df_grouped.sum(axis=1)

                # 시각화를 위한 데이터프레임 (노선번호 = index, 총합승차 = values)
                chart_data = df_grouped['총합승차'].sort_index()

                st.subheader("📈 노선번호별 총 승차승객수")
                st.line_chart(chart_data)

                st.success("✅ 분석 완료")
else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
