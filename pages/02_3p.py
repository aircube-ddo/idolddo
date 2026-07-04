import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="아이돌 신장 분석",
    page_icon="📏",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("kpop_idol.csv")

df = load_data()

st.title("📏 K-Pop 아이돌 신장(키) 분포 분석")
st.markdown("전체 아이돌들의 신장 데이터를 기반으로 한 통계 요약과 분포 그래프, 맞춤형 탐색을 제공합니다.")

# 1. 성별 평균 신장 비교
st.subheader("💡 성별 평균 신장")
avg_m = df[df["성별"] == "남"]["키(cm)"].mean()
avg_f = df[df["성별"] == "여"]["키(cm)"].mean()

col1, col2 = st.columns(2)
with col1:
    st.info(f"♂️ **남자 아이돌 평균 키**: {avg_m:.1f} cm")
with col2:
    st.success(f"♀️ **여자 아이돌 평균 키**: {avg_f:.1f} cm")

# 2. 신장 기준 랭킹
st.subheader("🏆 키 랭킹 TOP 5")
rank_col1, rank_col2 = st.columns(2)

with rank_col1:
    st.markdown("🥇 **최장신 멤버 TOP 5**")
    tallest = df.sort_values(by="키(cm)", ascending=False).head(5)
    st.dataframe(tallest[["한국이름", "그룹", "소속사", "키(cm)", "성별"]], use_container_width=True)
    
with rank_col2:
    st.markdown("🥈 **최단신 멤버 TOP 5**")
    shortest = df.sort_values(by="키(cm)", ascending=True).head(5)
    st.dataframe(shortest[["한국이름", "그룹", "소속사", "키(cm)", "성별"]], use_container_width=True)

st.markdown("---")

# 3. 키 구간 검색 기능
st.subheader("🔍 신장 대역별 맞춤 검색")
min_h = int(df["키(cm)"].min())
max_h = int(df["키(cm)"].max())

selected_range = st.slider("원하는 키 대역을 선택해 주세요 (cm)", min_h, max_h, (165, 185))

ranged_df = df[(df["키(cm)"] >= selected_range[0]) & (df["키(cm)"] <= selected_range[1])]
st.write(f"👉 **{selected_range[0]}cm ~ {selected_range[1]}cm** 구간의 아이돌: 총 {len(ranged_df)}명")
st.dataframe(ranged_df[["그룹", "한국이름", "소속사", "키(cm)", "성별"]].sort_values(by="키(cm)", ascending=False), use_container_width=True)

st.markdown("---")

# 4. 시각화 (Plotly)
st.subheader("📊 전체 신장 분포도 (히스토그램)")
fig = px.histogram(
    df, 
    x="키(cm)", 
    color="성별", 
    barmode="overlay",
    title="남/여 아이돌 신장 분포 비교",
    labels={"키(cm)": "키 (cm)", "count": "명수"},
    color_discrete_map={"남": "#1E88E5", "여": "#FF8F00"}
)
st.plotly_chart(fig, use_container_width=True)
