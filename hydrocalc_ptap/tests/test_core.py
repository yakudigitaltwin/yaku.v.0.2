"""
Tests para el núcleo de HYDROCALC-PTAP

Pruebas unitarias para:
- Sistema de unidades
- Constantes y parámetros
- Validación
"""

import pytest
import numpy as np

from core.units import (
    convert, convert_to_si, format_value,
    UnitConverter, list_available_units,
    UnitType
)
from core.constants import (
    get_water_properties,
    get_design_parameter,
    check_parameter_range,
    get_chemical,
    list_chemicals,
    calculate_dosage_mass
)
from core.validation import (
    Validator,
    PTAPValidator,
    ValidationResult,
    ValidationLevel,
    validate_calculation
)


# =============================================================================
# TESTS DE UNIDADES
# =============================================================================

class TestUnitConversion:
    """Tests para conversión de unidades"""
    
    def test_flow_conversion_L_s_to_m3_s(self):
        """Convertir L/s a m³/s"""
        result = convert(100, "L_s", "m3_s")
        assert abs(result - 0.1) < 1e-6
    
    def test_flow_conversion_m3_s_to_L_s(self):
        """Convertir m³/s a L/s"""
        result = convert(0.5, "m3_s", "L_s")
        assert abs(result - 500) < 1e-6
    
    def test_time_conversion_min_to_s(self):
        """Convertir minutos a segundos"""
        result = convert(30, "min", "s")
        assert abs(result - 1800) < 1e-6
    
    def test_time_conversion_h_to_s(self):
        """Convertir horas a segundos"""
        result = convert(24, "h", "s")
        assert abs(result - 86400) < 1e-6
    
    def test_volume_conversion_L_to_m3(self):
        """Convertir litros a m³"""
        result = convert(1000, "L", "m3")
        assert abs(result - 1.0) < 1e-6
    
    def test_concentration_conversion_mg_L_to_kg_m3(self):
        """Convertir mg/L a kg/m³"""
        result = convert(50, "mg_L", "kg_m3")
        assert abs(result - 0.05) < 1e-6
    
    def test_power_conversion_kW_to_W(self):
        """Convertir kW a W"""
        result = convert(2.5, "kW", "W")
        assert abs(result - 2500) < 1e-6
    
    def test_invalid_unit(self):
        """Probar unidad inválida"""
        with pytest.raises(ValueError):
            convert(100, "invalid_unit", "m3_s")
    
    def test_incompatible_units(self):
        """Probar conversión entre unidades incompatibles"""
        with pytest.raises(ValueError):
            convert(100, "L_s", "kg")  # Caudal a masa
    
    def test_convert_to_si(self):
        """Probar conversión directa a SI"""
        value, unit = convert_to_si(500, "L_s")
        assert abs(value - 0.5) < 1e-6
        assert unit == "m³/s"
    
    def test_format_value(self):
        """Probar formateo de valores"""
        formatted = format_value(500.123456, "L_s", decimals=2)
        assert formatted == "500.12 L/s"
    
    def test_unit_converter_class(self):
        """Probar clase UnitConverter con historial"""
        converter = UnitConverter()
        
        result = converter.convert(100, "L_s", "m3_s", context="test")
        assert abs(result - 0.1) < 1e-6
        
        history = converter.get_history()
        assert len(history) == 1
        assert history[0]['context'] == "test"
        
        converter.clear_history()
        assert len(converter.get_history()) == 0


# =============================================================================
# TESTS DE CONSTANTES
# =============================================================================

class TestWaterProperties:
    """Tests para propiedades del agua"""
    
    def test_water_properties_at_20C(self):
        """Propiedades del agua a 20°C"""
        props = get_water_properties(20)
        assert abs(props.density - 998.21) < 0.01
        assert abs(props.viscosity_dynamic - 1.002e-3) < 1e-5
    
    def test_water_properties_at_25C(self):
        """Propiedades del agua a 25°C"""
        props = get_water_properties(25)
        assert abs(props.viscosity_dynamic - 0.890e-3) < 1e-5
    
    def test_water_properties_interpolation(self):
        """Interpolación de propiedades entre temperaturas"""
        props = get_water_properties(22)  # Entre 20 y 25
        assert props.temperature == 22
        # La viscosidad debería estar entre los valores de 20 y 25°C
        assert 0.890e-3 < props.viscosity_dynamic < 1.002e-3
    
    def test_water_properties_out_of_range(self):
        """Temperatura fuera de rango usa valores límite"""
        props_low = get_water_properties(-10)
        assert props_low.temperature == 0  # Usa el valor más bajo disponible
        
        props_high = get_water_properties(100)
        assert props_high.temperature == 40  # Usa el valor más alto disponible


class TestDesignParameters:
    """Tests para parámetros de diseño"""
    
    def test_get_flocculation_G_parameter(self):
        """Obtener parámetro G para floculación"""
        param = get_design_parameter('flocculation', 'G')
        assert param is not None
        assert param.name == "Gradiente de velocidad"
        assert param.min_value == 20
        assert param.max_value == 80
    
    def test_check_G_in_range(self):
        """Verificar G dentro de rango"""
        result = check_parameter_range('flocculation', 'G', 50)
        assert result['in_range'] is True
        assert result['warning'] is None
    
    def test_check_G_out_of_range(self):
        """Verificar G fuera de rango"""
        result = check_parameter_range('flocculation', 'G', 100)
        assert result['in_range'] is False
        assert result['warning'] is not None
        assert "por encima" in result['warning']


class TestChemicals:
    """Tests para químicos"""
    
    def test_get_alum_chemical(self):
        """Obtener información del sulfato de aluminio"""
        chem = get_chemical('alum')
        assert chem is not None
        assert "aluminio" in chem.name.lower()
        assert chem.state == 'solid'
    
    def test_list_coagulant_chemicals(self):
        """Listar coagulantes disponibles"""
        coagulants = list_chemicals('coagulación')
        assert len(coagulants) > 0
        assert 'alum' in coagulants
    
    def test_calculate_dosage_mass(self):
        """Calcular masa diaria de químico"""
        # Q = 86400 m³/d (1 m³/s), Dosis = 20 mg/L
        mass = calculate_dosage_mass(86400, 20, 'alum', purity=98)
        # Masa esperada: 86400 × 20 / (0.98 × 1000) = 1763.27 kg/d
        assert abs(mass - 1763.27) < 1


# =============================================================================
# TESTS DE VALIDACIÓN
# =============================================================================

class TestValidation:
    """Tests para sistema de validación"""
    
    def test_check_positive_valid(self):
        """Verificar valor positivo válido"""
        msg = Validator.check_positive(100, "caudal")
        assert msg.level == ValidationLevel.INFO
    
    def test_check_positive_invalid(self):
        """Verificar valor positivo inválido"""
        msg = Validator.check_positive(-5, "caudal")
        assert msg.level == ValidationLevel.ERROR
        assert "mayor que cero" in msg.message
    
    def test_check_range_within(self):
        """Verificar valor dentro de rango"""
        msg = Validator.check_range(50, "G", min_val=20, max_val=80)
        assert msg.level == ValidationLevel.INFO
    
    def test_check_range_below(self):
        """Verificar valor por debajo del rango"""
        msg = Validator.check_range(10, "G", min_val=20, max_val=80)
        assert msg.level == ValidationLevel.WARNING
        assert "por debajo" in msg.message
    
    def test_check_range_above(self):
        """Verificar valor por encima del rango"""
        msg = Validator.check_range(100, "G", min_val=20, max_val=80)
        assert msg.level == ValidationLevel.WARNING
        assert "por encima" in msg.message
    
    def test_validation_result_aggregation(self):
        """Agregar múltiples mensajes de validación"""
        result = ValidationResult(is_valid=True)
        
        result.add_info("field1", "Información")
        result.add_warning("field2", "Advertencia")
        result.add_error("field3", "Error")
        
        assert len(result.messages) == 3
        assert len(result.get_errors()) == 1
        assert len(result.get_warnings()) == 1
        assert len(result.get_info()) == 1
        assert result.is_valid is False
    
    def test_ptap_validator_flow(self):
        """Validar caudal con PTAPValidator"""
        validator = PTAPValidator()
        result = validator.validate_flow(500, "L_s")
        
        assert result.is_valid is True
        # Debería tener al menos un mensaje info
        assert len(result.get_info()) > 0
    
    def test_ptap_validator_invalid_flow(self):
        """Validar caudal inválido"""
        validator = PTAPValidator()
        result = validator.validate_flow(-10, "L_s")
        
        assert result.is_valid is False
        assert len(result.get_errors()) > 0
    
    def test_validate_calculation_function(self):
        """Probar función validate_calculation"""
        inputs = {
            'flow': 500,
            'time': 30,
            'gradient': 50
        }
        
        rules = {
            'flow': 'flow',
            'time': 'time',
            'gradient': 'gradient'
        }
        
        result = validate_calculation(inputs, rules)
        
        # Todos deberían ser válidos con estos valores
        assert result.is_valid is True


# =============================================================================
# TESTS DE EJECUCIÓN
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
