#!/usr/bin/env python3
"""
Test script for the new process unit calculation service function.
"""

from app.services.classic_service import calculate_unit

def test_calculate_unit():
    print("Testing process unit calculation service function...")
    
    # Test case 1: Sedimentation design calculation
    print("\nTesting sedimentation design calculation...")
    try:
        result = calculate_unit(
            "sedimentation",
            {"Q_m3_s": 0.5, "area_m2": 1500, "depth_m": 4},
            "design"
        )
        print("✓ Sedimentation design test passed")
        print(f"  Results: {result}")
        expected_keys = ["surface_overflow_m_s", "surface_overflow_m_h", "volume_m3", "detention_time_h"]
        for key in expected_keys:
            if key not in result:
                print(f"✗ Missing expected key: {key}")
    except Exception as e:
        print(f"✗ Sedimentation design test failed: {e}")
    
    # Test case 2: Filtration design calculation
    print("\nTesting filtration design calculation...")
    try:
        result = calculate_unit(
            "filtration",
            {"Q_m3_s": 0.5, "area_m2": 250},
            "design"
        )
        print("✓ Filtration design test passed")
        print(f"  Results: {result}")
        expected_keys = ["filtration_rate_m_h"]
        for key in expected_keys:
            if key not in result:
                print(f"✗ Missing expected key: {key}")
    except Exception as e:
        print(f"✗ Filtration design test failed: {e}")
    
    # Test case 3: Disinfection design calculation
    print("\nTesting disinfection design calculation...")
    try:
        result = calculate_unit(
            "disinfection",
            {"Q_m3_s": 0.5, "volume_m3": 900, "chlorine_mg_l": 1.5},
            "design"
        )
        print("✓ Disinfection design test passed")
        print(f"  Results: {result}")
        expected_keys = ["contact_time_min", "CT_mg_min_l"]
        for key in expected_keys:
            if key not in result:
                print(f"✗ Missing expected key: {key}")
    except Exception as e:
        print(f"✗ Disinfection design test failed: {e}")
    
    # Test case 4: Sedimentation performance calculation
    print("\nTesting sedimentation performance calculation...")
    try:
        result = calculate_unit(
            "sedimentation",
            {"Q_m3_s": 0.5, "area_m2": 1500},
            "performance"
        )
        print("✓ Sedimentation performance test passed")
        print(f"  Results: {result}")
        expected_keys = ["turbidity_removal_percent", "surface_overflow_rate_m_h", "efficiency_score"]
        for key in expected_keys:
            if key not in result:
                print(f"✗ Missing expected key: {key}")
    except Exception as e:
        print(f"✗ Sedimentation performance test failed: {e}")
    
    # Test case 5: Filtration performance calculation
    print("\nTesting filtration performance calculation...")
    try:
        result = calculate_unit(
            "filtration",
            {"Q_m3_s": 0.5, "area_m2": 250},
            "performance"
        )
        print("✓ Filtration performance test passed")
        print(f"  Results: {result}")
        expected_keys = ["turbidity_removal_percent", "filtration_rate_m_h", "efficiency_score"]
        for key in expected_keys:
            if key not in result:
                print(f"✗ Missing expected key: {key}")
    except Exception as e:
        print(f"✗ Filtration performance test failed: {e}")
    
    # Test case 6: Disinfection performance calculation
    print("\nTesting disinfection performance calculation...")
    try:
        result = calculate_unit(
            "disinfection",
            {"Q_m3_s": 0.5, "volume_m3": 900, "chlorine_mg_l": 1.5, "contact_time_min": 15},
            "performance"
        )
        print("✓ Disinfection performance test passed")
        print(f"  Results: {result}")
        expected_keys = ["CT_value_mg_min_l", "log_inactivation", "efficiency_score"]
        for key in expected_keys:
            if key not in result:
                print(f"✗ Missing expected key: {key}")
    except Exception as e:
        print(f"✗ Disinfection performance test failed: {e}")
    
    # Test case 7: Invalid unit type
    print("\nTesting invalid unit type...")
    try:
        result = calculate_unit(
            "invalid_unit",
            {"Q_m3_s": 0.5},
            "design"
        )
        print("✗ Invalid unit type test failed - should have raised exception")
    except ValueError as e:
        print(f"✓ Invalid unit type test passed: {e}")
    except Exception as e:
        print(f"✗ Invalid unit type test failed with unexpected error: {e}")
    
    # Test case 8: Invalid calculation type
    print("\nTesting invalid calculation type...")
    try:
        result = calculate_unit(
            "sedimentation",
            {"Q_m3_s": 0.5, "area_m2": 1500},
            "invalid_calculation"
        )
        print("✗ Invalid calculation type test failed - should have raised exception")
    except ValueError as e:
        print(f"✓ Invalid calculation type test passed: {e}")
    except Exception as e:
        print(f"✗ Invalid calculation type test failed with unexpected error: {e}")

if __name__ == "__main__":
    test_calculate_unit()