import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(
    page_title="K-Pop Idol Database",
    page_icon="🎤",
    layout="wide"
)

# 데이터 로드 함수 (캐싱 처리로 속도 향상)
@st.cache_data
def load_data():
    # 파일명은 제공해주신 'kpop_idol.csv' 그대로 매칭합니다.
    df = pd.read_csv("kpop_idol.csv")
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일을 불러오지 못했습니다. 'kpop_idol.csv' 파일이 같은 경로에 있는지 확인해주세요. 에러: {e}")
    st.stop()

# 메인 타이틀
st.title("🎵 K-Pop 아이돌 데이터베이스")
st.markdown("원하는 성별이나 소속사별로 아이돌 데이터를 검색하고 확인해보세요!")

# 사이드바 혹은 탭 구성 (여기서는 깔끔하게 상단 탭으로 구성)
tab1, tab2 = st.tabs(["👫 성별 및 이름 검색", "🏢 소속사별 조회"])

# -------------------------------------------------------------
# TAB 1: 성별 및 이름 검색
# -------------------------------------------------------------
with tab1:
    st.header("성별 및 이름 검색")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 성별 필터 (전체, 남, 여)
        gender_options = ["전체", "남", "여"]
        selected_gender = st.selectbox("성별 선택", gender_options)
        
    with col2:
        # 검색어 입력 (그룹명 또는 이름)
        search_query = st.text_input("아이돌 이름 또는 그룹명 검색", "").strip()
    
    # 데이터 필터링
    filtered_df = df.copy()
    
    if selected_gender != "전체":
        filtered_df = filtered_df[filtered_df["성별"] == selected_gender]
        
    if search_query:
        filtered_df = filtered_df[
            filtered_df["한국이름"].str.contains(search_query, case=False, na=False) |
            filtered_df["영문이름"].str.contains(search_query, case=False, na=False) |
            filtered_df["그룹"].str.contains(search_query, case=False, na=False)
        ]
        
    st.write(f"🔍 검색 결과: 총 {len(filtered_df)}건")
    
    # 결과 보여주기
    if not filtered_df.empty:
        # 주요 컬럼 위주로 데이터프레임 노출 (사진 URL 제외한 깔끔한 표)
        view_cols = ["그룹", "한국이름", "영문이름", "생년월일", "키(cm)", "소속사", "데뷔일", "성별"]
        st.dataframe(filtered_df[view_cols], use_container_width=True)
        
        # 프로필 사진 카드식 배치 (선택 사항)
        st.markdown("### 📸 프로필 사진 보기")
        # 사진이 있는 데이터만 필터링해서 보여주기
        photo_df = filtered_df[filtered_df["photo_url"].notna()]
        
        if not photo_df.empty:
            # 4열 레이아웃으로 사진 배치
            cols = st.columns(4)
            for idx, (_, row) in enumerate(photo_df.iterrows()):
                with cols[idx % 4]:
                    st.image(row["photo_url"], caption=f"{row['그룹']} - {row['한국이름']}", use_container_width=True)
        else:
            st.info("검색된 조건에 해당하는 아이돌의 프로필 사진이 없습니다.")
    else:
        st.warning("검색 결과가 없습니다. 다른 키워드를 입력해보세요.")

# -------------------------------------------------------------
# TAB 2: 소속사별 조회
# -------------------------------------------------------------
with tab2:
    st.header("소속사별 아이돌 조회")
    
    # 소속사 고유값 추출
    companies = sorted(df["소속사"].unique().tolist())
    selected_company = st.selectbox("소속사를 선택하세요", companies)
    
    # 해당 소속사 데이터 필터링
    company_df = df[df["소속사"] == selected_company]
    
    st.subheader(f"🏢 {selected_company} 소속 아이돌 리스트")
    st.write(f"총 {len(company_df)}명의 멤버가 등록되어 있습니다.")
    
    # 요약 통계 정보 간단히 제공
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        # 그룹 목록
        groups = company_df["그룹"].unique()
        st.metric(label="소속 그룹 수", value=len(groups), delta=None)
        st.markdown(f"**활동 그룹**: {', '.join(groups)}")
    with col_stat2:
        # 평균 키 (소수점 첫째자리까지 계산)
        avg_height = company_df["키(cm)"].mean()
        st.metric(label="평균 신장", value=f"{avg_height:.1f} cm", delta=None)
        
    st.markdown("---")
    
    # 데이터 표 출력
    view_cols_comp = ["그룹", "한국이름", "생년월일", "키(cm)", "데뷔일", "성별"]
    st.dataframe(company_df[view_cols_comp].sort_values(by=["그룹", "한국이름"]), use_container_width=True)
    
    # 소속사 멤버 사진 모아보기
    st.markdown("### 📸 소속사 멤버 갤러리")
    company_photo_df = company_df[company_df["photo_url"].notna()]
    
    if not company_photo_df.empty:
        comp_cols = st.columns(5)
        for idx, (_, row) in enumerate(company_photo_df.iterrows()):
            with comp_cols[idx % 5]:
                st.image(row["photo_url"], caption=f"[{row['그룹']}] {row['한국이름']}", use_container_width=True)
    else:
        st.info("이 소속사에는 등록된 사진이 없습니다.")
