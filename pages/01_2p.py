import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="소속사별 조회",
    page_icon="🏢",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("kpop_idol.csv")

df = load_data()

st.title("🏢 소속사별 아이돌 탐색")
st.markdown("특정 기획사를 선택하여 소속 아티스트와 그룹의 다양한 현황을 확인해보세요.")

# 소속사 목록 정렬
agencies = sorted(df["소속사"].unique())
selected_agency = st.selectbox("조회할 소속사(기획사)를 선택하세요", agencies)

# 필터링
agency_df = df[df["소속사"] == selected_agency]

st.subheader(f"✨ {selected_agency} 소속 현황")

col_metric1, col_metric2, col_metric3 = st.columns(3)
with col_metric1:
    st.metric("소속 아티스트 수", f"{len(agency_df)}명")
with col_metric2:
    groups = agency_df["그룹"].unique()
    st.metric("등록 그룹 수", f"{len(groups)}개")
with col_metric3:
    avg_h = agency_df["키(cm)"].mean()
    st.metric("평균 키", f"{avg_h:.1f} cm")

st.markdown(f"**활동 그룹 목록**: {', '.join(groups)}")
st.markdown("---")

# 표 형식으로 보기
st.dataframe(agency_df[["그룹", "한국이름", "생년월일", "키(cm)", "데뷔일", "성별"]].sort_values(by="그룹"), use_container_width=True)

# 갤러리 뷰
st.markdown("### 📸 소속사 멤버 갤러리")
cols = st.columns(5)
for idx, (_, row) in enumerate(agency_df.iterrows()):
    with cols[idx % 5]:
        with st.container(border=True):
            img_url = row["photo_url"] if pd.notna(row["photo_url"]) else "https://placehold.co/300x400/eeeeee/cccccc?text=No+Photo"
            st.image(img_url, use_container_width=True)
            st.caption(f"[{row['그룹']}] {row['한국이름']}")
