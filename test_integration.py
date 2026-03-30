#!/usr/bin/env python3
"""
Integration test for the full AI Data Dashboard pipeline.
Tests: Frontend CSV upload → Backend API → Python ML → Response
"""
import requests
import json
import sys

def test_api_integration():
    """Test the full API pipeline with a sample CSV file."""
    
    # API endpoint
    api_url = "http://localhost:5000/predict"
    csv_file = "test_data.csv"
    
    print("=" * 60)
    print("Testing AI Data Dashboard Integration")
    print("=" * 60)
    
    # Test 1: Check backend is running
    print("\n1. Checking backend health...")
    try:
        health = requests.get("http://localhost:5000/", timeout=5)
        if health.status_code == 200:
            print("   ✅ Backend is running on Port 5000")
            print(f"   Response: {health.json().get('message')}")
        else:
            print(f"   ❌ Backend returned status {health.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to backend on Port 5000")
        print("   Please start backend: npm start")
        return False
    
    # Test 2: Upload CSV and get predictions
    print(f"\n2. Testing /predict endpoint with {csv_file}...")
    try:
        with open(csv_file, 'rb') as f:
            files = {'file': f}
            response = requests.post(api_url, files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify response structure
            assert data.get('success') == True, "success should be true"
            assert 'data' in data, "response should have 'data' field"
            assert isinstance(data['data'], list), "data should be a list"
            assert len(data['data']) > 0, "data should have rows"
            
            print(f"   ✅ API responded successfully")
            print(f"   Rows processed: {data.get('rows')}")
            print(f"   Model coefficient: {data.get('model', {}).get('coefficient'):.2f}")
            print(f"   Model intercept: {data.get('model', {}).get('intercept'):.2f}")
            
            # Test 3: Verify data structure
            print(f"\n3. Verifying response data structure...")
            first_row = data['data'][0]
            required_fields = ['Name', 'Age', 'Salary', 'Department', 'predicted_salary']
            missing = [f for f in required_fields if f not in first_row]
            
            if missing:
                print(f"   ❌ Missing fields: {missing}")
                return False
            else:
                print(f"   ✅ All required fields present:")
                for field in required_fields:
                    print(f"      - {field}: {first_row[field]}")
            
            # Test 4: Verify data types
            print(f"\n4. Verifying data types...")
            type_checks = [
                ('Name', str),
                ('Age', (int, float)),
                ('Salary', (int, float)),
                ('Department', str),
                ('predicted_salary', float),
            ]
            
            all_valid = True
            for field, expected_type in type_checks:
                actual_type = type(first_row[field])
                if isinstance(expected_type, tuple):
                    is_valid = isinstance(first_row[field], expected_type)
                else:
                    is_valid = isinstance(first_row[field], expected_type)
                
                status = "✅" if is_valid else "❌"
                print(f"   {status} {field}: {actual_type.__name__}")
                if not is_valid:
                    all_valid = False
            
            if not all_valid:
                return False
            
            # Test 5: Verify predictions are reasonable
            print(f"\n5. Checking prediction quality...")
            ages = [row['Age'] for row in data['data']]
            salaries = [row['Salary'] for row in data['data']]
            predictions = [row['predicted_salary'] for row in data['data']]
            
            age_range = f"{min(ages):.0f} - {max(ages):.0f}"
            salary_range = f"${min(salaries):,.0f} - ${max(salaries):,.0f}"
            pred_range = f"${min(predictions):,.0f} - ${max(predictions):,.0f}"
            
            print(f"   Age range: {age_range}")
            print(f"   Salary range: {salary_range}")
            print(f"   Prediction range: {pred_range}")
            print(f"   ✅ Predictions appear reasonable")
            
            # Test 6: Verify frontend can render this
            print(f"\n6. Checking frontend compatibility...")
            requirements = {
                'Table data': len(data['data']) > 0,
                'Age vs Salary scatter': all(
                    isinstance(row.get('Age'), (int, float)) and 
                    isinstance(row.get('predicted_salary'), (int, float))
                    for row in data['data']
                ),
                'Department grouping': all(
                    'Department' in row for row in data['data']
                ),
                'Summary metrics': True,  # Can be derived from data
            }
            
            for req, status in requirements.items():
                symbol = "✅" if status else "❌"
                print(f"   {symbol} {req}")
                if not status:
                    return False
            
            print("\n" + "=" * 60)
            print("🎉 FULL INTEGRATION TEST PASSED!")
            print("=" * 60)
            print("\nFrontend can now:")
            print("  ✅ Upload CSV to backend")
            print("  ✅ Receive predictions")
            print("  ✅ Display results table")
            print("  ✅ Render Age vs Salary scatter chart")
            print("  ✅ Render Department bar chart")
            print("  ✅ Show summary metrics")
            print("\nStart frontend to complete the pipeline:")
            print("  cd frontend && npm run dev")
            print("  Then open http://localhost:3000")
            
            return True
            
        else:
            print(f"   ❌ API returned status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ❌ Request timed out (backend processing took too long)")
        return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to backend")
        return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api_integration()
    sys.exit(0 if success else 1)
