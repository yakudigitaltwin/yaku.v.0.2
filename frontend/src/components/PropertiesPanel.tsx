import React, { useState } from 'react';
import { ProcessUnit } from '../types/process';

interface PropertiesPanelProps {
  unit: ProcessUnit | null;
  onUpdate: (unit: ProcessUnit) => void;
  onClose: () => void;
}

interface ParameterField {
  key: string;
  label: string;
  unit: string;
  min: number;
  max: number;
  step: number;
}

const getParameterFields = (type: string): ParameterField[] => {
  switch (type) {
    case 'source':
      return [
        { key: 'Q_m3_s', label: 'Caudal', unit: 'm³/s', min: 0.01, max: 10, step: 0.01 },
        { key: 'turbidity_ntu', label: 'Turbidez', unit: 'NTU', min: 0, max: 1000, step: 1 },
        { key: 'pH', label: 'pH', unit: '', min: 0, max: 14, step: 0.1 }
      ];
    case 'rapid_mix':
      return [
        { key: 'Q_m3_s', label: 'Caudal', unit: 'm³/s', min: 0.01, max: 10, step: 0.01 },
        { key: 'volume_m3', label: 'Volumen', unit: 'm³', min: 1, max: 1000, step: 1 },
        { key: 'G_s', label: 'Gradiente de velocidad', unit: 's⁻¹', min: 10, max: 1000, step: 10 },
        { key: 'coagulant_mg_l', label: 'Dosis de coagulante', unit: 'mg/L', min: 0, max: 200, step: 1 }
      ];
    case 'flocculation':
      return [
        { key: 'Q_m3_s', label: 'Caudal', unit: 'm³/s', min: 0.01, max: 10, step: 0.01 },
        { key: 'volume_m3', label: 'Volumen', unit: 'm³', min: 10, max: 5000, step: 10 },
        { key: 'G_s', label: 'Gradiente de velocidad', unit: 's⁻¹', min: 5, max: 100, step: 1 }
      ];
    case 'sedimentation':
      return [
        { key: 'Q_m3_s', label: 'Caudal', unit: 'm³/s', min: 0.01, max: 10, step: 0.01 },
        { key: 'area_m2', label: 'Área superficial', unit: 'm²', min: 10, max: 10000, step: 10 },
        { key: 'depth_m', label: 'Profundidad', unit: 'm', min: 0.5, max: 10, step: 0.1 }
      ];
    case 'filtration':
      return [
        { key: 'Q_m3_s', label: 'Caudal', unit: 'm³/s', min: 0.01, max: 10, step: 0.01 },
        { key: 'area_m2', label: 'Área del filtro', unit: 'm²', min: 1, max: 1000, step: 1 },
        { key: 'headloss_m', label: 'Pérdida de carga', unit: 'm', min: 0.1, max: 5, step: 0.1 }
      ];
    case 'disinfection':
      return [
        { key: 'Q_m3_s', label: 'Caudal', unit: 'm³/s', min: 0.01, max: 10, step: 0.01 },
        { key: 'volume_m3', label: 'Volumen', unit: 'm³', min: 10, max: 5000, step: 10 },
        { key: 'chlorine_mg_l', label: 'Dosis de cloro', unit: 'mg/L', min: 0, max: 10, step: 0.1 }
      ];
    case 'tank':
      return [
        { key: 'Q_m3_s', label: 'Caudal', unit: 'm³/s', min: 0.01, max: 10, step: 0.01 },
        { key: 'volume_m3', label: 'Volumen', unit: 'm³', min: 1, max: 10000, step: 1 }
      ];
    default:
      return [];
  }
};

const PropertiesPanel: React.FC<PropertiesPanelProps> = ({ unit, onUpdate, onClose }) => {
  const [parameters, setParameters] = useState<Record<string, number>>(unit?.parameters || {});
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleParameterChange = (key: string, value: string) => {
    const numValue = parseFloat(value);
    const newParameters = { ...parameters, [key]: numValue };
    const newErrors = { ...errors };

    // Validate the parameter
    const field = getParameterFields(unit?.type || '').find(f => f.key === key);
    if (field) {
      if (isNaN(numValue)) {
        newErrors[key] = 'Debe ser un número válido';
      } else if (numValue < field.min || numValue > field.max) {
        newErrors[key] = `Debe estar entre ${field.min} y ${field.max}`;
      } else {
        delete newErrors[key];
      }
    }

    setParameters(newParameters);
    setErrors(newErrors);
  };

  const handleSave = () => {
    if (unit && Object.keys(errors).length === 0) {
      onUpdate({ ...unit, parameters });
      onClose();
    } else {
      alert('Por favor corrija los errores antes de guardar');
    }
  };

  const handleCancel = () => {
    setParameters(unit?.parameters || {});
    setErrors({});
    onClose();
  };

  if (!unit) {
    return (
      <div className="properties-panel">
        <div className="panel-header">
          <h3>Propiedades</h3>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>
        <div className="panel-content">
          <p>Seleccione una unidad para ver sus propiedades</p>
        </div>
      </div>
    );
  }

  const parameterFields = getParameterFields(unit.type);

  return (
    <div className="properties-panel">
      <div className="panel-header">
        <h3>Propiedades de {unit.name}</h3>
        <button className="close-btn" onClick={onClose}>×</button>
      </div>
      
      <div className="panel-content">
        <div className="info-section">
          <h4>Información de la unidad</h4>
          <div className="info-item">
            <label>Tipo:</label>
            <span>{unit.type}</span>
          </div>
          <div className="info-item">
            <label>Icono:</label>
            <span>{unit.icon}</span>
          </div>
          <div className="info-item">
            <label>Color:</label>
            <span>{unit.color}</span>
          </div>
        </div>

        <div className="parameters-section">
          <h4>Parámetros operativos</h4>
          {parameterFields.map(field => (
            <div key={field.key} className="parameter-field">
              <label>
                {field.label} ({field.unit})
                {errors[field.key] && (
                  <span className="error">{errors[field.key]}</span>
                )}
              </label>
              <input
                type="number"
                value={parameters[field.key] || ''}
                onChange={(e) => handleParameterChange(field.key, e.target.value)}
                min={field.min}
                max={field.max}
                step={field.step}
                className={errors[field.key] ? 'error' : ''}
              />
              <div className="parameter-hint">
                Rango: {field.min} - {field.max}
              </div>
            </div>
          ))}
        </div>

        <div className="actions">
          <button className="btn-secondary" onClick={handleCancel}>
            Cancelar
          </button>
          <button 
            className="btn-primary" 
            onClick={handleSave}
            disabled={Object.keys(errors).length > 0}
          >
            Guardar
          </button>
        </div>
      </div>
    </div>
  );
};

export default PropertiesPanel;