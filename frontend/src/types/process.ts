export interface Position {
  x: number;
  y: number;
}

export interface ProcessUnit {
  id: string;
  type: string;
  name: string;
  position: Position;
  parameters: Record<string, number>;
  icon: string;
  color: string;
}

export interface Connection {
  source: string;
  target: string;
}

export interface PlantData {
  id: string;
  name: string;
  units: ProcessUnit[];
  connections: Connection[];
}