import React, { useState, useRef } from 'react';
import { useDrag, useDrop } from 'react-dnd';
import { ProcessUnit } from '../types/process';

interface ProcessNodeProps {
  unit: ProcessUnit;
  isSelected: boolean;
  onSelect: () => void;
  onUpdate: (unit: ProcessUnit) => void;
  onDelete: (unitId: string) => void;
  onConnection: (targetId: string) => void;
}

const ProcessNode: React.FC<ProcessNodeProps> = ({
  unit,
  isSelected,
  onSelect,
  onUpdate,
  onDelete,
  onConnection
}) => {
  const [isConnecting, setIsConnecting] = useState(false);
  const nodeRef = useRef<HTMLDivElement>(null);

  const [, drag] = useDrag(() => ({
    type: 'node',
    item: { id: unit.id },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  }));

  const [, drop] = useDrop(() => ({
    accept: 'node',
    hover: (item: { id: string }) => {
      if (item.id !== unit.id) {
        setIsConnecting(true);
      }
    },
    drop: (item: { id: string }) => {
      if (item.id !== unit.id) {
        onConnection(unit.id);
      }
      setIsConnecting(false);
    },
    collect: (monitor) => ({
      isOver: !!monitor.isOver(),
    }),
  }));

  drag(drop(nodeRef));

  const handleDoubleClick = () => {
    const newName = prompt('Editar nombre:', unit.name);
    if (newName && newName.trim()) {
      onUpdate({ ...unit, name: newName.trim() });
    }
  };

  const handleDelete = () => {
    if (confirm(`¿Eliminar unidad "${unit.name}"?`)) {
      onDelete(unit.id);
    }
  };

  const getNodeTypeName = (type: string) => {
    const typeNames: Record<string, string> = {
      'source': 'Fuente',
      'rapid_mix': 'Coagulación',
      'flocculation': 'Floculación',
      'sedimentation': 'Sedimentación',
      'filtration': 'Filtración',
      'disinfection': 'Desinfección',
      'tank': 'Tanque'
    };
    return typeNames[type] || type;
  };

  return (
    <div
      ref={nodeRef}
      className={`process-node ${isSelected ? 'selected' : ''} ${isConnecting ? 'connecting' : ''}`}
      style={{
        left: unit.position.x,
        top: unit.position.y,
        backgroundColor: unit.color,
        borderColor: isSelected ? '#2c3e50' : unit.color,
      }}
      onClick={onSelect}
      onDoubleClick={handleDoubleClick}
    >
      <div className="node-header">
        <span className="node-icon">{unit.icon}</span>
        <div className="node-info">
          <div className="node-name">{unit.name}</div>
          <div className="node-type">{getNodeTypeName(unit.type)}</div>
        </div>
        <button 
          className="node-delete"
          onClick={(e) => {
            e.stopPropagation();
            handleDelete();
          }}
        >
          ×
        </button>
      </div>
      
      <div className="node-params">
        {Object.entries(unit.parameters).slice(0, 3).map(([key, value]) => (
          <div key={key} className="param-item">
            <span className="param-key">{key}:</span>
            <span className="param-value">{value.toFixed(2)}</span>
          </div>
        ))}
        {Object.keys(unit.parameters).length > 3 && (
          <div className="param-more">
            +{Object.keys(unit.parameters).length - 3} más
          </div>
        )}
      </div>

      <div className="node-ports">
        <div className="port input-port"></div>
        <div className="port output-port"></div>
      </div>

      {isConnecting && (
        <div className="connection-indicator">
          Conectando...
        </div>
      )}
    </div>
  );
};

export default ProcessNode;