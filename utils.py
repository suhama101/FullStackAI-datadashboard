"""
OPTIONAL DEV TOOL SUPPORT - Used by the Streamlit app (app.py) for interactive analysis.

Main production ML cleaning: ml_model.py (called by server.js backend)

Note: The main API uses its own cleaning logic in ml_model.py.
This utility is only for the Streamlit dev dashboard.

See ARCHITECTURE.md for details.
"""


def clean_data(df):
	"""Remove null values and duplicate rows from a dataframe."""
	cleaned_df = df.dropna().drop_duplicates()
	return cleaned_df
