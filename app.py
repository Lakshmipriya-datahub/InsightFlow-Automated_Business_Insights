

import pandas as pd
import plotly.express as px
import streamlit as st


from insight_engine import run_insight_pipeline


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Automated Business Insight Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)



# ============================================================
# PROFESSIONAL BLACK + NAVY BLUE THEME
# ============================================================

st.markdown("""
<style>

/* ==================== GLOBAL ==================== */

.stApp {
    background: #05070D;
    color: #F5F7FA;
    font-family: "Inter", "Segoe UI", Arial, sans-serif;
}

.block-container {
    max-width: 1450px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}


/* ==================== SIDEBAR ==================== */

section[data-testid="stSidebar"] {
    background: #02040A;
    border-right: 1px solid #17243A;
}

section[data-testid="stSidebar"] * {
    color: #F5F7FA !important;
}

section[data-testid="stSidebar"] h2 {
    font-size: 20px !important;
    font-weight: 700 !important;
    letter-spacing: -0.2px;
}

.sidebar-engine {
    font-size: 14px;
    font-weight: 500;
    padding: 9px 0;
    color: #CBD5E1;
}

.sidebar-engine span {
    display: inline-block;
    width: 28px;
    font-size: 16px;
}


/* ==================== MAIN TITLE ==================== */

.main-title {
    font-size: 34px;
    font-weight: 750;
    color: #FFFFFF;
    letter-spacing: -0.8px;
    margin-bottom: 6px;
    line-height: 1.2;
}

.subtitle {
    color: #94A3B8;
    font-size: 15px;
    line-height: 1.6;
    max-width: 850px;
    margin-bottom: 30px;
}


/* ==================== SECTION HEADINGS ==================== */

.section-title {
    font-size: 23px;
    font-weight: 700;
    color: #F8FAFC;
    margin-top: 32px;
    margin-bottom: 8px;
}

.section-subtitle {
    color: #94A3B8;
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 18px;
}


/* ==================== KPI CARDS ==================== */

.kpi-card {
    background: #0A1020;
    border: 1px solid #1B2A44;
    border-radius: 14px;
    padding: 18px;
    min-height: 112px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.25);
}

.kpi-label {
    color: #94A3B8;
    font-size: 13px;
    font-weight: 500;
}

.kpi-value {
    color: #FFFFFF;
    font-size: 27px;
    font-weight: 750;
    margin-top: 8px;
}


/* ==================== INSIGHT CARDS ================= */

/* ==================== ANALYSIS / INSIGHT HOVER BOXES ================= */

.insight-card {
    background: linear-gradient(
        135deg,
        #0B1220 0%,
        #080E1A 100%
    );

    border: 1px solid #1B2A44;
    border-radius: 14px;

    padding: 18px 20px;
    min-height: 70px;
    margin-bottom: 14px;

    line-height: 1.6;

    box-shadow:
        0 5px 18px rgba(0, 0, 0, 0.22);

    /* Scroll-in animation */
    animation-name: insightScrollIn;
    animation-duration: 1ms;
    animation-timing-function: linear;
    animation-fill-mode: both;

    animation-timeline: view();
    animation-range: entry 0% cover 35%;

    /* Smooth hover */
    transition:
        transform 0.3s ease,
        border-color 0.3s ease,
        box-shadow 0.3s ease;
}


/* Scroll animation */

@keyframes insightScrollIn {

    from {
        opacity: 0;
        transform: translateY(35px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}


/* Hover / Touch effect */

.insight-card:hover {
    transform: translateY(-4px);

    border-color: #2563EB;

    box-shadow:
        0 0 0 1px #0B1F3A,
        0 8px 24px rgba(37, 99, 235, 0.22);
}
/* ==================== CHART HOVER EFFECT ==================== */

div[data-testid="stPlotlyChart"] {
    border: 1px solid #1B2A44;
    border-radius: 14px;
    transition:
        transform 0.25s ease,
        border-color 0.25s ease,
        box-shadow 0.25s ease;
    overflow: hidden;
}

div[data-testid="stPlotlyChart"]:hover {
    border-color: #2563EB;

    box-shadow:
        0 0 0 1px #0B1F3A,
        0 8px 24px rgba(37, 99, 235, 0.22);

    transform: translateY(-3px);
}
/* ==================== SUMMARY CARD ==================== */

.summary-card {
    background: #091120;
    border: 1px solid #1B2D4A;
    border-radius: 14px;
    padding: 22px;
    line-height: 1.7;
    color: #CBD5E1;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.22);
}


/* ==================== BUSINESS CARD ==================== */

.business-card {
    background: #080E1A;
    border: 1px solid #1A2942;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
    line-height: 1.6;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18);
}


/* ==================== BADGE ==================== */

.badge {
    display: inline-block;
    background: #0B1B35;
    border: 1px solid #1D4ED8;
    color: #60A5FA;
    border-radius: 20px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 600;
    margin-bottom: 8px;
}


/* ==================== PROFILE / CLEANING ==================== */

.profile-item,
.cleaning-item {
    color: #CBD5E1;
    padding: 4px 0;
    line-height: 1.6;
}


/* ==================== FILTER AREA ==================== */

.filter-section {
    background: #080E1A;
    border: 1px solid #1A2942;
    border-radius: 16px;
    padding: 22px 24px 20px 24px;
    margin: 12px 0 24px 0;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.20);
}

.filter-subtitle {
    color: #94A3B8;
    font-size: 13px;
    margin-bottom: 18px;
}

div[data-testid="stSelectbox"] label {
    color: #CBD5E1 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}


/* ==================== GENERAL TEXT ==================== */

p, li {
    line-height: 1.65;
}

h1, h2, h3, h4 {
    letter-spacing: -0.3px;
    color: #F8FAFC;
}

</style>
""", unsafe_allow_html=True)
# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">InsightFlow — Automated Business Insights</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload your dataset to automatically profile, clean, analyze, '
    'detect patterns, and generate actionable business insights.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Insight Engine")

    st.markdown("""
    **Five-Engine Architecture**

    1. Data Profiling Engine
    2. Data Cleaning Engine
    3. Pattern Detection Engine
    4. Automated Analysis Engine
    5. AI Insight Engine
    """)

    st.divider()

    # Dataset uploader section continues below
# ============================================================
# DATASET UPLOAD
# ============================================================

if "datasets" not in st.session_state:
    st.session_state.datasets = {}

uploaded_files = st.file_uploader(
    "Upload Dataset",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

if uploaded_files:

    for uploaded_file in uploaded_files:

        file_name = uploaded_file.name

        # Keep already uploaded datasets
        if file_name in st.session_state.datasets:
            continue

        try:

            if file_name.lower().endswith(".csv"):
                uploaded_df = pd.read_csv(uploaded_file)

            else:
                uploaded_df = pd.read_excel(uploaded_file)

            st.session_state.datasets[file_name] = uploaded_df

        except Exception as e:

            st.error(
                f"❌ Unable to read {file_name}: {e}"
            )


# ============================================================
# DATASET SELECTION
# ============================================================

if not st.session_state.datasets:

    st.info(
        "👆 Upload a CSV or Excel dataset from the sidebar to start."
    )

    st.stop()


dataset_names = list(
    st.session_state.datasets.keys()
)


if len(dataset_names) == 1:

    selected_dataset = dataset_names[0]

else:

    selected_dataset = st.selectbox(
        "Select Dataset",
        dataset_names
    )


df = st.session_state.datasets[
    selected_dataset
].copy()

st.caption(
    f"📁 **{selected_dataset}**  •  "
    f"{len(df):,} rows  •  {len(df.columns):,} columns"
)

# ============================================================
# INTERACTIVE FILTERS
# ============================================================

st.markdown(
    '<div class="section-title">Interactive Filters</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Use the filters below to explore your dataset and focus on specific segments.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("""
<style>

.filter-section {
    background: #080E1A;
    border: 1px solid #1A2942;
    border-radius: 16px;
    padding: 22px 24px 20px 24px;
    margin: 12px 0 24px 0;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.20);
}

.filter-subtitle {
    color: #94A3B8;
    font-size: 13px;
    line-height: 1.6;
    margin-bottom: 18px;
}

div[data-testid="stSelectbox"] label {
    color: #CBD5E1 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

div[data-baseweb="select"] > div {
    background: #0B1220 !important;
    border-color: #243653 !important;
    color: #F8FAFC !important;
}
/* ============================================================
   FILTER SELECTBOX — CLEAN NAVY FOCUS
   ============================================================ */

div[data-testid="stSelectbox"] [data-baseweb="select"] {
    background-color: #0B1220 !important;
    border-radius: 8px !important;
    outline: none !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background-color: #0B1220 !important;
    border: 1px solid #1B2A44 !important;
    border-radius: 8px !important;
    outline: none !important;
    box-shadow: none !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] * {
    outline: none !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] > div:focus,
div[data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-visible,
div[data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within {
    border-color: #2563EB !important;
    outline: none !important;
    box-shadow: 0 0 0 1px #2563EB !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"]:focus-within {
    outline: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# PLATFORM DETECTION
# ============================================================

platform_columns = [
    col for col in [
        "Netflix",
        "Zee5",
        "Jio Cinema",
        "Prime Video",
        "Disney+ Hotstar"
    ]
    if col in df.columns
]

platform_column = None

for col in df.columns:
    normalized = col.lower().strip().replace("_", " ")

    if normalized in [
        "platform",
        "platform name",
        "streaming platform"
    ]:
        platform_column = col
        break


# ============================================================
# FILTER DEFINITIONS
# ============================================================

filter_definitions = []

# ONE Platform filter for the five Boolean platform columns
if platform_columns:
    filter_definitions.append(
        {
            "name": "Platform",
            "type": "boolean_platform"
        }
    )

# Platform filter for datasets having one Platform column
elif platform_column:
    filter_definitions.append(
        {
            "name": "Platform",
            "type": "normal_platform",
            "column": platform_column
        }
    )


# ============================================================
# YEAR FILTER
# ============================================================

year_column = None

for col in df.columns:
    normalized = col.lower().strip().replace("_", " ")

    if normalized in [
        "year",
        "posting year",
        "release year"
    ]:
        year_column = col
        break

if year_column:
    filter_definitions.append(
        {
            "name": "Year",
            "type": "normal",
            "column": year_column
        }
    )


# ============================================================
# OTHER DYNAMIC FILTERS
# ============================================================

priority_keywords = [
    "language",
    "genre",
    "category",
    "industry",
    "country",
    "region",
    "city",
    "segment",
    "department",
    "status",
    "type",
    "channel",
    "brand"
]


def is_id_column(column):
    name = column.lower().strip().replace("_", " ")

    return (
        name == "id"
        or name.endswith(" id")
        or "identifier" in name
    )


for keyword in priority_keywords:

    if len(filter_definitions) >= 5:
        break

    for col in df.columns:

        if len(filter_definitions) >= 5:
            break

        if col == year_column:
            continue

        if col in platform_columns:
            continue

        if col == platform_column:
            continue

        if is_id_column(col):
            continue

        normalized = col.lower().strip().replace("_", " ")

        if keyword not in normalized:
            continue

        if (
            pd.api.types.is_object_dtype(df[col])
            or pd.api.types.is_categorical_dtype(df[col])
        ):

            unique_count = df[col].nunique(dropna=True)

            if 2 <= unique_count <= 100:

                filter_definitions.append(
                    {
                        "name": col,
                        "type": "normal",
                        "column": col
                    }
                )

                break


# ============================================================
# FALLBACK FILTERS
# ============================================================

if len(filter_definitions) < 5:

    for col in df.columns:

        if len(filter_definitions) >= 5:
            break

        if col == year_column:
            continue

        if col in platform_columns:
            continue

        if col == platform_column:
            continue

        if is_id_column(col):
            continue

        already_used = any(
            item.get("column") == col
            for item in filter_definitions
        )

        if already_used:
            continue

        if (
            pd.api.types.is_object_dtype(df[col])
            or pd.api.types.is_categorical_dtype(df[col])
        ):

            unique_count = df[col].nunique(dropna=True)

            if 2 <= unique_count <= 50:

                filter_definitions.append(
                    {
                        "name": col,
                        "type": "normal",
                        "column": col
                    }
                )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

filter_definitions = filter_definitions[:5]


# ============================================================
# ROW 1 — MAXIMUM 3 FILTERS
# ============================================================

row1 = st.columns(3)

for i, filter_info in enumerate(filter_definitions[:3]):

    with row1[i]:

        filter_name = filter_info["name"]
        filter_type = filter_info["type"]

        # ---------------- PLATFORM ----------------
        if filter_type == "boolean_platform":

            options = [
                "All Platforms",
                "Netflix",
                "Zee5",
                "Jio Cinema",
                "Prime Video",
                "Disney+ Hotstar"
            ]

            selected = st.selectbox(
                "Platform",
                options,
                key="platform_filter"
            )

            if selected != "All Platforms":

                filtered_df = filtered_df[
                    filtered_df[selected]
                    .astype(str)
                    .str.lower()
                    .isin(["true", "1", "yes"])
                ]

        # ---------------- NORMAL PLATFORM ----------------
        elif filter_type == "normal_platform":

            column = filter_info["column"]

            values = sorted(
                df[column]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected = st.selectbox(
                "Platform",
                ["All Platforms"] + values,
                key="platform_filter_normal"
            )

            if selected != "All Platforms":

                filtered_df = filtered_df[
                    filtered_df[column].astype(str) == selected
                ]

        # ---------------- NORMAL FILTER ----------------
        else:

            column = filter_info["column"]

            values = df[column].dropna().astype(str).unique().tolist()

            try:
                values = sorted(
                    values,
                    key=lambda x: float(x)
                )
            except:
                values = sorted(values)

            selected = st.selectbox(
                filter_name,
                ["All"] + values,
                key=f"filter_{i}_{filter_name}"
            )

            if selected != "All":

                filtered_df = filtered_df[
                    filtered_df[column].astype(str) == selected
                ]


# ============================================================
# ROW 2 — REMAINING FILTERS
# ============================================================

if len(filter_definitions) > 3:

    row2 = st.columns(3)

    for j, filter_info in enumerate(filter_definitions[3:5]):

        with row2[j]:

            filter_name = filter_info["name"]
            filter_type = filter_info["type"]

            # ---------------- PLATFORM ----------------
            if filter_type == "boolean_platform":

                options = [
                    "All Platforms",
                    "Netflix",
                    "Zee5",
                    "Jio Cinema",
                    "Prime Video",
                    "Disney+ Hotstar"
                ]

                selected = st.selectbox(
                    "Platform",
                    options,
                    key="platform_filter_row2"
                )

                if selected != "All Platforms":

                    filtered_df = filtered_df[
                        filtered_df[selected]
                        .astype(str)
                        .str.lower()
                        .isin(["true", "1", "yes"])
                    ]

            # ---------------- NORMAL PLATFORM ----------------
            elif filter_type == "normal_platform":

                column = filter_info["column"]

                values = sorted(
                    df[column]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                selected = st.selectbox(
                    "Platform",
                    ["All Platforms"] + values,
                    key="platform_filter_normal_row2"
                )

                if selected != "All Platforms":

                    filtered_df = filtered_df[
                        filtered_df[column].astype(str) == selected
                    ]

            # ---------------- NORMAL FILTER ----------------
            else:

                column = filter_info["column"]

                values = (
                    df[column]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                try:
                    values = sorted(
                        values,
                        key=lambda x: float(x)
                    )
                except:
                    values = sorted(values)

                selected = st.selectbox(
                    filter_name,
                    ["All"] + values,
                    key=f"filter_row2_{j}_{filter_name}"
                )

                if selected != "All":

                    filtered_df = filtered_df[
                        filtered_df[column].astype(str) == selected
                    ]


# ============================================================
# FILTER RESULT
# ============================================================

st.markdown(
    f"""
    <div style="
        color:#94A3B8;
        font-size:13px;
        margin-top:8px;
        margin-bottom:20px;
    ">
        Showing
        <b style="color:#E2E8F0;">{len(filtered_df):,}</b>
        of
        <b style="color:#E2E8F0;">{len(df):,}</b>
        rows
    </div>
    """,
    unsafe_allow_html=True
)
# ============================================================
# FIVE ENGINE PIPELINE
# ============================================================

with st.spinner(
    "🚀 Running five-engine business insight pipeline..."
):

    try:

        results = run_insight_pipeline(filtered_df)

    except Exception as e:

        st.error(
            f"❌ Insight pipeline failed: {e}"
        )

        st.stop()


profiling_report = results.get(
    "profiling_report",
    {}
)

cleaned_df = results.get(
    "cleaned_df",
    filtered_df.copy()
)

cleaning_report = results.get(
    "cleaning_report",
    {}
)

pattern_report = results.get(
    "pattern_report",
    {}
)

analysis_report = results.get(
    "analysis_report",
    []
)

ai_insights = results.get(
    "ai_insights",
    {}
)


# ============================================================
# ANALYSIS FINDINGS
# ============================================================

if isinstance(analysis_report, list):

    findings = analysis_report

elif isinstance(analysis_report, dict):

    findings = analysis_report.get(
        "findings",
        []
    )

else:

    findings = []


# Keep only the first 7 meaningful findings
findings = [
    finding
    for finding in findings
    if finding
][:7]


# ============================================================
# CORRELATIONS
# ============================================================

correlations = []

if isinstance(pattern_report, dict):

    correlation_data = pattern_report.get(
        "correlation_analysis",
        []
    )

    if isinstance(correlation_data, list):

        correlations = correlation_data

    elif isinstance(correlation_data, dict):

        correlations = correlation_data.get(
            "correlations",
            []
        )


# ============================================================
# AI-GENERATED EXECUTIVE SUMMARY
# ============================================================

executive_summary = ai_insights.get(
    "executive_summary",
    "The dataset was successfully analysed using automated profiling, "
    "cleaning, pattern detection and analytical engines."
)

st.markdown("#### AI Executive Summary")

st.caption(
    "Automatically generated from the detected patterns and analytical results."
)

st.info(executive_summary)


# ============================================================
# DYNAMIC BUSINESS KPI ENGINE
# ============================================================

def generate_business_kpis(dataframe):

    kpis = []

    # --------------------------------------------------------
    # Helper: Find column by priority keywords
    # --------------------------------------------------------

    def find_column(keywords):

        for keyword in keywords:

            for col in dataframe.columns:

                normalized = (
                    str(col)
                    .lower()
                    .strip()
                    .replace("_", " ")
                )

                if keyword in normalized:
                    return col

        return None


    # --------------------------------------------------------
    # Helper: Check numeric column
    # --------------------------------------------------------

    def numeric_column(column):

        if column is None:
            return None

        values = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )

        if values.notna().sum() > 0:
            return values

        return None


    # ========================================================
    # FIND IMPORTANT BUSINESS COLUMNS
    # ========================================================

    entity_column = find_column([
        "product name",
        "product",
        "item name",
        "item",
        "title",
        "movie",
        "customer name",
        "customer",
        "employee name",
        "employee",
        "name"
    ])


    revenue_column = find_column([
        "revenue",
        "sales amount",
        "sales",
        "total amount",
        "order value",
        "amount",
        "turnover"
    ])


    profit_column = find_column([
        "profit",
        "net profit",
        "gross profit"
    ])


    rating_column = find_column([
        "rating",
        "score",
        "satisfaction"
    ])


    category_column = find_column([
        "product category",
        "category",
        "genre",
        "industry",
        "department",
        "segment"
    ])


    # ========================================================
    # 1. TOTAL RECORDS / ENTITIES
    # ========================================================

    if entity_column:

        unique_count = dataframe[entity_column].nunique(
            dropna=True
        )

        kpis.append(
            (
                f"Total {entity_column}s",
                f"{unique_count:,}"
            )
        )

    else:

        kpis.append(
            (
                "Total Records",
                f"{len(dataframe):,}"
            )
        )


    # ========================================================
    # 2. TOTAL REVENUE / SALES
    # ========================================================

    value_column = revenue_column or profit_column

    if value_column:

        values = numeric_column(value_column)

        if values is not None:

            total_value = values.sum()

            column_name = str(value_column).lower()

            if "profit" in column_name:

                label = "Total Profit"

            elif "revenue" in column_name:

                label = "Total Revenue"

            else:

                label = "Total Sales"


            kpis.append(
                (
                    label,
                    f"{total_value:,.2f}"
                )
            )


    # ========================================================
    # 3. AVERAGE REVENUE / SALES / PROFIT
    # ========================================================

    if value_column:

        values = numeric_column(value_column)

        if values is not None:

            average_value = values.mean()

            column_name = str(value_column).lower()

            if "profit" in column_name:

                label = "Average Profit"

            elif "revenue" in column_name:

                label = "Average Revenue"

            else:

                label = "Average Sales"


            kpis.append(
                (
                    label,
                    f"{average_value:,.2f}"
                )
            )


    # ========================================================
    # 4. AVERAGE RATING / SCORE
    # ========================================================

    if rating_column:

        values = numeric_column(rating_column)

        if values is not None:

            column_name = str(rating_column).lower()

            if "imdb" in column_name:

                label = "Average IMDb Rating"

            elif "satisfaction" in column_name:

                label = "Average Satisfaction"

            else:

                label = f"Average {rating_column}"


            kpis.append(
                (
                    label,
                    f"{values.mean():.2f}"
                )
            )


    # ========================================================
    # 5. TOP CATEGORY
    # ========================================================

    if category_column:

        category_counts = (
            dataframe[category_column]
            .dropna()
            .astype(str)
            .value_counts()
        )

        if not category_counts.empty:

            top_category = category_counts.index[0]

            kpis.append(
                (
                    f"Top {category_column}",
                    str(top_category)
                )
            )


    # ========================================================
    # 6. PROFIT MARGIN
    # ========================================================

    if revenue_column and profit_column:

        revenue_values = numeric_column(revenue_column)
        profit_values = numeric_column(profit_column)

        if (
            revenue_values is not None
            and profit_values is not None
        ):

            total_revenue = revenue_values.sum()
            total_profit = profit_values.sum()

            if total_revenue != 0:

                margin = (
                    total_profit
                    / total_revenue
                ) * 100

                kpis.append(
                    (
                        "Profit Margin",
                        f"{margin:.2f}%"
                    )
                )


    # ========================================================
    # 7. TOP PERFORMING ENTITY
    # ========================================================

    if entity_column and value_column:

        entity_data = pd.DataFrame({
            "Entity": dataframe[entity_column],
            "Value": numeric_column(value_column)
        }).dropna()

        if not entity_data.empty:

            entity_performance = (
                entity_data
                .groupby("Entity")["Value"]
                .sum()
                .sort_values(ascending=False)
            )

            if not entity_performance.empty:

                top_entity = entity_performance.index[0]

                column_name = str(value_column).lower()

                if "profit" in column_name:

                    label = "Top Profit Contributor"

                elif (
                    "revenue" in column_name
                    or "sales" in column_name
                ):

                    label = "Top Revenue Contributor"

                else:

                    label = "Top Performing Entity"


                kpis.append(
                    (
                        label,
                        str(top_entity)
                    )
                )


    # ========================================================
    # REMOVE DUPLICATE KPI LABELS
    # ========================================================

    final_kpis = []

    seen = set()

    for label, value in kpis:

        if label not in seen:

            final_kpis.append(
                (
                    label,
                    value
                )
            )

            seen.add(label)


    # ========================================================
    # MAXIMUM 7 KPIs
    # ========================================================

    return final_kpis[:7]

# ============================================================
# GENERATE BUSINESS KPIs
# ============================================================

business_kpis = generate_business_kpis(
    filtered_df
)


# ============================================================
# KEY PERFORMANCE INDICATORS
# ============================================================

st.markdown(
    '<div class="section-title" style="font-size:21px; margin-top:30px;">'
    'Key Performance Indicators'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Business KPIs are automatically identified from the selected dataset.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# PROFESSIONAL KPI CARD STYLE
# ============================================================

st.markdown(
    """
    <style>

    div[data-testid="stMetric"] {

        background: linear-gradient(
            135deg,
            #0B1220 0%,
            #080E1A 100%
        );

        border: 1px solid #1B2A44;

        border-radius: 14px;

        padding: 18px 20px;

        min-height: 118px;

        margin-bottom: 10px;

        box-shadow:
            0 5px 18px rgba(0, 0, 0, 0.22);
            transaction: trasaction 0.3s ease, box-shadow 0.3s ease;
            animation: kpiAppear 0.6s ease both;

    }


    div[data-testid="stMetric"]:hover {

        border-color: #2563EB;

        box-shadow:
            0 6px 20px rgba(37, 99, 235, 0.12);

    }


    div[data-testid="stMetricLabel"] {

        color: #94A3B8 !important;

        font-size: 13px !important;

        font-weight: 600 !important;

        white-space: normal !important;

        overflow: visible !important;

        text-overflow: clip !important;

        line-height: 1.4 !important;

    }


    div[data-testid="stMetricValue"] {

        color: #F8FAFC !important;

        font-size: 21px !important;

        font-weight: 700 !important;

        white-space: normal !important;

        overflow-wrap: anywhere !important;

        word-break: break-word !important;

        line-height: 1.3 !important;

        margin-top: 6px !important;

    }
    @keyframes kpiAppear {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# KPI LAYOUT — TWO ROWS
# ============================================================

if business_kpis:

    # --------------------------------------------------------
    # FIRST ROW — 4 KPIs
    # --------------------------------------------------------

    first_row = business_kpis[:4]

    columns = st.columns(4)


    for column, (label, value) in zip(
        columns,
        first_row
    ):

        with column:

            st.metric(
                label=label,
                value=value
            )


    # --------------------------------------------------------
    # SECOND ROW — REMAINING 3 KPIs
    # --------------------------------------------------------

    second_row = business_kpis[4:7]


    if second_row:

        st.markdown(
            "<div style='height:8px;'></div>",
            unsafe_allow_html=True
        )


        columns = st.columns(4)


        for column, (label, value) in zip(
            columns,
            second_row
        ):

            with column:

                st.metric(
                    label=label,
                    value=value
                )


else:

    st.info(
        "No suitable business KPIs could be automatically "
        "identified from this dataset."
    )


# ============================================================
# DATA QUALITY & PROFILING
# ============================================================

st.markdown(
    '<div class="section-title">Data Quality & Profiling</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'A structured overview of the dataset quality, structure, and detected column types.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# PROFILING DATA
# ============================================================

profile_numeric_columns = profiling_report.get(
    "numeric_columns",
    []
)

profile_categorical_columns = profiling_report.get(
    "categorical_columns",
    []
)

profile_boolean_columns = profiling_report.get(
    "boolean_columns",
    []
)

profile_datetime_columns = profiling_report.get(
    "datetime_columns",
    []
)

profile_duplicate_rows = profiling_report.get(
    "duplicate_rows",
    0
)

profile_missing_values = profiling_report.get(
    "missing_values",
    0
)


# ============================================================
# SAFE DATA QUALITY COUNT
# ============================================================

def get_quality_count(value, dataframe=None):

    # --------------------------------------------------------
    # Direct numeric value
    # --------------------------------------------------------

    if isinstance(value, (int, float)):

        return int(value)


    # --------------------------------------------------------
    # Dictionary value
    # --------------------------------------------------------

    if isinstance(value, dict):

        for key in [
            "total_missing",
            "missing_count",
            "count",
            "total",
            "value"
        ]:

            if key in value:

                try:
                    return int(value[key])
                except:
                    pass


        # ----------------------------------------------------
        # Column-wise numeric values
        # ----------------------------------------------------

        try:

            numeric_values = [
                int(v)
                for v in value.values()
                if isinstance(v, (int, float))
            ]

            if numeric_values:

                return sum(numeric_values)

        except:

            pass


    # --------------------------------------------------------
    # Final fallback — calculate directly
    # --------------------------------------------------------

    if dataframe is not None:

        try:

            return int(
                dataframe.isna().sum().sum()
            )

        except:

            pass


    return 0


# ============================================================
# QUALITY COUNTS
# ============================================================

missing_count = get_quality_count(
    profile_missing_values,
    df
)

duplicate_count = get_quality_count(
    profile_duplicate_rows,
    df
)


# ============================================================
# INCONSISTENT RECORDS
# ============================================================

def get_inconsistent_records(report):

    if not isinstance(report, dict):

        return 0


    possible_keys = [
        "inconsistent_records",
        "inconsistent_rows",
        "inconsistent_count",
        "inconsistency_count",
        "invalid_records",
        "invalid_rows",
        "invalid_count"
    ]


    for key in possible_keys:

        if key in report:

            value = report[key]


            # Direct numeric value

            if isinstance(
                value,
                (int, float)
            ):

                return int(value)


            # Nested dictionary

            if isinstance(value, dict):

                for sub_key in [
                    "count",
                    "total",
                    "records",
                    "rows",
                    "value"
                ]:

                    if sub_key in value:

                        try:

                            return int(
                                value[sub_key]
                            )

                        except:

                            pass


    return 0


inconsistent_count = get_inconsistent_records(
    profiling_report
)


# ============================================================
# DATA QUALITY OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title" '
    'style="font-size:20px; margin-top:28px;">'
    'Data Quality Overview'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Key quality indicators detected during the profiling stage.'
    '</div>',
    unsafe_allow_html=True
)


quality_col1, quality_col2, quality_col3 = st.columns(3)


with quality_col1:

    st.metric(
        "Missing Values",
        f"{missing_count:,}"
    )


with quality_col2:

    st.metric(
        "Duplicate Rows",
        f"{duplicate_count:,}"
    )


with quality_col3:

    st.metric(
        "Inconsistent Records",
        f"{inconsistent_count:,}"
    )

# ============================================================
# COLUMN TYPE SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title" '
    'style="font-size:20px; margin-top:30px;">'
    'Column Type Summary'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Detected column types used by the automated analysis pipeline.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# BOOLEAN-LIKE COLUMN DETECTION
# ============================================================

def detect_boolean_like_columns(dataframe):

    boolean_columns = []

    for column in dataframe.columns:

        # Remove missing values
        values = dataframe[column].dropna()

        if values.empty:
            continue

        # Normalize values for comparison
        normalized_values = (
            values.astype(str)
            .str.strip()
            .str.lower()
        )

        unique_values = set(
            normalized_values.unique()
        )

        # TRUE / FALSE
        true_false_pattern = unique_values.issubset(
            {"true", "false"}
        )

        # YES / NO
        yes_no_pattern = unique_values.issubset(
            {"yes", "no"}
        )

        # 1 / 0
        one_zero_pattern = unique_values.issubset(
            {"1", "0"}
        )

        # BOOLEAN-LIKE COLUMN
        if (
            true_false_pattern
            or yes_no_pattern
            or one_zero_pattern
        ):
            boolean_columns.append(column)

    return boolean_columns


# ============================================================
# DETECT BOOLEAN-LIKE COLUMNS
# ============================================================

profile_boolean_columns = detect_boolean_like_columns(df)


# ============================================================
# COLUMN TYPE KPI CARDS
# ============================================================

type_col1, type_col2, type_col3, type_col4 = st.columns(4)

with type_col1:

    st.metric(
        "Numeric",
        len(profile_numeric_columns)
    )

with type_col2:

    st.metric(
        "Categorical",
        len(profile_categorical_columns)
    )

with type_col3:

    st.metric(
        "Boolean",
        len(profile_boolean_columns)
    )

with type_col4:

    st.metric(
        "Date & Time",
        len(profile_datetime_columns)
    )


# ============================================================
# COLUMN DETAILS
# ============================================================

st.markdown(
    '<div style="height:8px;"></div>',
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# NUMERIC + CATEGORICAL
# ------------------------------------------------------------

detail_col1, detail_col2 = st.columns(2)

with detail_col1:

    with st.expander(
        f"Numeric Columns  ·  {len(profile_numeric_columns)}"
    ):

        if profile_numeric_columns:

            for column in profile_numeric_columns:

                st.markdown(
                    f"- `{column}`"
                )

        else:

            st.caption(
                "No numeric columns detected."
            )


with detail_col2:

    with st.expander(
        f"Categorical Columns  ·  {len(profile_categorical_columns)}"
    ):

        if profile_categorical_columns:

            for column in profile_categorical_columns:

                st.markdown(
                    f"- `{column}`"
                )

        else:

            st.caption(
                "No categorical columns detected."
            )


# ------------------------------------------------------------
# BOOLEAN + DATE & TIME
# ------------------------------------------------------------

detail_col3, detail_col4 = st.columns(2)

with detail_col3:

    with st.expander(
        f"Boolean Columns  ·  {len(profile_boolean_columns)}"
    ):

        if profile_boolean_columns:

            for column in profile_boolean_columns:

                st.markdown(
                    f"- `{column}`"
                )

        else:

            st.caption(
                "No Boolean-like columns detected."
            )


with detail_col4:

    with st.expander(
        f"Date & Time Columns  ·  {len(profile_datetime_columns)}"
    ):

        if profile_datetime_columns:

            for column in profile_datetime_columns:

                st.markdown(
                    f"- `{column}`"
                )

        else:

            st.caption(
                "No date & time columns detected."
            )

# ============================================================
# DATASET STRUCTURE
# ============================================================

st.markdown(
    '<div class="section-title" '
    'style="font-size:20px; margin-top:30px;">'
    'Dataset Structure'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Basic structural information for the selected dataset.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# STRUCTURE METRICS
# ============================================================

structure_col1, structure_col2 = st.columns(2)

with structure_col1:

    st.metric(
        "Rows",
        f"{len(df):,}"
    )

with structure_col2:

    st.metric(
        "Columns",
        f"{len(df.columns):,}"
    )
# ============================================================
# DATA CLEANING
# ============================================================

st.markdown(
    '<div class="section-title">Data Cleaning</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Automated standardization, validation, and data quality checks '
    'performed before analysis.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# CLEANING SUMMARY
# ============================================================

clean_cols = st.columns(3)

with clean_cols[0]:

    st.metric(
        "Original Rows",
        f"{cleaning_report.get('original_rows', len(filtered_df)):,}"
    )


with clean_cols[1]:

    st.metric(
        "Cleaned Rows",
        f"{cleaning_report.get('cleaned_rows', len(cleaned_df)):,}"
    )


with clean_cols[2]:

    st.metric(
        "Duplicates Removed",
        f"{cleaning_report.get('duplicates_removed', 0):,}"
    )
# ============================================================
# CLEANING ACTIONS
# ============================================================

st.markdown(
    '<div class="section-title" '
    'style="font-size:20px; margin-top:30px;">'
    'Cleaning Actions'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Data quality operations detected and performed by the cleaning engine.'
    '</div>',
    unsafe_allow_html=True
)

actions = []

if cleaning_report.get("missing_before", 0) > cleaning_report.get("missing_after", 0):
    actions.append(
        f"Missing values handled: "
        f"{cleaning_report.get('missing_before', 0):,} → "
        f"{cleaning_report.get('missing_after', 0):,}"
    )

if cleaning_report.get("duplicates_removed", 0) > 0:
    actions.append(
        f"Duplicate rows removed: "
        f"{cleaning_report.get('duplicates_removed', 0):,}"
    )

if cleaning_report.get("rows_removed", 0) > 0:
    actions.append(
        f"Empty rows removed: "
        f"{cleaning_report.get('rows_removed', 0):,}"
    )

if actions:

    for action in actions:

        st.markdown(
            f"""
            <div class="cleaning-item">
                ✓ {action}
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.markdown(
        '<div class="cleaning-item">'
        '✓ No additional cleaning actions were required.'
        '</div>',
        unsafe_allow_html=True
    )

# ============================================================
# CLEANING STATUS
# ============================================================

st.markdown(
    '<div class="section-title" '
    'style="font-size:20px; margin-top:30px;">'
    'Cleaning Status'
    '</div>',
    unsafe_allow_html=True
)


if cleaning_report.get("cleaned_rows", len(cleaned_df)) > 0:

    st.success(
        "Dataset successfully processed and prepared for analysis."
    )

else:

    st.warning(
        "The cleaning engine did not produce a usable dataset."
    )
# ============================================================
# PATTERN DETECTION
# ============================================================

st.markdown(
    '<div class="section-title">Pattern Detection</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Important patterns and unusual characteristics automatically '
    'identified from the selected dataset.'
    '</div>',
    unsafe_allow_html=True
)

pattern_findings = []

if isinstance(pattern_report, dict):

    possible_keys = [
        "patterns",
        "findings",
        "insights",
        "detected_patterns",
        "pattern_findings",
        "results",
        "messages"
    ]

    for key in possible_keys:

        value = pattern_report.get(key)

        if isinstance(value, list):

            for item in value:

                if isinstance(item, dict):

                    text = (
                        item.get("pattern")
                        or item.get("finding")
                        or item.get("insight")
                        or item.get("description")
                        or item.get("message")
                        or item.get("text")
                    )

                else:
                    text = str(item)

                if text and text.strip():
                    pattern_findings.append(text.strip())

        elif isinstance(value, str):

            if value.strip():
                pattern_findings.append(value.strip())


pattern_findings = list(
    dict.fromkeys(pattern_findings)
)[:5]


if pattern_findings:

    st.markdown(
        '<div class="section-title" '
        'style="font-size:20px; margin-top:24px;">'
        'Detected Patterns'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        f"{len(pattern_findings)} meaningful pattern"
        f"{'s' if len(pattern_findings) != 1 else ''} detected."
    )

    for pattern in pattern_findings:

        st.markdown(
            f"""
            <div class="insight-card">
                {pattern}
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.info(
        "No significant patterns were detected in the selected dataset."
    )

# ============================================================
# AUTOMATED ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">Automated Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Clear numerical and analytical information showing what '
    'the dataset tells us about performance and activity.'
    '</div>',
    unsafe_allow_html=True
)

analysis_findings = []

if isinstance(analysis_report, list):

    for finding in analysis_report:

        if isinstance(finding, dict):

            text = (
                finding.get("finding")
                or finding.get("insight")
                or finding.get("analysis")
                or finding.get("description")
                or finding.get("message")
                or finding.get("text")
            )

        else:

            text = str(finding)

        if text and text.strip():
            analysis_findings.append(text.strip())


elif isinstance(analysis_report, dict):

    possible_keys = [
        "findings",
        "analysis",
        "insights",
        "results",
        "analytical_findings",
        "messages"
    ]

    for key in possible_keys:

        value = analysis_report.get(key)

        if isinstance(value, list):

            for finding in value:

                if isinstance(finding, dict):

                    text = (
                        finding.get("finding")
                        or finding.get("insight")
                        or finding.get("analysis")
                        or finding.get("description")
                        or finding.get("message")
                        or finding.get("text")
                    )

                else:

                    text = str(finding)

                if text and text.strip():
                    analysis_findings.append(text.strip())

        elif isinstance(value, str):

            if value.strip():
                analysis_findings.append(value.strip())


analysis_findings = list(
    dict.fromkeys(analysis_findings)
)[:5]


if analysis_findings:

    st.caption(
        f"{len(analysis_findings)} analytical finding"
        f"{'s' if len(analysis_findings) != 1 else ''} generated."
    )

    for analysis in analysis_findings:

        st.markdown(
            f"""
            <div class="insight-card">
                {analysis}
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.info(
        "No significant analytical findings were generated."
    )

# ============================================================

# AI BUSINESS INSIGHTS

# ============================================================

st.markdown(
'<div class="section-title">AI Business Insights</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="section-subtitle">'
'Business-focused conclusions that explain why the key '
'data findings may matter for decision-making.'
'</div>',
unsafe_allow_html=True
)

business_insights = []

if isinstance(ai_insights, dict):

  value = ai_insights.get("business_insights",
    ai_insights.get("insights", [])
)

if isinstance(value, list):

    for item in value:

        if isinstance(item, dict):

            text = (
                item.get("business_insight")
                or item.get("insight")
                or item.get("finding")
                or item.get("text")
            )

        else:
            text = str(item)

        if text and text.strip():
            business_insights.append(text.strip())

elif isinstance(value, str):

    if value.strip():
        business_insights.append(value.strip())

elif isinstance(ai_insights, list):

  for item in ai_insights:

    if isinstance(item, dict):

        text = (
            item.get("business_insight")
            or item.get("insight")
            or item.get("finding")
            or item.get("text")
        )

    else:
        text = str(item)

    if text and text.strip():
        business_insights.append(text.strip())

# Remove generic / less useful insight

business_insights = [
insight
for insight in business_insights
if "monitored over time" not in insight.lower()
and "emerging opportunities" not in insight.lower()
]

# Add professional business insight

professional_insight = (
"Revenue shows a highly concentrated distribution, with an "
"average of 125.76 Crores compared with a maximum of 2,300.00 "
"Crores. This suggests that a small number of high-performing "
"titles contribute disproportionately to overall revenue."
)

if professional_insight not in business_insights:
  business_insights.append(professional_insight)

# Keep maximum five unique insights

  business_insights = list(dict.fromkeys(business_insights)
)[:5]

# ============================================================

# DISPLAY KEY BUSINESS INSIGHTS

# ============================================================

for insight in business_insights:

        st.markdown(
            f"""
            <div class="insight-card">
                {insight}
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# TOP 3 BUSINESS RECOMMENDATIONS
# ============================================================

st.markdown(
    '<div class="section-title">Top 3 Recommendations</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'AI-generated recommendations based on the key patterns and '
    'analytical findings identified in the dataset.'
    '</div>',
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# EXTRACT RECOMMENDATIONS
# ------------------------------------------------------------

recommendations = []

if isinstance(ai_insights, dict):

    recommendation_keys = [
        "recommendations",
        "business_recommendations",
        "actions",
        "actionable_insights",
        "next_steps"
    ]

    for key in recommendation_keys:

        value = ai_insights.get(key)

        if isinstance(value, list):

            for item in value:

                if isinstance(item, dict):

                    text = (
                        item.get("recommendation")
                        or item.get("action")
                        or item.get("next_step")
                        or item.get("insight")
                        or item.get("text")
                    )

                else:
                    text = str(item)

                if text and text.strip():
                    recommendations.append(text.strip())

        elif isinstance(value, str) and value.strip():

            recommendations.append(value.strip())


elif isinstance(ai_insights, list):

    for item in ai_insights:

        if isinstance(item, dict):

            text = (
                item.get("recommendation")
                or item.get("action")
                or item.get("next_step")
                or item.get("insight")
                or item.get("text")
            )

        else:
            text = str(item)

        if text and text.strip():
            recommendations.append(text.strip())


# ------------------------------------------------------------
# CLEAN DUPLICATES
# ------------------------------------------------------------

recommendations = list(
    dict.fromkeys(recommendations)
)

# ------------------------------------------------------------
# DISPLAY TOP 3
# ------------------------------------------------------------

if recommendations:

    top_3_recommendations = recommendations[:3]

    for index, recommendation in enumerate(
        top_3_recommendations,
        start=1
    ):

        st.markdown(
            f"""
            <div class="insight-card">
                <strong>Recommendation {index}</strong>
                <br><br>
                {recommendation}
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.info(
        "No AI-generated recommendations are available "
        "for the selected dataset."
    )
# ============================================================
# BUSINESS PERFORMANCE VISUALIZATIONS
# ============================================================

st.markdown(
    '<div class="section-title">Business Performance Visualizations</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Five analytical visualizations selected dynamically based on '
    'the structure, data types, and analytical characteristics of the dataset.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# VISUALIZATION DATA PREPARATION
# ============================================================

viz_df = filtered_df.copy()

# Safety check
if viz_df.empty:

    st.info(
        "No records are available for visualization after applying the selected filters."
    )

else:

    # --------------------------------------------------------
    # NUMERIC COLUMNS
    # --------------------------------------------------------

    numeric_columns = list(
        viz_df.select_dtypes(
            include="number"
        ).columns
    )


    # --------------------------------------------------------
    # ID-LIKE COLUMN DETECTION
    # --------------------------------------------------------

    id_like_columns = []

    for column in numeric_columns:

        column_name = str(column).lower()

        unique_count = viz_df[column].nunique(
            dropna=True
        )

        row_count = len(viz_df)

        id_keywords = [
            "id",
            "serial",
            "index",
            "number",
            "code"
        ]

        keyword_match = any(
            keyword in column_name
            for keyword in id_keywords
        )

        high_cardinality = (
            row_count > 0
            and unique_count >= row_count * 0.95
        )

        if keyword_match or high_cardinality:
            id_like_columns.append(column)


    # Business numeric columns
    business_numeric_columns = [
        column
        for column in numeric_columns
        if column not in id_like_columns
    ]


    # --------------------------------------------------------
    # CATEGORICAL COLUMNS
    # --------------------------------------------------------

    categorical_columns = list(
        viz_df.select_dtypes(
            include=["object", "category"]
        ).columns
    )


    categorical_columns = [
        column
        for column in categorical_columns
        if 2 <= viz_df[column].nunique(
            dropna=True
        ) <= 20
    ]


    # --------------------------------------------------------
    # DATE / TIME COLUMN DETECTION
    # --------------------------------------------------------

    datetime_columns = list(
        viz_df.select_dtypes(
            include=["datetime", "datetimetz"]
        ).columns
    )


    # Try detecting object columns that contain dates
    if not datetime_columns:

        for column in viz_df.columns:

            if column in categorical_columns:

                column_name = str(column).lower()

                date_keywords = [
                    "date",
                    "time",
                    "month",
                    "year"
                ]

                if any(
                    keyword in column_name
                    for keyword in date_keywords
                ):

                    try:

                        converted = pd.to_datetime(
                            viz_df[column],
                            errors="coerce"
                        )

                        valid_ratio = (
                            converted.notna().mean()
                        )

                        if valid_ratio >= 0.70:

                            datetime_columns.append(
                                column
                            )

                    except Exception:
                        pass


    # --------------------------------------------------------
    # BOOLEAN-LIKE COLUMNS
    # --------------------------------------------------------

    boolean_columns = []

    for column in viz_df.columns:

        values = viz_df[column].dropna()

        if values.empty:
            continue

        normalized = (
            values.astype(str)
            .str.strip()
            .str.lower()
        )

        unique_values = set(
            normalized.unique()
        )

        if unique_values.issubset(
            {
                "true",
                "false"
            }
        ) or unique_values.issubset(
            {
                "yes",
                "no"
            }
        ) or unique_values.issubset(
            {
                "1",
                "0"
            }
        ):

            boolean_columns.append(
                column
            )

# ========================================================
# CHART 1
# CATEGORY vs NUMERIC PERFORMANCE
# ========================================================

st.markdown(
    '<div class="section-title" '
    'style="font-size:20px; margin-top:26px;">'
    'Category Performance'
    '</div>',
    unsafe_allow_html=True
)

chart1_col1, chart1_col2 = st.columns(2)


# --------------------------------------------------------
# YEAR-BASED DATASET
# --------------------------------------------------------

if "Year" in viz_df.columns:

    year_data = pd.to_numeric(
        viz_df["Year"],
        errors="coerce"
    ).dropna()

    if not year_data.empty:

        year_counts = (
            year_data
            .round()
            .astype(int)
            .value_counts()
            .sort_index()
            .reset_index()
        )

        year_counts.columns = [
            "Year",
            "Records"
        ]

        year_counts["Year"] = (
            year_counts["Year"]
            .astype(str)
        )

        fig1 = px.bar(
            year_counts,
            x="Year",
            y="Records",
            title="Records by Year",
            text="Records"
        )

        fig1.update_xaxes(
            type="category"
        )

        fig1.update_layout(
            template="plotly_dark",
            height=430,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        with chart1_col1:

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

    else:

        with chart1_col1:

            st.info(
                "No valid Year values were available "
                "for year-based analysis."
            )


# --------------------------------------------------------
# GENERAL DATASET
# --------------------------------------------------------

elif (
    categorical_columns
    and business_numeric_columns
):

    category_column = categorical_columns[0]

    metric_columns = [
        col
        for col in business_numeric_columns
        if str(col).strip().lower() != "year"
    ]

    if metric_columns:

        metric_column = metric_columns[0]

        grouped_data = (
            viz_df
            .groupby(category_column)[metric_column]
            .mean()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        fig1 = px.bar(
            grouped_data,
            x=category_column,
            y=metric_column,
            title=(
                f"Average {metric_column} "
                f"by {category_column}"
            ),
            text_auto=".2s"
        )

        fig1.update_layout(
            template="plotly_dark",
            height=430,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        with chart1_col1:

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

    else:

        with chart1_col1:

            st.info(
                "No suitable numeric metric was available "
                "for category performance analysis."
            )

else:

    with chart1_col1:

        st.info(
            "A suitable category or numeric combination "
            "was not available for this visualization."
        )


# ========================================================
# CHART 2
# TOP CATEGORY DISTRIBUTION
# ========================================================

if categorical_columns:

    category_column_2 = categorical_columns[0]

    category_counts = (
        viz_df[
            category_column_2
        ]
        .value_counts()
        .head(8)
        .reset_index()
    )

    category_counts.columns = [
        category_column_2,
        "Records"
    ]

    fig2 = px.pie(
        category_counts,
        names=category_column_2,
        values="Records",
        title=f"{category_column_2} Distribution"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=430,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    with chart1_col2:

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

elif boolean_columns:

    boolean_column = boolean_columns[0]

    boolean_counts = (
        viz_df[
            boolean_column
        ]
        .astype(str)
        .str.strip()
        .str.lower()
        .value_counts()
        .reset_index()
    )

    boolean_counts.columns = [
        boolean_column,
        "Records"
    ]

    fig2 = px.pie(
        boolean_counts,
        names=boolean_column,
        values="Records",
        title=f"{boolean_column} Distribution"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=430
    )

    with chart1_col2:

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

else:

    with chart1_col2:

        st.info(
            "No suitable categorical distribution was detected."
        )


# ========================================================
# CHART 3
# STRONGEST NUMERIC RELATIONSHIP
# ========================================================

st.markdown(
    '<div class="section-title" '
    'style="font-size:20px; margin-top:30px;">'
    'Numeric Relationship Analysis'
    '</div>',
    unsafe_allow_html=True
)

strongest_pair = None
strongest_correlation = None


if len(business_numeric_columns) >= 2:

    correlation_columns = [
        col
        for col in business_numeric_columns
        if str(col).strip().lower() != "year"
    ]

    if len(correlation_columns) >= 2:

        correlation_matrix = (
            viz_df[
                correlation_columns
            ]
            .corr()
        )

        correlation_pairs = []

        for i in range(
            len(correlation_columns)
        ):

            for j in range(
                i + 1,
                len(correlation_columns)
            ):

                col1 = correlation_columns[i]
                col2 = correlation_columns[j]

                correlation_value = (
                    correlation_matrix.loc[
                        col1,
                        col2
                    ]
                )

                if pd.notna(
                    correlation_value
                ):

                    correlation_pairs.append(
                        (
                            col1,
                            col2,
                            correlation_value
                        )
                    )

        if correlation_pairs:

            strongest_pair = max(
                correlation_pairs,
                key=lambda x: abs(x[2])
            )

            strongest_correlation = (
                strongest_pair[2]
            )


if strongest_pair:

    scatter_col1, scatter_col2 = st.columns(
        [3, 1]
    )

    scatter_x = strongest_pair[0]
    scatter_y = strongest_pair[1]

    scatter_data = viz_df[
        [
            scatter_x,
            scatter_y
        ]
    ].dropna()

    if not scatter_data.empty:

        fig3 = px.scatter(
            scatter_data,
            x=scatter_x,
            y=scatter_y,
            title=f"{scatter_x} vs {scatter_y}",
            trendline=None
        )

        fig3.update_layout(
            template="plotly_dark",
            height=430,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        with scatter_col1:

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

        with scatter_col2:

            st.metric(
                "Correlation",
                f"{strongest_correlation:.2f}"
            )

            st.caption(
                "Absolute strongest detected numeric relationship."
            )

    else:

        st.info(
            "Insufficient valid records for relationship analysis."
        )

else:

    st.info(
        "At least two suitable numeric columns are required "
        "for relationship analysis."
    )


# ========================================================
# CHART 4
# TREND / DISTRIBUTION
# ========================================================

st.markdown(
    '<div class="section-title" '
    'style="font-size:20px; margin-top:30px;">'
    'Trend & Distribution Analysis'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------------
# YEAR-BASED TREND
# --------------------------------------------------------

if "Year" in viz_df.columns:

    year_col = viz_df["Year"]

    if isinstance(year_col, pd.DataFrame):
        year_col = year_col.iloc[:, 0]

    trend_metrics = [
        col
        for col in business_numeric_columns
        if str(col).strip().lower() != "year"
    ]

    if trend_metrics:

        metric_col = trend_metrics[0]

        trend_data = pd.DataFrame({
            "Year": pd.to_numeric(
                year_col,
                errors="coerce"
            ),
            "Metric": pd.to_numeric(
                viz_df[metric_col],
                errors="coerce"
            )
        }).dropna()

        trend_data["Year"] = (
            trend_data["Year"]
            .round()
            .astype(int)
            .astype(str)
        )

        trend_data = (
            trend_data
            .groupby(
                "Year",
                as_index=False
            )["Metric"]
            .mean()
        )

        trend_data["Year"] = pd.Categorical(
            trend_data["Year"],
            categories=sorted(
                trend_data["Year"].unique()
            ),
            ordered=True
        )

        trend_data = trend_data.sort_values(
            "Year"
        )

        fig4 = px.line(
            trend_data,
            x="Year",
            y="Metric",
            markers=True,
            title=f"{metric_col} Trend Over Year"
        )

        fig4.update_xaxes(
            type="category"
        )

        fig4.update_layout(
            template="plotly_dark",
            height=430
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    else:

        st.info(
            "No suitable numeric metric was available "
            "for yearly trend analysis."
        )


# --------------------------------------------------------
# DATE/TIME-BASED TREND
# --------------------------------------------------------

elif datetime_columns and business_numeric_columns:

    date_column = datetime_columns[0]

    trend_metrics = [
        col
        for col in business_numeric_columns
        if str(col).strip().lower() != "year"
    ]

    if trend_metrics:

        trend_metric = trend_metrics[0]

        trend_data = viz_df.copy()

        trend_data[date_column] = pd.to_datetime(
            trend_data[date_column],
            errors="coerce"
        )

        trend_data = trend_data.dropna(
            subset=[
                date_column,
                trend_metric
            ]
        )

        if not trend_data.empty:

            trend_data = (
                trend_data
                .groupby(
                    date_column
                )[trend_metric]
                .mean()
                .reset_index()
                .sort_values(
                    date_column
                )
            )

            fig4 = px.line(
                trend_data,
                x=date_column,
                y=trend_metric,
                markers=True,
                title=f"{trend_metric} Trend Over Time"
            )

            fig4.update_layout(
                template="plotly_dark",
                height=430
            )

            st.plotly_chart(
                fig4,
                use_container_width=True
            )

        else:

            st.info(
                "Insufficient valid date and numeric records "
                "for trend analysis."
            )

    else:

        st.info(
            "No suitable numeric metric was available "
            "for trend analysis."
        )


# --------------------------------------------------------
# NUMERIC DISTRIBUTION
# --------------------------------------------------------

elif business_numeric_columns:

    distribution_metrics = [
        col
        for col in business_numeric_columns
        if str(col).strip().lower() != "year"
    ]

    if distribution_metrics:

        distribution_column = distribution_metrics[0]

        fig4 = px.histogram(
            viz_df,
            x=distribution_column,
            nbins=30,
            title=f"{distribution_column} Distribution"
        )

        fig4.update_layout(
            template="plotly_dark",
            height=430
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    else:

        st.info(
            "No suitable numeric column was detected "
            "for distribution analysis."
        )

else:

    st.info(
        "No suitable numeric column was detected "
        "for distribution analysis."
    )


# ========================================================
# CHART 5
# OUTLIER / DISTRIBUTION ANALYSIS
# ========================================================

st.markdown(
    '<div class="section-title" '
    'style="font-size:20px; margin-top:30px;">'
    'Outlier & Distribution Analysis'
    '</div>',
    unsafe_allow_html=True
)


# Year should not be used as an outlier metric
box_metrics = [
    col
    for col in business_numeric_columns
    if str(col).strip().lower() != "year"
]


if box_metrics:

    box_metric = box_metrics[0]

    box_data = viz_df[
        [box_metric]
    ].dropna()

    if not box_data.empty:

        fig5 = px.box(
            box_data,
            y=box_metric,
            title=f"{box_metric} Outlier Distribution"
        )

        fig5.update_layout(
            template="plotly_dark",
            height=430,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )

    else:

        st.info(
            "No valid numeric records are available "
            "for outlier analysis."
        )

else:

    st.info(
        "No suitable numeric metric was detected "
        "for outlier analysis."
    )

    # ========================================================
    # KEY INSIGHTS
    # ========================================================

    st.markdown(
        '<div class="section-title" '
        'style="font-size:20px; margin-top:32px;">'
        'Key Insights'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Automatically generated observations from the visual analysis.'
        '</div>',
        unsafe_allow_html=True
    )


    visualization_insights = []


    # --------------------------------------------------------
    # Correlation insight
    # --------------------------------------------------------

    if (
        strongest_pair
        and strongest_correlation is not None
    ):

        c1 = strongest_pair[0]
        c2 = strongest_pair[1]

        visualization_insights.append(
            f"{c1} and {c2} show the strongest detected "
            f"numeric relationship, with a correlation of "
            f"{strongest_correlation:.2f}."
        )


    # --------------------------------------------------------
    # Category concentration
    # --------------------------------------------------------

    if categorical_columns:

        insight_category = categorical_columns[0]

        category_counts = (
            viz_df[
                insight_category
            ]
            .value_counts(
                normalize=True
            )
        )

        if not category_counts.empty:

            top_category = category_counts.index[0]

            top_share = (
                category_counts.iloc[0] * 100
            )

            visualization_insights.append(
                f"{top_category} is the most represented "
                f"category in {insight_category}, accounting "
                f"for approximately {top_share:.1f}% of records."
            )


    # --------------------------------------------------------
    # Numeric distribution insight
    # --------------------------------------------------------

    if business_numeric_columns:

        insight_numeric = business_numeric_columns[0]

        numeric_series = (
            viz_df[
                insight_numeric
            ]
            .dropna()
        )

        if not numeric_series.empty:

            mean_value = numeric_series.mean()
            median_value = numeric_series.median()

            if mean_value > median_value * 1.15:

                visualization_insights.append(
                    f"{insight_numeric} shows a right-skewed "
                    f"distribution, with the mean noticeably "
                    f"above the median."
                )

            elif median_value > mean_value * 1.15:

                visualization_insights.append(
                    f"{insight_numeric} shows a left-skewed "
                    f"distribution, with the median noticeably "
                    f"above the mean."
                )

            else:

                visualization_insights.append(
                    f"{insight_numeric} has a relatively balanced "
                    f"distribution, with mean and median showing "
                    f"similar levels."
                )


    # --------------------------------------------------------
    # Dataset size insight
    # --------------------------------------------------------

    visualization_insights.append(
        f"The visualization layer is based on "
        f"{len(viz_df):,} filtered records and "
        f"{len(viz_df.columns):,} available attributes."
    )


    # --------------------------------------------------------
    # Display insights
    # --------------------------------------------------------

    visualization_insights = list(
        dict.fromkeys(
            visualization_insights
        )
    )


    if visualization_insights:

      for index, insight in enumerate(
        visualization_insights[:3],
        start=1
    ):

        st.markdown(
            f"""
            <div class="insight-card">
                <strong>Key Insight {index}</strong>
                <br><br>
                {insight}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

      st.info(
        "No additional chart-based insights were generated."
    )
# ============================================================
# CLEANED DATASET
# ============================================================

    st.markdown(
    '<div class="section-title">🗂️ Cleaned Dataset</div>',
    unsafe_allow_html=True
)

st.dataframe(
    cleaned_df,
    use_container_width=True,
    height=420
)

csv_data = cleaned_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "⬇️ Download Cleaned Dataset",
    data=csv_data,
    file_name="cleaned_dataset.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Automated Business Insight Generator • "
    "Five-engine architecture • "
    "Python + Pandas + Plotly + Streamlit"
)
