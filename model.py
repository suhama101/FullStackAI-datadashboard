"""
OPTIONAL DEV TOOL SUPPORT - Used by the Streamlit app (app.py) for interactive analysis.

Main production ML: ml_model.py (called by server.js backend)

These functions are NOT used by the REST API or Next.js dashboard.
They are provided for exploratory data analysis via Streamlit only.

See ARCHITECTURE.md for details.
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def analyze_data(df):
	"""Return summary statistics, correlations, and text insights for a dataframe."""
	summary_stats = df.describe(include="all")

	numeric_df = df.select_dtypes(include="number")
	if numeric_df.shape[1] >= 2:
		correlations = numeric_df.corr()
	else:
		correlations = pd.DataFrame()

	if not numeric_df.empty:
		numeric_summary = pd.DataFrame(
			{
				"average": numeric_df.mean(),
				"max": numeric_df.max(),
				"min": numeric_df.min(),
			}
		)
	else:
		numeric_summary = pd.DataFrame(columns=["average", "max", "min"])

	categorical_df = df.select_dtypes(include=["object", "category"])
	categorical_rows = []
	for column in categorical_df.columns:
		value_counts = categorical_df[column].value_counts(dropna=True)
		if not value_counts.empty:
			categorical_rows.append(
				{
					"column": column,
					"top_category": str(value_counts.index[0]),
					"count": int(value_counts.iloc[0]),
				}
			)

	top_categories = pd.DataFrame(categorical_rows)

	insights = []
	insights.append(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

	null_count = int(df.isnull().sum().sum())
	insights.append(f"Total missing values: {null_count}")

	if not correlations.empty:
		corr_pairs = correlations.where(~np.eye(correlations.shape[0], dtype=bool))
		max_corr = corr_pairs.abs().stack().sort_values(ascending=False)
		if not max_corr.empty:
			top_pair = max_corr.index[0]
			top_value = correlations.loc[top_pair[0], top_pair[1]]
			insights.append(
				f"Strongest numeric correlation: {top_pair[0]} vs {top_pair[1]} = {top_value:.2f}"
			)
		else:
			insights.append("Not enough numeric variation to compute pairwise correlations.")
	else:
		insights.append("Correlation analysis requires at least two numeric columns.")

	if not numeric_summary.empty:
		insights.append("Numeric summary includes average, max, and min for numeric columns.")
	else:
		insights.append("No numeric columns available for average, max, and min summary.")

	if not top_categories.empty:
		insights.append("Top category identified for each categorical column.")
	else:
		insights.append("No categorical columns available for top category analysis.")

	insight_text = "\n".join(insights)

	return {
		"summary_statistics": summary_stats,
		"correlations": correlations,
		"numeric_summary": numeric_summary,
		"top_categories": top_categories,
		"insights": insight_text,
	}


def predict_salary_from_age(df, age):
	"""Train a simple regression model (Age -> Salary) and predict salary for input age."""
	if "Age" not in df.columns or "Salary" not in df.columns:
		return {
			"success": False,
			"message": "Required columns 'Age' and 'Salary' were not found in the dataset.",
		}

	model_data = df[["Age", "Salary"]].dropna().copy()
	model_data = model_data[pd.to_numeric(model_data["Age"], errors="coerce").notna()]
	model_data = model_data[pd.to_numeric(model_data["Salary"], errors="coerce").notna()]

	if model_data.shape[0] < 2:
		return {
			"success": False,
			"message": "Not enough valid rows to train regression model. Need at least 2 rows.",
		}

	X = model_data[["Age"]].astype(float)
	y = model_data["Salary"].astype(float)

	regressor = LinearRegression()
	regressor.fit(X, y)

	predicted_salary = float(regressor.predict(np.array([[float(age)]], dtype=float))[0])

	return {
		"success": True,
		"predicted_salary": predicted_salary,
		"training_rows": int(model_data.shape[0]),
		"coefficient": float(regressor.coef_[0]),
		"intercept": float(regressor.intercept_),
	}
