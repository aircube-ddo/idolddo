import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="아이돌 이름 검색",
    page_icon="👤",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("kpop_idol.csv")

df = load_data()

st.title("👤 K-Pop 아이돌 멤버 검색")
st.markdown("원하는 이름(한국어/영어) 혹은 그룹명을 검색하고 상세 카드를 확인해보세요.")

# 검색창 구성
col1, col2 = st.columns([1, 2])
with col1:
    gender_filter = st.selectbox("성별 필터", ["전체", "남", "여"])
with col2:
    search_query = st.text_input("아이돌 이름 또는 그룹명을 입력하세요")

# 필터링 로직
filtered_df = df.copy()

if gender_filter != "전체":
    filtered_df = filtered_df[filtered_df["성별"] == gender_filter]
    
if search_query:
    filtered_df = filtered_df[
        filtered_df["한국이름"].str.contains(search_query, case=False, na=False) |
        filtered_df["영문이름"].str.contains(search_query, case=False, na=False) |
        filtered_df["그룹"].str.contains(search_query, case=False, na=False)
    ]

st.write(f"🔍 검색 결과 : 총 {len(filtered_df)}명")

if not filtered_df.empty:
    # 전체 데이터 테이블 노출
    st.dataframe(filtered_df.drop(columns=["photo_url"], errors="ignore"), use_container_width=True)
    
    # 카드 레이아웃으로 프로필 노출
    st.markdown("### 📸 프로필 상세 카드")
    cols = st.columns(4)
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        with cols[idx % 4]:
            with st.container(border=True):
                # photo_url이 비어있을 경우 대체 이미지 사용
                img_url = row["photo_url"] if pd.notna(row["photo_url"]) else "https://placehold.co/300x400/eeeeee/cccccc?text=No+Photo"
                st.image(img_url, use_container_width=True)
                st.markdown(f"**이름**: {row['한국이름']} ({row['영문이름']})")
                st.markdown(f"**그룹**: {row['그룹']}")
                st.markdown(f"**소속사**: {row['소속사']}")
                st.markdown(f"**생년월일**: {row['생년월일']}")
                st.markdown(f"**키**: {row['키(cm)']}cm")
else:
    st.warning("조건에 부합하는 아이돌을 찾을 수 없습니다.")
