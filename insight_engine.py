
import pandas as pd
import numpy as np


# ============================================================
# ENGINE 1 — DATA PROFILING ENGINE
# ============================================================

def data_profiling_engine(df):

    # --------------------------------------------------------
    # NUMERIC COLUMNS
    # --------------------------------------------------------

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    # --------------------------------------------------------
    # DATE / TIME COLUMNS
    # --------------------------------------------------------

    datetime_columns = []

    for col in df.columns:

        # Already datetime dtype
        if pd.api.types.is_datetime64_any_dtype(df[col]):

            datetime_columns.append(col)
            continue

        # Object / string columns
        if df[col].dtype == "object":

            values = df[col].astype(str).str.strip()

            # Time-only format: HH:MM:SS
            time_converted = pd.to_datetime(
                values,
                format="%H:%M:%S",
                errors="coerce"
            )

            if time_converted.notna().mean() >= 0.80:

                datetime_columns.append(col)
                continue

            # Date / datetime format
            date_converted = pd.to_datetime(
                values,
                errors="coerce",
                format="mixed"
            )

            if date_converted.notna().mean() >= 0.80:

                datetime_columns.append(col)

    # --------------------------------------------------------
    # CATEGORICAL COLUMNS
    # --------------------------------------------------------

    categorical_columns = [
        col
        for col in df.select_dtypes(
            exclude=np.number
        ).columns.tolist()
        if col not in datetime_columns
    ]

    # --------------------------------------------------------
    # PROFILING REPORT
    # --------------------------------------------------------

    profiling_report = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "datetime_columns": datetime_columns,
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_types": {
            col: str(dtype)
            for col, dtype in df.dtypes.items()
        }
    }

    return profiling_report
    
# ============================================================
# ENGINE 2 — DATA CLEANING ENGINE
# ============================================================

def data_cleaning_engine(df):

    cleaned_df = df.copy()

    before_rows = len(cleaned_df)
    missing_before = int(
        cleaned_df.isnull().sum().sum()
    )

    # Remove completely empty rows
    cleaned_df = cleaned_df.dropna(
        how="all"
    )

    # Remove duplicate rows
    cleaned_df = cleaned_df.drop_duplicates()

    # Clean string columns
    for col in cleaned_df.select_dtypes(
        include="object"
    ).columns:

        cleaned_df[col] = (
            cleaned_df[col]
            .astype(str)
            .str.strip()
            .replace("nan", np.nan)
        )

    # Fill numeric missing values with median
    for col in cleaned_df.select_dtypes(
        include=np.number
    ).columns:

        if cleaned_df[col].isnull().any():

            median_value = cleaned_df[col].median()

            if pd.notna(median_value):
                cleaned_df[col] = cleaned_df[col].fillna(
                    median_value
                )

    # Fill categorical missing values
    for col in cleaned_df.select_dtypes(
        include="object"
    ).columns:

        if cleaned_df[col].isnull().any():

            cleaned_df[col] = cleaned_df[col].fillna(
                "Unknown"
            )

    missing_after = int(
        cleaned_df.isnull().sum().sum()
    )

    cleaning_report = {
        "rows_before": before_rows,
        "rows_after": len(cleaned_df),
        "rows_removed": before_rows - len(cleaned_df),
        "missing_before": missing_before,
        "missing_after": missing_after,
        "duplicates_removed": int(
            df.duplicated().sum()
        )
    }

    return cleaned_df, cleaning_report


# ============================================================
# ENGINE 3 — PATTERN DETECTION ENGINE
# ============================================================

def pattern_detection_engine(df):

    pattern_report = {
        "numeric_patterns": [],
        "categorical_patterns": [],
        "correlations": [],
        "patterns": []
    }

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    categorical_cols = df.select_dtypes(
        exclude=np.number
    ).columns.tolist()

    # --------------------------------------------------------
    # REMOVE ID-LIKE NUMERIC COLUMNS
    # --------------------------------------------------------

    useful_numeric_cols = []

    for col in numeric_cols:

        col_lower = str(col).lower()

        if any(word in col_lower for word in [
            "id", "serial", "index", "code"
        ]):
            continue

        if df[col].nunique(dropna=True) >= max(
            10,
            int(len(df) * 0.95)
        ):
            continue

        useful_numeric_cols.append(col)

    # --------------------------------------------------------
    # NUMERIC PATTERNS
    # --------------------------------------------------------

    for col in useful_numeric_cols:

        series = df[col].dropna()

        if len(series) == 0:
            continue

        mean_value = float(series.mean())
        median_value = float(series.median())
        min_value = float(series.min())
        max_value = float(series.max())

        pattern_report["numeric_patterns"].append({
            "column": col,
            "mean": mean_value,
            "median": median_value,
            "minimum": min_value,
            "maximum": max_value
        })

        # Strong difference between average and middle value
        if median_value != 0:

            difference = (
                abs(mean_value - median_value)
                / abs(median_value)
            )

            if difference >= 0.50:

                pattern_report["patterns"].append(
                    f"{col} is unevenly distributed. "
                    f"The average is {mean_value:.2f}, "
                    f"while the middle value is {median_value:.2f}. "
                    f"This means a smaller number of records have "
                    f"much higher values than most records."
                )

    # --------------------------------------------------------
    # CATEGORICAL PATTERNS
    # --------------------------------------------------------

    for col in categorical_cols:

        # Skip long text / unique-name columns
        unique_count = df[col].nunique(dropna=True)

        if unique_count == 0:
            continue

        if unique_count > 30:
            continue

        counts = (
            df[col]
            .value_counts(dropna=True)
        )

        if len(counts) == 0:
            continue

        pattern_report["categorical_patterns"].append({
            "column": col,
            "top_values": counts.head(5).to_dict()
        })

        top_value = counts.index[0]
        top_count = int(counts.iloc[0])
        total_count = int(counts.sum())

        share = (
            top_count / total_count
            if total_count > 0
            else 0
        )

        if share >= 0.50:

            pattern_report["patterns"].append(
                f"{col} is strongly concentrated around "
                f"'{top_value}', which appears in "
                f"{share * 100:.1f}% of the records "
                f"({top_count} out of {total_count})."
            )

        elif share >= 0.20:

            pattern_report["patterns"].append(
                f"'{top_value}' is the most common value in "
                f"{col}, representing {share * 100:.1f}% "
                f"of the records."
            )

    # --------------------------------------------------------
    # CORRELATIONS
    # --------------------------------------------------------

    if len(useful_numeric_cols) >= 2:

        corr = df[useful_numeric_cols].corr()

        correlation_candidates = []

        for i in range(len(useful_numeric_cols)):

            for j in range(i + 1, len(useful_numeric_cols)):

                value = corr.iloc[i, j]

                if pd.notna(value):

                    correlation_value = float(value)

                    pattern_report["correlations"].append({
                        "column_1": useful_numeric_cols[i],
                        "column_2": useful_numeric_cols[j],
                        "correlation": correlation_value
                    })

                    correlation_candidates.append({
                        "column_1": useful_numeric_cols[i],
                        "column_2": useful_numeric_cols[j],
                        "correlation": correlation_value
                    })

        # Use strongest relationship only
        if correlation_candidates:

            strongest = max(
                correlation_candidates,
                key=lambda x: abs(x["correlation"])
            )

            value = strongest["correlation"]

            if abs(value) >= 0.50:

                direction = (
                    "move together"
                    if value > 0
                    else "tend to move in opposite directions"
                )

                pattern_report["patterns"].append(
                    f"{strongest['column_1']} and "
                    f"{strongest['column_2']} {direction}. "
                    f"The relationship value is {value:.2f}."
                )

    # --------------------------------------------------------
    # KEEP ONLY 5 USEFUL PATTERNS
    # --------------------------------------------------------

    pattern_report["patterns"] = list(
        dict.fromkeys(pattern_report["patterns"])
    )[:5]

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    if not pattern_report["patterns"]:

        pattern_report["patterns"].append(
            "The selected data does not show any strong "
            "repeated patterns using the available information."
        )

    return pattern_report


# ============================================================
# ENGINE 4 — AUTOMATED ANALYSIS ENGINE
# ============================================================

def automated_analysis_engine(df):

    analysis_report = []

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    categorical_cols = df.select_dtypes(
        exclude=np.number
    ).columns.tolist()

    # --------------------------------------------------------
    # REMOVE ID-LIKE NUMERIC COLUMNS
    # --------------------------------------------------------

    useful_numeric_cols = []

    for col in numeric_cols:

        col_lower = str(col).lower()

        if any(word in col_lower for word in [
            "id", "serial", "index", "code"
        ]):
            continue

        if df[col].nunique(dropna=True) >= max(
            10,
            int(len(df) * 0.95)
        ):
            continue

        useful_numeric_cols.append(col)

    # --------------------------------------------------------
    # NUMERIC BUSINESS ANALYSIS
    # --------------------------------------------------------

    for col in useful_numeric_cols:

        series = df[col].dropna()

        if len(series) == 0:
            continue

        mean_value = float(series.mean())
        median_value = float(series.median())
        min_value = float(series.min())
        max_value = float(series.max())

        analysis_report.append({
            "type": "numeric",
            "metric": col,
            "insight": (
                f"{col} has an average value of "
                f"{mean_value:.2f}. "
                f"Most records are around {median_value:.2f}, "
                f"while the values range from "
                f"{min_value:.2f} to {max_value:.2f}."
            )
        })

    # --------------------------------------------------------
    # CATEGORICAL BUSINESS ANALYSIS
    # --------------------------------------------------------

    for col in categorical_cols:

        unique_count = df[col].nunique(dropna=True)

        if unique_count == 0 or unique_count > 30:
            continue

        counts = df[col].value_counts(
            dropna=True
        )

        if len(counts) == 0:
            continue

        top_category = counts.index[0]
        top_count = int(counts.iloc[0])
        total_count = int(counts.sum())

        share = (
            top_count / total_count * 100
            if total_count > 0
            else 0
        )

        analysis_report.append({
            "type": "categorical",
            "metric": col,
            "insight": (
                f"{top_category} is the most common "
                f"{col.lower()} with {top_count} records, "
                f"representing {share:.1f}% of the available data."
            )
        })

    # --------------------------------------------------------
    # DATE / MONTH ANALYSIS
    # --------------------------------------------------------

    date_columns = []

    for col in df.columns:

        if pd.api.types.is_datetime64_any_dtype(df[col]):

            date_columns.append(col)

        elif df[col].dtype == "object":

            converted = pd.to_datetime(
                df[col],
                errors="coerce"
            )

            if converted.notna().mean() >= 0.80:

                date_columns.append(col)

    if date_columns and useful_numeric_cols:

        date_col = date_columns[0]

        dates = pd.to_datetime(
            df[date_col],
            errors="coerce"
        )

        temp = df.copy()
        temp["_analysis_date_"] = dates

        temp = temp.dropna(
            subset=["_analysis_date_"]
        )

        if len(temp) > 0:

            value_col = useful_numeric_cols[0]

            monthly = (
                temp.groupby(
                    temp["_analysis_date_"].dt.to_period("M")
                )[value_col]
                .mean()
            )

            if len(monthly) > 0:

                highest_month = monthly.idxmax()
                highest_value = float(monthly.max())

                analysis_report.append({
                    "type": "time",
                    "metric": value_col,
                    "insight": (
                        f"The highest average {value_col.lower()} "
                        f"was recorded in {highest_month.strftime('%B %Y')}, "
                        f"at {highest_value:.2f}."
                    )
                })

    # --------------------------------------------------------
    # KEEP ONLY 5 ANALYSES
    # --------------------------------------------------------

    analysis_report = analysis_report[:5]

    return analysis_report


# ============================================================
# ENGINE 5 — AI INSIGHT ENGINE
# ============================================================

def run_ai_insight_engine(
    df,
    profiling_report,
    pattern_report,
    analysis_report
):

    business_insights = []

    # --------------------------------------------------------
    # FIND USEFUL NUMERIC COLUMNS
    # --------------------------------------------------------

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    useful_numeric_cols = []

    for col in numeric_cols:

        col_lower = str(col).lower()

        if any(word in col_lower for word in [
            "id", "serial", "index", "code"
        ]):
            continue

        if df[col].nunique(dropna=True) >= max(
            10,
            int(len(df) * 0.95)
        ):
            continue

        useful_numeric_cols.append(col)

    # --------------------------------------------------------
    # BUSINESS INSIGHT 1 — DATA QUALITY
    # --------------------------------------------------------

    missing_values = profiling_report.get(
        "missing_values",
        0
    )

    duplicate_rows = profiling_report.get(
        "duplicate_rows",
        0
    )

    if missing_values > 0:

        business_insights.append(
            f"Data quality needs attention because "
            f"{missing_values} missing values were identified. "
            f"Cleaning these fields can make future reporting "
            f"more reliable."
        )

    elif duplicate_rows > 0:

        business_insights.append(
            f"The dataset contained {duplicate_rows} duplicate "
            f"records. Removing repeated records helps keep "
            f"business results accurate."
        )

    else:

        business_insights.append(
            "The dataset has a clean starting point with no "
            "missing values or duplicate records requiring "
            "attention."
        )

    # --------------------------------------------------------
    # BUSINESS INSIGHT 2 — REVENUE / SALES / VALUE
    # --------------------------------------------------------

    value_column = None

    for col in useful_numeric_cols:

        col_lower = str(col).lower()

        if any(word in col_lower for word in [
            "revenue",
            "sales",
            "amount",
            "income",
            "profit",
            "price",
            "value"
        ]):

            value_column = col
            break

    if value_column:

        series = df[value_column].dropna()

        if len(series) > 0:

            total_value = float(series.sum())
            average_value = float(series.mean())
            maximum_value = float(series.max())

            business_insights.append(
                f"{value_column} generated a total of "
                f"{total_value:,.2f} across the available records. "
                f"The average was {average_value:,.2f}, while the "
                f"highest individual value reached "
                f"{maximum_value:,.2f}."
            )

    # --------------------------------------------------------
    # BUSINESS INSIGHT 3 — TOP CATEGORY
    # --------------------------------------------------------

    categorical_cols = df.select_dtypes(
        exclude=np.number
    ).columns.tolist()

    top_category_found = False

    for col in categorical_cols:

        unique_count = df[col].nunique(dropna=True)

        if unique_count == 0 or unique_count > 20:
            continue

        counts = df[col].value_counts(
            dropna=True
        )

        if len(counts) == 0:
            continue

        top_value = counts.index[0]
        top_count = int(counts.iloc[0])
        total_count = int(counts.sum())

        share = (
            top_count / total_count * 100
            if total_count > 0
            else 0
        )

        business_insights.append(
            f"{top_value} is the leading category in "
            f"{col.lower()}, accounting for {share:.1f}% "
            f"of the records ({top_count} records). "
            f"This shows where the largest concentration "
            f"of activity exists."
        )

        top_category_found = True
        break

    # --------------------------------------------------------
    # BUSINESS INSIGHT 4 — STRONGEST NUMERIC RELATIONSHIP
    # --------------------------------------------------------

    correlations = pattern_report.get(
        "correlations",
        []
    )

    if correlations:

        strongest = max(
            correlations,
            key=lambda x: abs(
                x.get("correlation", 0)
            )
        )

        correlation_value = float(
            strongest.get("correlation", 0)
        )

        if abs(correlation_value) >= 0.50:

            if correlation_value > 0:

                relationship_text = (
                    "tend to increase together"
                )

            else:

                relationship_text = (
                    "tend to move in opposite directions"
                )

            business_insights.append(
                f"{strongest['column_1']} and "
                f"{strongest['column_2']} {relationship_text}. "
                f"The relationship value is "
                f"{correlation_value:.2f}. "
                f"This relationship may be useful when "
                f"planning business decisions."
            )

    # --------------------------------------------------------
    # BUSINESS INSIGHT 5 — OVERALL BUSINESS SIGNAL
    # --------------------------------------------------------

    if useful_numeric_cols:

        best_col = useful_numeric_cols[0]

        series = df[best_col].dropna()

        if len(series) > 0:

            mean_value = float(series.mean())
            median_value = float(series.median())
            maximum_value = float(series.max())

            if median_value != 0:

                difference = (
                    abs(mean_value - median_value)
                    / abs(median_value)
                )

            else:

                difference = 0

            if difference >= 0.50:

                business_insights.append(
                    f"{best_col} shows a wide difference between "
                    f"the average ({mean_value:.2f}) and the middle "
                    f"value ({median_value:.2f}). This suggests that "
                    f"a smaller number of high-value records are "
                    f"having a noticeable effect on the overall result."
                )

            else:

                business_insights.append(
                    f"{best_col} is relatively consistent across "
                    f"the dataset, with an average of "
                    f"{mean_value:.2f} and a highest value of "
                    f"{maximum_value:.2f}. This gives a clearer "
                    f"picture of typical performance."
                )

    # --------------------------------------------------------
    # ENSURE EXACTLY 5 BUSINESS INSIGHTS
    # --------------------------------------------------------

    business_insights = list(
        dict.fromkeys(business_insights)
    )

    # Fill if fewer than 5
    while len(business_insights) < 5:

        business_insights.append(
            "The available data can be monitored over time "
            "to identify changes in business performance "
            "and emerging opportunities."
        )

    business_insights = business_insights[:5]

    # --------------------------------------------------------
    # EXECUTIVE SUMMARY
    # --------------------------------------------------------

    executive_summary = (
        f"The dataset contains {len(df):,} records. "
        f"The automated analysis identified key data patterns, "
        f"business metrics, category concentrations, and "
        f"relationships that can support better decision-making."
    )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    recommendations = []

    if missing_values > 0:

        recommendations.append(
            "Review missing fields regularly so important "
            "business information is not lost."
        )

    if duplicate_rows > 0:

        recommendations.append(
            "Continue checking for duplicate records before "
            "using the data for business reporting."
        )

    if correlations:

        recommendations.append(
            "Monitor the strongest relationships between key "
            "metrics to understand changes in performance."
        )

    recommendations.append(
        "Track the most important business metrics over time "
        "to identify new trends early."
    )

    recommendations.append(
        "Review highly concentrated categories to understand "
        "where most business activity is coming from."
    )

    recommendations = list(
        dict.fromkeys(recommendations)
    )[:3]

    return {
        "source": "Automated Insight Engine",
        "executive_summary": executive_summary,
        "business_insights": business_insights,
        "insights": business_insights,
        "recommendations": recommendations
    }
# ============================================================
# MASTER FIVE-ENGINE PIPELINE
# ============================================================

def run_insight_pipeline(df):

    # Engine 1
    profiling_report = data_profiling_engine(df)

    # Engine 2
    cleaned_df, cleaning_report = data_cleaning_engine(df)

    # Engine 3
    pattern_report = pattern_detection_engine(
        cleaned_df
    )

    # Engine 4
    analysis_report = automated_analysis_engine(
        cleaned_df
    )

    # Engine 5
    ai_insights = run_ai_insight_engine(
        cleaned_df,
        profiling_report,
        pattern_report,
        analysis_report
    )

    return {
        "profiling_report": profiling_report,
        "cleaned_df": cleaned_df,
        "cleaning_report": cleaning_report,
        "pattern_report": pattern_report,
        "analysis_report": analysis_report,
        "ai_insights": ai_insights
    }
