"""
OPTIONAL DEV TOOL - Not part of the main production dashboard.

This Streamlit app is provided for interactive data exploration and analysis during development.

Main production dashboard: frontend/app/page.tsx (Next.js)
Main API backend: server.js (Express)
Main ML engine: ml_model.py (Python)

To run this app:
	.venv\\Scripts\\Activate.ps1
  streamlit run app.py

See ARCHITECTURE.md for full system details.
"""
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils import clean_data
from model import analyze_data, predict_salary_from_age


st.set_page_config(page_title="AI Data Analytics Dashboard", layout="wide")
st.title("🎯 AI Data Analytics Dashboard")

st.sidebar.header("📁 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
	try:
		with st.spinner("Loading CSV file..."):
			df = pd.read_csv(uploaded_file)
		st.sidebar.success("✅ CSV uploaded successfully.")
		
		# Sidebar Navigation
		st.sidebar.markdown("---")
		st.sidebar.header("🧭 Navigation")
		page = st.sidebar.radio(
			"Select a section:",
			options=["Overview", "Filters & Search", "Predictions", "Insights", "Visualizations"],
			index=0
		)

		# Process data once with spinner
		with st.spinner("Cleaning data..."):
			cleaned_df = clean_data(df)
		
		# OVERVIEW SECTION
		if page == "Overview":
			st.header("📊 Data Overview")
			col1, col2 = st.columns(2)
			with col1:
				st.metric("Total Rows", df.shape[0])
			with col2:
				st.metric("Total Columns", df.shape[1])
			
			st.subheader("Raw Dataset")
			st.dataframe(df, use_container_width=True)

			st.subheader("Cleaned Dataset")
			st.dataframe(cleaned_df, use_container_width=True)

			csv_data = cleaned_df.to_csv(index=False).encode("utf-8")
			st.download_button(
				label="⬇️ Download Cleaned Dataset as CSV",
				data=csv_data,
				file_name="cleaned_dataset.csv",
				mime="text/csv",
			)
		
		# FILTERS & SEARCH SECTION
		elif page == "Filters & Search":
			st.header("🔍 Filters & Search")
			
			filtered_df = cleaned_df
			col1, col2 = st.columns(2)
			
			with col1:
				if "Department" in cleaned_df.columns:
					department_values = cleaned_df["Department"].dropna().astype(str).unique().tolist()
					department_values.sort()
					department_options = ["All"] + department_values
					selected_department = st.selectbox("Filter by Department", department_options)

					if selected_department != "All":
						filtered_df = cleaned_df[
							cleaned_df["Department"].astype(str) == selected_department
						]
				else:
					st.info("'Department' column not found.")
			
			with col2:
				if "Name" in filtered_df.columns:
					search_name = st.text_input("Search by Name")
					if search_name:
						filtered_df = filtered_df[
							filtered_df["Name"].astype(str).str.contains(search_name, case=False, na=False)
						]
				else:
					st.info("'Name' column not found.")

			st.subheader("Filtered Results")
			st.dataframe(filtered_df, use_container_width=True)

		# PREDICTIONS SECTION
		elif page == "Predictions":
			st.header("🤖 ML Prediction")
			st.markdown("Predict salary based on age using a linear regression model.")
			
			col1, col2 = st.columns([1, 2])
			with col1:
				age_input = st.number_input("Enter Age", min_value=0.0, step=1.0, value=30.0)
				predict_button = st.button("🔮 Predict Salary", key="pred_btn")
			
			with col2:
				st.empty()
			
			if predict_button:
				with st.spinner("Training model and predicting..."):
					prediction_result = predict_salary_from_age(cleaned_df, age_input)
				
				if prediction_result["success"]:
					st.success(
						f"✅ Predicted Salary for age {age_input:.0f}: "
						f"${prediction_result['predicted_salary']:,.2f}"
					)
					col1, col2, col3 = st.columns(3)
					with col1:
						st.metric("Training Rows", prediction_result['training_rows'])
					with col2:
						st.metric("Coefficient", f"{prediction_result['coefficient']:.4f}")
					with col3:
						st.metric("Intercept", f"{prediction_result['intercept']:.2f}")
				else:
					st.info(f"ℹ️ {prediction_result['message']}")

		# INSIGHTS SECTION
		elif page == "Insights":
			st.header("💡 Data Insights")
			
			with st.spinner("Analyzing data..."):
				analysis = analyze_data(cleaned_df)
			
			st.markdown("#### 📈 Summary")
			st.write(analysis["insights"])

			st.markdown("#### 🔢 Numeric Column Statistics")
			if not analysis["numeric_summary"].empty:
				st.dataframe(analysis["numeric_summary"], use_container_width=True)
			else:
				st.info("No numeric columns available.")

			st.markdown("#### 🏷️ Top Categories by Column")
			if not analysis["top_categories"].empty:
				st.dataframe(analysis["top_categories"], use_container_width=True)
			else:
				st.info("No categorical columns available.")

		# VISUALIZATIONS SECTION
		elif page == "Visualizations":
			st.header("📉 Data Visualizations")

			with st.spinner("Generating visualizations..."):
				# Salary Boxplot
				if "Salary" in cleaned_df.columns:
					salary_values = pd.to_numeric(cleaned_df["Salary"], errors="coerce").dropna()
					if not salary_values.empty:
						st.subheader("💰 Salary Distribution")
						fig, ax = plt.subplots(figsize=(8, 4))
						sns.boxplot(x=salary_values, ax=ax)
						ax.set_title("Salary Boxplot")
						ax.set_xlabel("Salary")
						ax.set_ylabel("Value")
						st.pyplot(fig)
						plt.close(fig)
					else:
						st.info("'Salary' column exists, but no valid numeric salary values were found.")
				else:
					st.info("'Salary' column not found.")

				# Department Countplot
				if "Department" in cleaned_df.columns:
					department_values = cleaned_df["Department"].dropna().astype(str)
					if not department_values.empty:
						st.subheader("🏢 Employee Count by Department")
						fig, ax = plt.subplots(figsize=(8, 4))
						order = department_values.value_counts().index
						sns.countplot(x=department_values, order=order, ax=ax)
						ax.set_title("Department Countplot")
						ax.set_xlabel("Department")
						ax.set_ylabel("Count")
						ax.tick_params(axis="x", rotation=45)
						st.pyplot(fig)
						plt.close(fig)
					else:
						st.info("'Department' column exists, but no values found.")
				else:
					st.info("'Department' column not found.")

				# Numeric Histograms
				numeric_columns = cleaned_df.select_dtypes(include="number").columns
				if len(numeric_columns) > 0:
					st.subheader("📊 Numeric Distributions (Histograms)")
					for column in numeric_columns:
						fig, ax = plt.subplots(figsize=(8, 4))
						sns.histplot(cleaned_df[column], kde=True, ax=ax)
						ax.set_title(f"Distribution of {column}")
						ax.set_xlabel(column)
						ax.set_ylabel("Count")
						st.pyplot(fig)
						plt.close(fig)
				else:
					st.info("No numeric columns available for histogram plots.")

				# Categorical Bar Charts
				categorical_columns = cleaned_df.select_dtypes(include=["object", "category"]).columns
				if len(categorical_columns) > 0:
					st.subheader("🏷️ Categorical Distributions (Bar Charts)")
					for column in categorical_columns:
						counts = cleaned_df[column].value_counts().head(20)
						fig, ax = plt.subplots(figsize=(8, 4))
						sns.barplot(x=counts.index.astype(str), y=counts.values, ax=ax)
						ax.set_title(f"Top Categories in {column}")
						ax.set_xlabel(column)
						ax.set_ylabel("Count")
						ax.tick_params(axis="x", rotation=45)
						st.pyplot(fig)
						plt.close(fig)
				else:
					st.info("No categorical columns available for bar charts.")
	except Exception as exc:
		st.error(f"❌ Error reading CSV file: {exc}")
else:
	st.info("📤 Please upload a CSV file to view the dataset.")
