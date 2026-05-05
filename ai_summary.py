def generate_summary(report):
    score = report["data_quality_score"]
    missing = report["missing_values"]
    unique = report["unique_values"]

    summary = f"Dataset contains {report['num_rows']} rows and {report['num_columns']} columns.\n\n"

    # 🎯 Quality assessment
    if score >= 90:
        summary += "✅ Data quality is excellent.\n"
    elif score >= 70:
        summary += "⚠️ Data quality is moderate.\n"
    else:
        summary += "❌ Data quality is poor.\n"

    # 🔍 Missing value insights
    high_missing = [col for col, val in missing.items() if val > 0]

    if high_missing:
        summary += "\n⚠️ Columns with missing values:\n"
        for col in high_missing:
            summary += f"- {col}\n"

    # 📊 Column insights
    summary += "\n📊 Column insights:\n"
    for col, val in unique.items():
        if val == report["num_rows"]:
            summary += f"- {col} looks like an identifier (unique values).\n"
        elif val < 5:
            summary += f"- {col} may be categorical.\n"

    # 🧠 ML readiness
    summary += "\n🧠 ML Readiness:\n"
    if score >= 80:
        summary += "Dataset is suitable for machine learning.\n"
    else:
        summary += "Dataset needs preprocessing before ML.\n"

    # 🚀 Suggestions
    summary += "\n🚀 Suggested Actions:\n"
    summary += "- Handle missing values\n"
    summary += "- Normalize numeric columns\n"
    summary += "- Encode categorical variables\n"

    return summary