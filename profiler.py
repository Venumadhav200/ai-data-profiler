import pandas as pd
from utils import is_valid_email

# 🔹 Data Quality Detection
def detect_data_quality(df):
    issues = {}

    issues["duplicate_rows"] = int(df.duplicated().sum())

    column_issues = {}

    for col in df.columns:
        col_issues = {}

        col_issues["missing_percent"] = float((df[col].isnull().sum() / len(df)) * 100)

        if "email" in col.lower():
            invalid_emails = df[col].dropna().apply(lambda x: not is_valid_email(x)).sum()
            col_issues["invalid_emails"] = int(invalid_emails)

        column_issues[col] = col_issues

    issues["column_issues"] = column_issues

    return issues


# 🔹 Outlier Detection
def detect_outliers(df):
    outliers = {}

    for col in df.select_dtypes(include=['int64', 'float64']).columns:
        mean = df[col].mean()
        std = df[col].std()

        outlier_count = ((df[col] - mean).abs() > 3 * std).sum()

        outliers[col] = int(outlier_count)

    return outliers


# 🔹 Data Quality Score
def calculate_quality_score(report):
    score = 100

    for col, val in report["missing_values"].items():
        if val > 0:
            score -= 5

    for col, issues in report["data_quality"]["column_issues"].items():
        if "invalid_emails" in issues:
            score -= issues["invalid_emails"] * 2

    return max(score, 0)


# 🔹 Main Function
def profile_data(file_path):
    df = pd.read_csv(file_path)

    report = {}

    report["columns"] = list(df.columns)
    report["num_rows"] = len(df)
    report["num_columns"] = len(df.columns)

    report["data_types"] = df.dtypes.astype(str).to_dict()
    report["missing_values"] = df.isnull().sum().to_dict()
    report["unique_values"] = df.nunique().to_dict()

    report["data_quality"] = detect_data_quality(df)

    # 🔥 NEW FEATURES
    report["outliers"] = detect_outliers(df)
    report["data_quality_score"] = calculate_quality_score(report)

    return report