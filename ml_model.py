import json
import sys

import pandas as pd
from sklearn.linear_model import LinearRegression


REQUIRED_COLUMNS = ["Name", "Age", "Salary", "Department"]


def error_response(message):
    return {"success": False, "error": message}


def clean_data(df):
    cleaned = df.copy()

    # Normalize text columns and strip surrounding spaces.
    for col in ["Name", "Department"]:
        cleaned[col] = cleaned[col].astype(str).str.strip()

    cleaned["Age"] = pd.to_numeric(cleaned["Age"], errors="coerce")
    cleaned["Salary"] = pd.to_numeric(cleaned["Salary"], errors="coerce")
    cleaned = cleaned.drop_duplicates()
    cleaned = cleaned.dropna(subset=["Name", "Age", "Salary", "Department"])

    return cleaned


def process_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        return error_response("CSV file was not found.")
    except pd.errors.EmptyDataError:
        return error_response("CSV file is empty.")
    except pd.errors.ParserError:
        return error_response("Wrong CSV format. Unable to parse file.")
    except Exception as exc:
        return error_response(f"Failed to read CSV file: {exc}")

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        return error_response(
            "Missing required columns: " + ", ".join(missing_columns)
        )

    cleaned_df = clean_data(df)
    if cleaned_df.empty:
        return error_response("No valid rows available after cleaning.")

    train_df = cleaned_df[["Age", "Salary"]].dropna()
    if len(train_df) < 2:
        return error_response(
            "Not enough valid data to train model. Need at least 2 valid rows."
        )

    model = LinearRegression()
    model.fit(train_df[["Age"]], train_df["Salary"])

    output_df = cleaned_df.copy()
    output_df["predicted_salary"] = model.predict(output_df[["Age"]])

    result = {
        "success": True,
        "rows": len(output_df),
        "model": {
            "coefficient": float(model.coef_[0]),
            "intercept": float(model.intercept_),
        },
        "data": output_df.to_dict(orient="records"),
    }
    return result


def main():
    if len(sys.argv) < 2:
        print(
            json.dumps(
                error_response("Usage: python ml_model.py <path_to_csv>"),
                indent=2,
            )
        )
        sys.exit(1)

    csv_path = sys.argv[1]
    result = process_csv(csv_path)
    print(json.dumps(result, indent=2, default=str))

    if not result.get("success", False):
        sys.exit(1)


if __name__ == "__main__":
    main()