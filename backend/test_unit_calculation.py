#!/usr/bin/env python3
"""
Test script for the new process unit calculation API endpoint.
"""

import requests
import json

# Test the new API endpoint
def test_unit_calculation():
    url = "http://localhost:8000/classic/calculate-unit"
    
    # Test case 1: Sedimentation design calculation
    test_data_1 = {
        "unit_id": "sedimentation_test",
        "unit_type": "sedimentation",
        "parameters": {
            "Q_m3_s": 0.5,
            "area_m2": 1500,
            "depth_m": 4
        },
        "calculation_type": "design"
    }
    
    print("Testing sedimentation design calculation...")
    try:
        response = requests.post(url, json=test_data_1)
        if response.status_code == 200:
            result = response.json()
            print("✓ Sedimentation design test passed")
            print(f"  Results: {result}")
        else:
            print(f"✗ Sedimentation design test failed: {response.status_code}")
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"✗ Sedimentation design test failed with exception: {e}")
    
    # Test case 2: Filtration performance calculation
    test_data_2 = {
        "unit_id": "filtration_test",
        "unit_type": "filtration",
        "parameters": {
            "Q_m3_s": 0.5,
            "area_m2": 250,
            "contact_time_min": 15
        },
        "calculation_type": "performance"
    }
    
    print("\nTesting filtration performance calculation...")
    try:
        response = requests.post(url, json=test_data_2)
        if response.status_code == 200:
            result = response.json()
            print("✓ Filtration performance test passed")
            print(f"  Results: {result}")
        else:
            print(f"✗ Filtration performance test failed: {response.status_code}")
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"✗ Filtration performance test failed with exception: {e}")
    
    # Test case 3: Disinfection performance calculation
    test_data_3 = {
        "unit_id": "disinfection_test",
        "unit_type": "disinfection",
        "parameters": {
            "Q_m3_s": 0.5,
            "volume_m3": 900,
            "chlorine_mg_l": 1.5,
            "contact_time_min": 15
        },
        "calculation_type": "performance"
    }
    
    print("\nTesting disinfection performance calculation...")
    try:
        response = requests.post(url, json=test_data_3)
        if response.status_code == 200:
            result = response.json()
            print("✓ Disinfection performance test passed")
            print(f"  Results: {result}")
        else:
            print(f"✗ Disinfection performance test failed: {response.status_code}")
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"✗ Disinfection performance test failed with exception: {e}")

if __name__ == "__main__":
    print("Testing process unit calculation API endpoint...")
    test_unit_calculation()