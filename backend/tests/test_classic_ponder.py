"""
Test cases for classic ponder calculation module
"""

import pytest
from app.calculations.classic_ponder import (
    validate_input_values,
    classic_ponder_calculation,
    calculate_hydraulic_loading_rate,
    calculate_surface_overflow_rate,
    calculate_detention_time,
    calculate_mixing_energy,
    calculate_floculation_efficiency,
    calculate_filtration_rate,
    calculate_disinfection_contact_time,
    calculate_CT_value,
    calculate_unit_efficiency,
    PonderResult
)


class TestInputValidation:
    """Test input validation functions"""
    
    def test_valid_flow_rate(self):
        """Test valid flow rate validation"""
        warnings = validate_input_values(Q_m3_s=0.5)
        assert len(warnings) == 0
    
    def test_invalid_flow_rate_negative(self):
        """Test negative flow rate validation"""
        warnings = validate_input_values(Q_m3_s=-0.1)
        assert len(warnings) > 0
        assert "Flow rate (Q_m3_s) must be positive" in warnings[0]
    
    def test_invalid_flow_rate_high(self):
        """Test unusually high flow rate validation"""
        warnings = validate_input_values(Q_m3_s=15.0)
        assert len(warnings) > 0
        assert "Flow rate (Q_m3_s) seems unusually high" in warnings[0]
    
    def test_valid_volume(self):
        """Test valid volume validation"""
        warnings = validate_input_values(volume_m3=1000)
        assert len(warnings) == 0
    
    def test_invalid_volume_negative(self):
        """Test negative volume validation"""
        warnings = validate_input_values(volume_m3=-50)
        assert len(warnings) > 0
        assert "Volume must be positive" in warnings[0]
    
    def test_valid_area(self):
        """Test valid area validation"""
        warnings = validate_input_values(area_m2=500)
        assert len(warnings) == 0
    
    def test_valid_depth(self):
        """Test valid depth validation"""
        warnings = validate_input_values(depth_m=3.5)
        assert len(warnings) == 0
    
    def test_invalid_depth_negative(self):
        """Test negative depth validation"""
        warnings = validate_input_values(depth_m=-1.0)
        assert len(warnings) > 0
        assert "Depth must be positive" in warnings[0]
    
    def test_valid_G_s(self):
        """Test valid velocity gradient validation"""
        warnings = validate_input_values(G_s=500)
        assert len(warnings) == 0
    
    def test_valid_coagulant_dosage(self):
        """Test valid coagulant dosage validation"""
        warnings = validate_input_values(coagulant_mg_l=25)
        assert len(warnings) == 0
    
    def test_invalid_coagulant_dosage_negative(self):
        """Test negative coagulant dosage validation"""
        warnings = validate_input_values(coagulant_mg_l=-5)
        assert len(warnings) > 0
        assert "Coagulant dosage cannot be negative" in warnings[0]
    
    def test_valid_chlorine_dosage(self):
        """Test valid chlorine dosage validation"""
        warnings = validate_input_values(chlorine_mg_l=2.0)
        assert len(warnings) == 0
    
    def test_valid_turbidity(self):
        """Test valid turbidity validation"""
        warnings = validate_input_values(turbidity_ntu=50)
        assert len(warnings) == 0
    
    def test_valid_ph(self):
        """Test valid pH validation"""
        warnings = validate_input_values(pH=7.2)
        assert len(warnings) == 0
    
    def test_invalid_ph_range(self):
        """Test invalid pH range validation"""
        warnings = validate_input_values(pH=15)
        assert len(warnings) > 0
        assert "pH must be between 0 and 14" in warnings[0]


class TestHydraulicCalculations:
    """Test hydraulic calculation functions"""
    
    def test_hydraulic_loading_rate(self):
        """Test hydraulic loading rate calculation"""
        result = calculate_hydraulic_loading_rate(0.5, 1000)
        expected = (0.5 * 86400) / 1000  # 43.2 m³/m²/day
        assert abs(result - expected) < 0.001
    
    def test_surface_overflow_rate(self):
        """Test surface overflow rate calculation"""
        result = calculate_surface_overflow_rate(0.5, 1000)
        expected = (0.5 * 3600) / 1000  # 1.8 m³/m²/h
        assert abs(result - expected) < 0.001
    
    def test_detention_time(self):
        """Test detention time calculation"""
        result = calculate_detention_time(1000, 0.5)
        expected = 1000 / 0.5 / 3600  # 0.555... hours
        assert abs(result - expected) < 0.001
    
    def test_mixing_energy(self):
        """Test mixing energy calculation"""
        result = calculate_mixing_energy(500, 30, 0.001)
        expected = 0.001 * (500 ** 2) * 30  # 7,500,000 watts
        assert abs(result - expected) < 0.001
    
    def test_floculation_efficiency(self):
        """Test floculation efficiency calculation"""
        result = calculate_floculation_efficiency(30, 0.5)  # 30 s⁻¹, 0.5 hours
        expected = 30 * 0.5 * 3600  # 54,000
        assert abs(result - expected) < 0.001
    
    def test_filtration_rate(self):
        """Test filtration rate calculation"""
        result = calculate_filtration_rate(0.5, 250)
        expected = (0.5 * 3600) / 250  # 7.2 m³/m²/h
        assert abs(result - expected) < 0.001
    
    def test_disinfection_contact_time(self):
        """Test disinfection contact time calculation"""
        result = calculate_disinfection_contact_time(900, 0.5)
        expected = (900 / 0.5) / 60  # 30 minutes
        assert abs(result - expected) < 0.001
    
    def test_CT_value(self):
        """Test CT value calculation"""
        result = calculate_CT_value(2.0, 30)  # 2.0 mg/L, 30 minutes
        expected = 2.0 * 30  # 60 mg·min/L
        assert abs(result - expected) < 0.001


class TestUnitEfficiency:
    """Test unit efficiency calculations"""
    
    def test_sedimentation_efficiency(self):
        """Test sedimentation efficiency calculation"""
        parameters = {"area_m2": 1500, "Q_m3_s": 0.5}
        result = calculate_unit_efficiency("sedimentation", parameters)
        
        assert "surface_overflow_rate_m_h" in result
        assert "efficiency_score" in result
        assert "turbidity_removal_percent" in result
        assert result["turbidity_removal_percent"] == 65
    
    def test_filtration_efficiency(self):
        """Test filtration efficiency calculation"""
        parameters = {"area_m2": 250, "Q_m3_s": 0.5}
        result = calculate_unit_efficiency("filtration", parameters)
        
        assert "filtration_rate_m_h" in result
        assert "efficiency_score" in result
        assert "turbidity_removal_percent" in result
        assert result["turbidity_removal_percent"] == 85
    
    def test_disinfection_efficiency(self):
        """Test disinfection efficiency calculation"""
        parameters = {"chlorine_mg_l": 2.0, "contact_time_min": 30}
        result = calculate_unit_efficiency("disinfection", parameters)
        
        assert "CT_value_mg_min_l" in result
        assert "efficiency_score" in result
        assert "log_inactivation" in result
    
    def test_rapid_mix_efficiency(self):
        """Test rapid mix efficiency calculation"""
        parameters = {"G_s": 700, "volume_m3": 30, "Q_m3_s": 0.5}
        result = calculate_unit_efficiency("rapid_mix", parameters)
        
        assert "G_s" in result
        assert "efficiency_score" in result
        assert "detention_time_min" in result
        assert "power_w" in result
    
    def test_flocculation_efficiency(self):
        """Test flocculation efficiency calculation"""
        parameters = {"G_s": 30, "volume_m3": 750, "Q_m3_s": 0.5}
        result = calculate_unit_efficiency("flocculation", parameters)
        
        assert "G_s" in result
        assert "efficiency_score" in result
        assert "Gt_value" in result
        assert "detention_time_min" in result


class TestClassicPonderCalculation:
    """Test classic ponder calculation function"""
    
    def test_rapid_mix_design_calculation(self):
        """Test rapid mix design calculation"""
        parameters = {
            "Q_m3_s": 0.5,
            "volume_m3": 30,
            "G_s": 60,
            "id": "rapid_mix_unit"
        }
        
        result = classic_ponder_calculation("rapid_mix", parameters, "design")
        
        assert isinstance(result, PonderResult)
        assert result.unit_id == "rapid_mix_unit"
        assert result.unit_type == "rapid_mix"
        assert result.calculation_type == "design"
        assert result.validation_passed
        assert len(result.warnings) == 0
        assert "detention_time_s" in result.variables_used
        assert "power_w" in result.variables_used
    
    def test_sedimentation_design_calculation(self):
        """Test sedimentation design calculation"""
        parameters = {
            "Q_m3_s": 0.5,
            "area_m2": 1500,
            "depth_m": 4,
            "id": "sedimentation_unit"
        }
        
        result = classic_ponder_calculation("sedimentation", parameters, "design")
        
        assert isinstance(result, PonderResult)
        assert result.unit_id == "sedimentation_unit"
        assert result.unit_type == "sedimentation"
        assert result.calculation_type == "design"
        assert result.validation_passed
        assert "surface_overflow_rate_m_h" in result.variables_used
        assert "hydraulic_loading_rate_m3_m2_day" in result.variables_used
    
    def test_filtration_performance_calculation(self):
        """Test filtration performance calculation"""
        parameters = {
            "Q_m3_s": 0.5,
            "area_m2": 250,
            "id": "filtration_unit"
        }
        
        result = classic_ponder_calculation("filtration", parameters, "performance")
        
        assert isinstance(result, PonderResult)
        assert result.unit_id == "filtration_unit"
        assert result.unit_type == "filtration"
        assert result.calculation_type == "performance"
        assert result.validation_passed
        assert "efficiency_score" in result.variables_used
    
    def test_disinfection_efficiency_calculation(self):
        """Test disinfection efficiency calculation"""
        parameters = {
            "Q_m3_s": 0.5,
            "volume_m3": 900,
            "chlorine_mg_l": 1.5,
            "id": "disinfection_unit"
        }
        
        result = classic_ponder_calculation("disinfection", parameters, "efficiency")
        
        assert isinstance(result, PonderResult)
        assert result.unit_id == "disinfection_unit"
        assert result.unit_type == "disinfection"
        assert result.calculation_type == "efficiency"
        assert result.validation_passed
        assert "efficiency_score" in result.variables_used
    
    def test_invalid_unit_type(self):
        """Test handling of invalid unit type"""
        parameters = {"Q_m3_s": 0.5}
        
        result = classic_ponder_calculation("invalid_unit", parameters, "design")
        
        assert isinstance(result, PonderResult)
        assert not result.validation_passed
        assert len(result.warnings) > 0
        assert "Unsupported unit type" in result.warnings[0]
    
    def test_invalid_calculation_type(self):
        """Test handling of invalid calculation type"""
        parameters = {"Q_m3_s": 0.5}
        
        result = classic_ponder_calculation("rapid_mix", parameters, "invalid_type")
        
        assert isinstance(result, PonderResult)
        assert not result.validation_passed
        assert len(result.warnings) > 0
        assert "Unsupported calculation type" in result.warnings[0]
    
    def test_invalid_input_values(self):
        """Test handling of invalid input values"""
        parameters = {
            "Q_m3_s": -0.5,  # Invalid negative flow rate
            "volume_m3": -30,  # Invalid negative volume
            "id": "invalid_unit"
        }
        
        result = classic_ponder_calculation("rapid_mix", parameters, "design")
        
        assert isinstance(result, PonderResult)
        assert not result.validation_passed
        assert len(result.warnings) > 0
        assert any("Flow rate" in warning for warning in result.warnings)
        assert any("Volume" in warning for warning in result.warnings)


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_zero_values(self):
        """Test handling of zero values"""
        with pytest.raises(ValueError, match="must be positive"):
            calculate_hydraulic_loading_rate(0, 1000)
        
        with pytest.raises(ValueError, match="must be positive"):
            calculate_surface_overflow_rate(0.5, 0)
        
        with pytest.raises(ValueError, match="must be positive"):
            calculate_detention_time(1000, 0)
    
    def test_extreme_values(self):
        """Test handling of extreme values"""
        warnings = validate_input_values(
            Q_m3_s=9.9,  # Just below warning threshold
            volume_m3=49999,  # Just below warning threshold
            area_m2=99999,  # Just below warning threshold
            depth_m=19.9,  # Just below warning threshold
            G_s=999,  # Just below warning threshold
            coagulant_mg_l=199,  # Just below warning threshold
            chlorine_mg_l=9.9,  # Just below warning threshold
            turbidity_ntu=999,  # Just below warning threshold
            pH=6.9  # Valid pH
        )
        
        # Should have no warnings for values just below thresholds
        assert len(warnings) == 0
    
    def test_extreme_values_with_warnings(self):
        """Test handling of extreme values that trigger warnings"""
        warnings = validate_input_values(
            Q_m3_s=10.1,  # Above warning threshold
            volume_m3=50001,  # Above warning threshold
            area_m2=100001,  # Above warning threshold
            depth_m=20.1,  # Above warning threshold
            G_s=1001,  # Above warning threshold
            coagulant_mg_l=201,  # Above warning threshold
            chlorine_mg_l=10.1,  # Above warning threshold
            turbidity_ntu=1001,  # Above warning threshold
            pH=15  # Invalid pH
        )
        
        # Should have multiple warnings
        assert len(warnings) > 5


if __name__ == "__main__":
    pytest.main([__file__])