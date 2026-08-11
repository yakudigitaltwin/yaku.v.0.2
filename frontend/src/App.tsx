import React, { useState } from 'react';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import ProcessBuilder from './components/ProcessBuilder';
import { ProcessUnit, Connection } from './types/process';

const API = "http://localhost:8000/api/v1";

export default function App() {
  const [simulationResults, setSimulationResults] = useState<any>(null);
  const [error, setError] = useState("");

  const handleSimulate = async (units: ProcessUnit[], connections: Connection[]) => {
    try {
      // Convert ProcessUnit format to backend format
      const backendUnits = units.map(unit => ({
        id: unit.id,
        type: unit.type,
        name: unit.name,
        parameters: unit.parameters
      }));

      const response = await fetch(`${API}/classic/design`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          id: "ptap-builder",
          name: "PTAP Process Builder",
          units: backendUnits,
          streams: connections.map(conn => ({
            id: `stream-${conn.source}-${conn.target}`,
            source: conn.source,
            target: conn.target,
            flow_m3_s: 0.5 // Default flow rate
          }))
        })
      });

      if (!response.ok) {
        throw new Error("No se pudo conectar con FastAPI");
      }

      const results = await response.json();
      setSimulationResults(results);
      setError("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error desconocido");
      setSimulationResults(null);
    }
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="app">
        <header className="topbar">
          <strong>YAKU</strong><span>Digital Twin · Classic v0.2</span>
        </header>
        
        {error && <div className="card error" style={{position: 'fixed', top: '70px', right: '20px', zIndex: 1000}}>
          {error}
        </div>}

        <ProcessBuilder onSimulate={handleSimulate} />

        {/* Results panel - shown when simulation is complete */}
        {simulationResults && (
          <div className="results-panel" style={{
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            width: '350px',
            background: 'white',
            border: '1px solid #ddd',
            borderRadius: '8px',
            padding: '16px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            zIndex: 1000,
            maxHeight: '300px',
            overflowY: 'auto'
          }}>
            <h3 style={{margin: '0 0 12px 0'}}>Resultados de Simulación</h3>
            <div style={{fontSize: '12px'}}>
              {Object.entries(simulationResults.units).map(([id, r]: any) => (
                <div key={id} style={{marginBottom: '12px', padding: '8px', background: '#f8f9fa', borderRadius: '4px'}}>
                  <b style={{color: '#333'}}>{id}</b>
                  {Object.entries(r).map(([k,v]) =>
                    <div key={k} style={{display: 'flex', justifyContent: 'space-between', margin: '2px 0'}}>
                      <span style={{color: '#666'}}>{k}:</span>
                      <strong style={{color: '#333'}}>{Number(v).toFixed(3)}</strong>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </DndProvider>
  );
}
