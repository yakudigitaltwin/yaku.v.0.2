import React from 'react';
import { ProcessUnit } from '../types/process';

interface ConnectionLineProps {
  source: ProcessUnit;
  target: ProcessUnit;
}

const ConnectionLine: React.FC<ConnectionLineProps> = ({ source, target }) => {
  // Calculate connection points (ports)
  const sourcePort = {
    x: source.position.x + 120, // Right side of the node
    y: source.position.y + 40, // Center vertically
  };

  const targetPort = {
    x: target.position.x, // Left side of the node
    y: target.position.y + 40, // Center vertically
  };

  // Calculate the path for the connection line
  const path = `M ${sourcePort.x} ${sourcePort.y} L ${targetPort.x} ${targetPort.y}`;

  return (
    <svg className="connection-svg" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 1 }}>
      <defs>
        <marker
          id="arrowhead"
          markerWidth="10"
          markerHeight="7"
          refX="9"
          refY="3.5"
          orient="auto"
        >
          <polygon
            points="0 0, 10 3.5, 0 7"
            fill="#666"
          />
        </marker>
      </defs>
      
      <path
        d={path}
        stroke="#666"
        strokeWidth="2"
        fill="none"
        markerEnd="url(#arrowhead)"
      />
      
      {/* Connection point circles */}
      <circle
        cx={sourcePort.x}
        cy={sourcePort.y}
        r="4"
        fill="#4CAF50"
        stroke="#2E7D32"
        strokeWidth="2"
      />
      <circle
        cx={targetPort.x}
        cy={targetPort.y}
        r="4"
        fill="#2196F3"
        stroke="#1565C0"
        strokeWidth="2"
      />
    </svg>
  );
};

export default ConnectionLine;