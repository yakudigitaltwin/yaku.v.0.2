"""
Sistema de validación para HYDROCALC-PTAP

Proporciona:
- Validación dimensional
- Verificación de rangos físicos
- Detección de errores comunes
- Sistema de warnings y errores estructurados
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from enum import Enum
import numpy as np


class ValidationLevel(Enum):
    """Niveles de severidad de validación"""
    INFO = "info"  # Información adicional
    WARNING = "warning"  # Advertencia, pero el cálculo es válido
    ERROR = "error"  # Error, el cálculo no puede proceder
    CRITICAL = "critical"  # Error crítico, posible peligro


@dataclass
class ValidationMessage:
    """Mensaje de validación individual"""
    level: ValidationLevel
    field: str
    message: str
    value: Optional[Any] = None
    expected: Optional[str] = None
    suggestion: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            'level': self.level.value,
            'field': self.field,
            'message': self.message,
            'value': self.value,
            'expected': self.expected,
            'suggestion': self.suggestion
        }


@dataclass
class ValidationResult:
    """Resultado de una validación completa"""
    is_valid: bool
    messages: List[ValidationMessage] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def add_info(self, field: str, message: str, **kwargs):
        """Agregar mensaje informativo"""
        self.messages.append(ValidationMessage(
            level=ValidationLevel.INFO,
            field=field,
            message=message,
            **kwargs
        ))
    
    def add_warning(self, field: str, message: str, **kwargs):
        """Agregar advertencia"""
        self.messages.append(ValidationMessage(
            level=ValidationLevel.WARNING,
            field=field,
            message=message,
            **kwargs
        ))
        self.is_valid = False
    
    def add_error(self, field: str, message: str, **kwargs):
        """Agregar error"""
        self.messages.append(ValidationMessage(
            level=ValidationLevel.ERROR,
            field=field,
            message=message,
            **kwargs
        ))
        self.is_valid = False
    
    def add_critical(self, field: str, message: str, **kwargs):
        """Agregar error crítico"""
        self.messages.append(ValidationMessage(
            level=ValidationLevel.CRITICAL,
            field=field,
            message=message,
            **kwargs
        ))
        self.is_valid = False
    
    def get_errors(self) -> List[ValidationMessage]:
        """Obtener solo errores y críticos"""
        return [m for m in self.messages 
                if m.level in (ValidationLevel.ERROR, ValidationLevel.CRITICAL)]
    
    def get_warnings(self) -> List[ValidationMessage]:
        """Obtener solo advertencias"""
        return [m for m in self.messages 
                if m.level == ValidationLevel.WARNING]
    
    def get_info(self) -> List[ValidationMessage]:
        """Obtener solo información"""
        return [m for m in self.messages 
                if m.level == ValidationLevel.INFO]
    
    def to_dict(self) -> dict:
        return {
            'is_valid': self.is_valid,
            'messages': [m.to_dict() for m in self.messages],
            'errors': [m.to_dict() for m in self.get_errors()],
            'warnings': [m.to_dict() for m in self.get_warnings()],
            'info': [m.to_dict() for m in self.get_info()],
            'context': self.context
        }
    
    def __str__(self) -> str:
        if self.is_valid:
            status = "✓ VÁLIDO"
        else:
            status = "✗ INVÁLIDO"
        
        lines = [f"Validación: {status}"]
        
        for msg in self.messages:
            icon = {'info': 'ℹ', 'warning': '⚠', 'error': '❌', 'critical': '🔴'}[msg.level.value]
            lines.append(f"  {icon} [{msg.field}] {msg.message}")
        
        return "\n".join(lines)


class Validator:
    """Clase base para validadores especializados"""
    
    @staticmethod
    def check_positive(value: float, field_name: str, 
                       allow_zero: bool = False) -> ValidationMessage:
        """Verificar que un valor sea positivo"""
        if allow_zero:
            if value < 0:
                return ValidationMessage(
                    level=ValidationLevel.ERROR,
                    field=field_name,
                    message=f"{field_name} debe ser mayor o igual a cero",
                    value=value,
                    expected=">= 0"
                )
        else:
            if value <= 0:
                return ValidationMessage(
                    level=ValidationLevel.ERROR,
                    field=field_name,
                    message=f"{field_name} debe ser mayor que cero",
                    value=value,
                    expected="> 0"
                )
        
        return ValidationMessage(
            level=ValidationLevel.INFO,
            field=field_name,
            message=f"{field_name} es positivo",
            value=value
        )
    
    @staticmethod
    def check_range(value: float, field_name: str, 
                    min_val: Optional[float] = None,
                    max_val: Optional[float] = None,
                    inclusive: bool = True) -> ValidationMessage:
        """Verificar que un valor esté dentro de un rango"""
        if min_val is not None:
            if inclusive:
                if value < min_val:
                    return ValidationMessage(
                        level=ValidationLevel.WARNING,
                        field=field_name,
                        message=f"{field_name} está por debajo del mínimo recomendado",
                        value=value,
                        expected=f">= {min_val}",
                        suggestion=f"Considere usar un valor >= {min_val}"
                    )
            else:
                if value <= min_val:
                    return ValidationMessage(
                        level=ValidationLevel.WARNING,
                        field=field_name,
                        message=f"{field_name} está por debajo del mínimo recomendado",
                        value=value,
                        expected=f"> {min_val}",
                        suggestion=f"Considere usar un valor > {min_val}"
                    )
        
        if max_val is not None:
            if inclusive:
                if value > max_val:
                    return ValidationMessage(
                        level=ValidationLevel.WARNING,
                        field=field_name,
                        message=f"{field_name} está por encima del máximo recomendado",
                        value=value,
                        expected=f"<= {max_val}",
                        suggestion=f"Considere usar un valor <= {max_val}"
                    )
            else:
                if value >= max_val:
                    return ValidationMessage(
                        level=ValidationLevel.WARNING,
                        field=field_name,
                        message=f"{field_name} está por encima del máximo recomendado",
                        value=value,
                        expected=f"< {max_val}",
                        suggestion=f"Considere usar un valor < {max_val}"
                    )
        
        return ValidationMessage(
            level=ValidationLevel.INFO,
            field=field_name,
            message=f"{field_name} está dentro del rango esperado",
            value=value
        )
    
    @staticmethod
    def check_not_nan(value: Any, field_name: str) -> ValidationMessage:
        """Verificar que un valor no sea NaN"""
        if isinstance(value, (int, float)) and np.isnan(value):
            return ValidationMessage(
                level=ValidationLevel.ERROR,
                field=field_name,
                message=f"{field_name} tiene un valor inválido (NaN)",
                value=value,
                expected="número válido"
            )
        
        return ValidationMessage(
            level=ValidationLevel.INFO,
            field=field_name,
            message=f"{field_name} es un número válido",
            value=value
        )
    
    @staticmethod
    def check_not_infinite(value: Any, field_name: str) -> ValidationMessage:
        """Verificar que un valor no sea infinito"""
        if isinstance(value, (int, float)) and np.isinf(value):
            return ValidationMessage(
                level=ValidationLevel.ERROR,
                field=field_name,
                message=f"{field_name} tiene un valor infinito",
                value=value,
                expected="número finito"
            )
        
        return ValidationMessage(
            level=ValidationLevel.INFO,
            field=field_name,
            message=f"{field_name} es finito",
            value=value
        )
    
    @staticmethod
    def check_dimensional_consistency(expected_dim: str, 
                                      actual_dim: str,
                                      field_name: str) -> ValidationMessage:
        """Verificar consistencia dimensional"""
        if expected_dim != actual_dim:
            return ValidationMessage(
                level=ValidationLevel.ERROR,
                field=field_name,
                message=f"Inconsistencia dimensional detectada",
                value=actual_dim,
                expected=expected_dim,
                suggestion=f"Verifique las unidades de entrada"
            )
        
        return ValidationMessage(
            level=ValidationLevel.INFO,
            field=field_name,
            message="Dimensiones consistentes",
            value=actual_dim
        )


# Validadores específicos para PTAP

class PTAPValidator(Validator):
    """Validador especializado para procesos PTAP"""
    
    @staticmethod
    def validate_flow(flow: float, unit: str = "m3_s") -> ValidationResult:
        """Validar caudal de entrada"""
        result = ValidationResult(is_valid=True)
        
        # Verificar no NaN
        msg = Validator.check_not_nan(flow, "caudal")
        result.messages.append(msg)
        if msg.level == ValidationLevel.ERROR:
            result.is_valid = False
            return result
        
        # Verificar positivo
        msg = Validator.check_positive(flow, "caudal")
        result.messages.append(msg)
        if msg.level == ValidationLevel.ERROR:
            result.is_valid = False
        
        # Verificar rango razonable (0.001 a 1000 m³/s)
        from core.units import convert_to_si
        try:
            flow_si, _ = convert_to_si(flow, unit)
            msg = Validator.check_range(flow_si, "caudal", 0.001, 1000)
            result.messages.append(msg)
        except Exception as e:
            result.add_error("caudal", f"Error en conversión de unidades: {str(e)}")
            result.is_valid = False
        
        return result
    
    @staticmethod
    def validate_detention_time(time: float, unit: str = "s",
                                process_type: str = "general") -> ValidationResult:
        """Validar tiempo de retención"""
        result = ValidationResult(is_valid=True)
        
        # Verificar no NaN
        msg = Validator.check_not_nan(time, "tiempo_retencion")
        result.messages.append(msg)
        if msg.level == ValidationLevel.ERROR:
            result.is_valid = False
            return result
        
        # Verificar positivo
        msg = Validator.check_positive(time, "tiempo_retencion")
        result.messages.append(msg)
        if msg.level == ValidationLevel.ERROR:
            result.is_valid = False
        
        # Convertir a segundos
        from core.units import convert_to_si
        try:
            time_si, _ = convert_to_si(time, unit)
            
            # Rangos según tipo de proceso
            ranges = {
                'rapid_mixing': (10, 60),  # segundos
                'flocculation': (900, 2700),  # 15-45 min en segundos
                'sedimentation': (7200, 21600),  # 2-6 h en segundos
                'filtration': (86400, 259200),  # 24-72 h en segundos
                'disinfection': (1200, 3600),  # 20-60 min en segundos
            }
            
            if process_type in ranges:
                min_t, max_t = ranges[process_type]
                msg = Validator.check_range(time_si, "tiempo_retencion", min_t, max_t)
                result.messages.append(msg)
                
                result.context['process_type'] = process_type
                result.context['recommended_range'] = f"{min_t}-{max_t} s"
        
        except Exception as e:
            result.add_error("tiempo_retencion", f"Error en conversión de unidades: {str(e)}")
            result.is_valid = False
        
        return result
    
    @staticmethod
    def validate_velocity_gradient(G: float, process_type: str = "flocculation") -> ValidationResult:
        """Validar gradiente de velocidad"""
        result = ValidationResult(is_valid=True)
        
        # Verificar no NaN
        msg = Validator.check_not_nan(G, "gradiente_velocidad")
        result.messages.append(msg)
        if msg.level == ValidationLevel.ERROR:
            result.is_valid = False
            return result
        
        # Verificar positivo
        msg = Validator.check_positive(G, "gradiente_velocidad")
        result.messages.append(msg)
        if msg.level == ValidationLevel.ERROR:
            result.is_valid = False
        
        # Rangos según tipo de proceso
        ranges = {
            'rapid_mixing': (300, 1000),
            'flocculation': (20, 80),
        }
        
        if process_type in ranges:
            min_G, max_G = ranges[process_type]
            msg = Validator.check_range(G, "gradiente_velocidad", min_G, max_G)
            result.messages.append(msg)
            
            result.context['process_type'] = process_type
            result.context['recommended_range'] = f"{min_G}-{max_G} s⁻¹"
        
        return result
    
    @staticmethod
    def validate_gt_number(GT: float, process_type: str = "flocculation") -> ValidationResult:
        """Validar número de Camp (GT)"""
        result = ValidationResult(is_valid=True)
        
        # Verificar no NaN
        msg = Validator.check_not_nan(GT, "numero_camp")
        result.messages.append(msg)
        if msg.level == ValidationLevel.ERROR:
            result.is_valid = False
            return result
        
        # Verificar positivo
        msg = Validator.check_positive(GT, "numero_camp")
        result.messages.append(msg)
        if msg.level == ValidationLevel.ERROR:
            result.is_valid = False
        
        # Rangos según tipo de proceso
        ranges = {
            'rapid_mixing': (10000, 60000),
            'flocculation': (20000, 200000),
        }
        
        if process_type in ranges:
            min_GT, max_GT = ranges[process_type]
            msg = Validator.check_range(GT, "numero_camp", min_GT, max_GT)
            result.messages.append(msg)
            
            result.context['process_type'] = process_type
            result.context['recommended_range'] = f"{min_GT}-{max_GT}"
        
        return result
    
    @staticmethod
    def validate_concentration(conc: float, chemical_type: str = "coagulant") -> ValidationResult:
        """Validar concentración química"""
        result = ValidationResult(is_valid=True)
        
        # Verificar no NaN
        msg = Validator.check_not_nan(conc, "concentracion")
        result.messages.append(msg)
        if msg.level == ValidationLevel.ERROR:
            result.is_valid = False
            return result
        
        # Verificar no negativo
        msg = Validator.check_positive(conc, "concentracion", allow_zero=True)
        result.messages.append(msg)
        if msg.level == ValidationLevel.ERROR:
            result.is_valid = False
        
        # Verificar rango razonable (0 a 1000 mg/L para coagulantes típicos)
        msg = Validator.check_range(conc, "concentracion", 0, 1000)
        result.messages.append(msg)
        
        return result


def validate_calculation(inputs: dict, validation_rules: dict) -> ValidationResult:
    """
    Validar múltiples entradas según reglas especificadas
    
    Args:
        inputs: Diccionario de valores de entrada {campo: valor}
        validation_rules: Diccionario de reglas {campo: tipo_validacion}
    
    Returns:
        ValidationResult consolidado
    """
    result = ValidationResult(is_valid=True)
    
    validator = PTAPValidator()
    
    for field, value in inputs.items():
        if field not in validation_rules:
            continue
        
        rule = validation_rules[field]
        
        if rule == 'flow':
            field_result = validator.validate_flow(value)
        elif rule == 'time':
            field_result = validator.validate_detention_time(value)
        elif rule == 'gradient':
            field_result = validator.validate_velocity_gradient(value)
        elif rule == 'gt':
            field_result = validator.validate_gt_number(value)
        elif rule == 'concentration':
            field_result = validator.validate_concentration(value)
        elif rule == 'positive':
            msg = Validator.check_positive(value, field)
            field_result = ValidationResult(is_valid=msg.level != ValidationLevel.ERROR)
            field_result.messages.append(msg)
        else:
            continue
        
        # Consolidar resultados
        result.is_valid = result.is_valid and field_result.is_valid
        result.messages.extend(field_result.messages)
    
    return result
