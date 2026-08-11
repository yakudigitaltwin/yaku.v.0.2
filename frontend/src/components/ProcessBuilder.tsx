import React, { useState, useCallback, useRef } from 'react';
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import ProcessNode from './ProcessNode';
import PropertiesPanel from './PropertiesPanel';
import ConnectionLine from './ConnectionLine';
import { ProcessUnit, Connection } from '../types/process';

interface ProcessBuilderProps {
  onSimulate: (units: ProcessUnit[], connections: Connection[]) => void;
}

interface PaletteItem {
  type: string;
  name: string;
  icon: string;
  color: string;
}

const PALETTE_ITEMS: PaletteItem[] = [
  { type: 'source', name: 'Fuente', icon: '💧', color: '#3498db' },
  { type: 'rapid_mix', name: 'Coagulación', icon: '⚗', color: '#e74c3c' },
  { type: 'flocculation', name: 'Floculación', icon: '🌊', color: '#f39c12' },
  { type: 'sedimentation', name: 'Sedimentación', icon: '🏞', color: '#27ae60' },
  { type: 'filtration', name: 'Filtración', icon: '🔬', color: '#9b59b6' },
  { type: 'disinfection', name: 'Desinfección', icon: '🧪', color: '#1abc9c' },
  { type: 'tank', name: 'Tanque', icon: '💧', color: '#34495e' },
];

interface Position {
  x: number;
  y: number;
}

export default function ProcessBuilder({ onSimulate }: ProcessBuilderProps) {
  const [units, setUnits] = useState<ProcessUnit[]>([]);
  const [connections, setConnections] = useState<Connection[]>([]);
  const [selectedUnit, setSelectedUnit] = useState<ProcessUnit | null>(null);
  const [draggingItem, setDraggingItem] = useState<PaletteItem | null>(null);
  const canvasRef = useRef<HTMLDivElement>(null);

  const addUnit = useCallback((item: PaletteItem, position: Position) => {
    const newUnit: ProcessUnit = {
      id: `${item.type}-${Date.now()}`,
      type: item.type,
      name: `${item.name} ${units.filter(u => u.type === item.type).length + 1}`,
      position,
      parameters: getDefaultParameters(item.type),
      icon: item.icon,
      color: item.color,
    };
    setUnits(prev => [...prev, newUnit]);
  }, [units]);

  const updateUnit = useCallback((updatedUnit: ProcessUnit) => {
    setUnits(prev => prev.map(unit => 
      unit.id === updatedUnit.id ? updatedUnit : unit
    ));
    setSelectedUnit(updatedUnit);
  }, []);

  const deleteUnit = useCallback((unitId: string) => {
    setUnits(prev => prev.filter(unit => unit.id !== unitId));
    setConnections(prev => prev.filter(conn => 
      conn.source !== unitId && conn.target !== unitId
    ));
    setSelectedUnit(null);
  }, []);

  const addConnection = useCallback((sourceId: string, targetId: string) => {
    // Check if connection already exists
    const exists = connections.some(conn => 
      conn.source === sourceId && conn.target === targetId
    );
    
    if (!exists && sourceId !== targetId) {
      setConnections(prev => [...prev, { source: sourceId, target: targetId }]);
    }
  }, [connections]);

  const validateFlowsheet = useCallback(() => {
    // Basic validation: must have source and proper connections
    const hasSource = units.some(u => u.type === 'source');
    const hasSink = units.some(u => u.type === 'tank' || units.some(u2 => 
      connections.some(conn => conn.source === u.id && conn.target === u2.id)
    ));
    
    return {
      isValid: hasSource && units.length > 1,
      errors: !hasSource ? ['Debe tener una fuente de agua'] : 
               units.length <= 1 ? ['Debe tener al menos dos unidades'] : []
    };
  }, [units, connections]);

  const handleSimulate = useCallback(() => {
    const validation = validateFlowsheet();
    if (validation.isValid) {
      onSimulate(units, connections);
    } else {
      alert(`Flowsheet inválido: ${validation.errors.join(', ')}`);
    }
  }, [units, connections, onSimulate, validateFlowsheet]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    if (!draggingItem || !canvasRef.current) return;

    const rect = canvasRef.current.getBoundingClientRect();
    const position = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    };

    addUnit(draggingItem, position);
    setDraggingItem(null);
  }, [draggingItem, addUnit]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
  }, []);

  return (
    <div className="process-builder">
      <div className="palette-section">
        <h3>PALETA</h3>
        <div className="palette">
          {PALETTE_ITEMS.map(item => (
            <div
              key={item.type}
              className="palette-item"
              draggable
              onDragStart={() => setDraggingItem(item)}
              style={{ backgroundColor: item.color }}
            >
              <span className="palette-icon">{item.icon}</span>
              <span className="palette-name">{item.name}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="canvas-section">
        <div className="toolbar">
          <h1>YAKU PROCESS BUILDER</h1>
          <button className="primary" onClick={handleSimulate}>
            Ejecutar Simulación
          </button>
        </div>
        
        <div
          ref={canvasRef}
          className="canvas"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          {/* Connection lines */}
          {connections.map((conn, index) => {
            const sourceUnit = units.find(u => u.id === conn.source);
            const targetUnit = units.find(u => u.id === conn.target);
            
            if (!sourceUnit || !targetUnit) return null;
            
            return (
              <ConnectionLine
                key={index}
                source={sourceUnit}
                target={targetUnit}
              />
            );
          })}
          
          {/* Process nodes */}
          {units.map(unit => (
            <ProcessNode
              key={unit.id}
              unit={unit}
              isSelected={selectedUnit?.id === unit.id}
              onSelect={() => setSelectedUnit(unit)}
              onUpdate={updateUnit}
              onDelete={deleteUnit}
              onConnection={(targetId) => {
                if (selectedUnit && selectedUnit.id !== targetId) {
                  addConnection(selectedUnit.id, targetId);
                }
              }}
            />
          ))}
        </div>
      </div>

      <PropertiesPanel
        unit={selectedUnit}
        onUpdate={updateUnit}
        onClose={() => setSelectedUnit(null)}
      />
    </div>
  );
}

function getDefaultParameters(type: string): Record<string, number> {
  switch (type) {
    case 'source':
      return { Q_m3_s: 0.5, turbidity_ntu: 20, pH: 7.2 };
    case 'rapid_mix':
      return { Q_m3_s: 0.5, volume_m3: 30, G_s: 60, coagulant_mg_l: 25 };
    case 'flocculation':
      return { Q_m3_s: 0.5, volume_m3: 750, G_s: 30 };
    case 'sedimentation':
      return { Q_m3_s: 0.5, area_m2: 1500, depth_m: 4 };
    case 'filtration':
      return { Q_m3_s: 0.5, area_m2: 250, headloss_m: 2 };
    case 'disinfection':
      return { Q_m3_s: 0.5, volume_m3: 900, chlorine_mg_l: 1.5 };
    case 'tank':
      return { Q_m3_s: 0.5, volume_m3: 100 };
    default:
      return {};
  }
}