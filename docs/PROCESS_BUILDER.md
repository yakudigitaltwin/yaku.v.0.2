# Yaku Classic v0.2: Process Builder

## Overview

Yaku Classic v0.2 introduces the Process Builder, a drag-and-drop interface that transforms the React application into a true PTAP (Water Treatment Plant) editor. This interface provides an intuitive visual environment for designing, configuring, and simulating water treatment processes.

## Features

### 🎨 Visual Interface
- **Drag-and-drop canvas** for building process flows
- **Visual unit palette** with all PTAP process types
- **Real-time connections** between process units
- **Interactive properties panel** for unit configuration

### 🔧 Process Units
- **Source (Fuente)**: Water input with quality parameters
- **Rapid Mix (Coagulación)**: Coagulation and rapid mixing
- **Flocculation (Floculación)**: Floculation process
- **Sedimentation (Sedimentación)**: Sedimentation tanks
- **Filtration (Filtración)**: Filtration units
- **Disinfection (Desinfección)**: Disinfection process
- **Tank (Tanque)**: Storage tanks

### 🎯 Key Capabilities
- **Unit positioning**: Drag units to desired positions
- **Parameter configuration**: Edit operational parameters
- **Connection management**: Create flow connections between units
- **Validation**: Automatic flowsheet validation
- **Simulation**: Execute simulations from the visual interface

## User Interface

### Layout Structure
```
┌─────────────────────────────────────────────────────────────────┐
│ YAKU PROCESS BUILDER                                            │
├─────────────────────────────────────────────────────────────────┤
│ PALETA                    │ CANVAS                           │
│                           │                                  │
│ 💧 Fuente     │           │                                  │
│ ⚗ Coag.      │           │    ┌─────────────┐               │
│ 🌊 Floc.      │           │    │ 💧 Fuente    │               │
│ 🏞 Sedim.     │───────────►│    │             │               │
│ 🔬 Filtro     │           │    └───────┬─────┘               │
│ 🧪 Cloro      │           │           │                     │
│ 💧 Tanque     │           │    ┌───────▼─────┐               │
│                           │    │ ⚗ Coag.      │               │
│                           │    └─────────────┘               │
│                           │                                  │
│                           │    ┌─────────────┐               │
│                           │    │ 🌊 Floc.     │               │
│                           │    └─────────────┘               │
│                           │                                  │
│                           │    ┌─────────────┐               │
│                           │    │ 🏞 Sedim.    │               │
│                           │    └─────────────┘               │
│                           │                                  │
│                           │    ┌─────────────┐               │
│                           │    │ 🔬 Filtro    │               │
│                           │    └─────────────┘               │
│                           │                                  │
│                           │    ┌─────────────┐               │
│                           │    │ 🧪 Cloro     │               │
│                           │    └─────────────┘               │
│                           │                                  │
│                           │    ┌─────────────┐               │
│                           │    │ 💧 Tanque    │               │
│                           │    └─────────────┘               │
│                           │                                  │
├─────────────────────────────────────────────────────────────────┤
│ PROPERTIES PANEL                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Propiedades de Fuente 1                                     │ │
│ │                                                            │ │
│ │ Información de la unidad                                    │ │
│ │ Tipo: source                                                │ │
│ │ Icono: 💧                                                   │ │
│ │ Color: #3498db                                              │ │
│ │                                                            │ │
│ │ Parámetros operativos                                        │ │
│ │ Caudal (m³/s): [0.50]                                       │ │
│ │ Turbidez (NTU): [20.00]                                     │ │
│ │ pH: [7.20]                                                  │ │
│ │                                                            │ │
│ │                     [Guardar] [Cancelar]                     │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Usage Guide

### 1. Adding Units
1. **Select a unit** from the palette on the left
2. **Drag and drop** it onto the canvas
3. **Position** the unit where you want it to appear
4. **Units are automatically numbered** (e.g., "Fuente 1", "Fuente 2")

### 2. Configuring Units
1. **Click on a unit** to select it
2. **The properties panel** will appear on the right
3. **Edit parameters** such as flow rate, volume, etc.
4. **Click "Guardar"** to save changes
5. **Click "Cancelar"** to discard changes

### 3. Creating Connections
1. **Select a source unit** (click on it)
2. **Drag to a target unit** (hover over the target)
3. **Release** to create the connection
4. **Connections are shown as arrows** between units

### 4. Running Simulations
1. **Ensure your flowsheet is valid** (has source and proper connections)
2. **Click "Ejecutar Simulación"** in the toolbar
3. **Results will appear** in a popup panel at the bottom right
4. **Review calculation results** for each unit

### 5. Managing Units
- **Double-click** on a unit to rename it
- **Click the × button** to delete a unit
- **Drag units** to reposition them on the canvas

## Unit Types and Parameters

### Source (Fuente)
- **Caudal (Q_m3_s)**: Water flow rate in m³/s
- **Turbidez (NTU)**: Turbidity in Nephelometric Turbidity Units
- **pH**: pH value (0-14)

### Rapid Mix (Coagulación)
- **Caudal (Q_m3_s)**: Water flow rate in m³/s
- **Volumen (volume_m3)**: Mixing tank volume in m³
- **Gradiente de velocidad (G_s)**: Velocity gradient in s⁻¹
- **Dosis de coagulante (coagulant_mg_l)**: Coagulant dosage in mg/L

### Flocculation (Floculación)
- **Caudal (Q_m3_s)**: Water flow rate in m³/s
- **Volumen (volume_m3)**: Flocculation basin volume in m³
- **Gradiente de velocidad (G_s)**: Velocity gradient in s⁻¹

### Sedimentation (Sedimentación)
- **Caudal (Q_m3_s)**: Water flow rate in m³/s
- **Área superficial (area_m2)**: Surface area in m²
- **Profundidad (depth_m)**: Water depth in m

### Filtration (Filtración)
- **Caudal (Q_m3_s)**: Water flow rate in m³/s
- **Área del filtro (area_m2)**: Filter area in m²
- **Pérdida de carga (headloss_m)**: Head loss in m

### Disinfection (Desinfección)
- **Caudal (Q_m3_s)**: Water flow rate in m³/s
- **Volumen (volume_m3)**: Disinfection chamber volume in m³
- **Dosis de cloro (chlorine_mg_l)**: Chlorine dosage in mg/L

### Tank (Tanque)
- **Caudal (Q_m3_s)**: Water flow rate in m³/s
- **Volumen (volume_m3)**: Tank volume in m³

## Validation Rules

### Flowsheet Validation
- **Must have at least one source unit**
- **Must have at least two units total**
- **All units must have valid parameters**
- **Connections must form a valid flow path**

### Parameter Validation
- **Flow rates** must be positive (0.01-10 m³/s)
- **Volumes** must be positive (1-10000 m³)
- **Areas** must be positive (1-10000 m²)
- **Chemical dosages** must be non-negative
- **pH values** must be between 0-14

## Simulation Results

When you run a simulation, results are displayed showing:
- **Unit identification** and name
- **Calculated parameters** (detention time, efficiency, etc.)
- **Performance metrics** for each unit type

Results are shown in a popup panel that can be closed by clicking outside of it.

## Keyboard Shortcuts

- **Double-click**: Rename unit
- **Delete key**: Remove selected unit
- **Escape**: Close properties panel
- **Ctrl+Z**: Undo (future implementation)

## Technical Implementation

### Architecture
- **React DnD** for drag-and-drop functionality
- **Canvas-based rendering** for connections
- **State management** with React hooks
- **Responsive design** for different screen sizes

### Integration
- **Backend API** integration for calculations
- **Real-time validation** of flowsheets
- **Parameter synchronization** between frontend and backend

### Performance
- **Optimized rendering** for large flowsheets
- **Efficient connection calculation**
- **Lazy loading** of unit components

## Future Enhancements

### Phase 1 (Current)
- ✅ Basic drag-and-drop functionality
- ✅ Unit connections and flow paths
- ✅ Parameter configuration
- ✅ Simulation execution
- ✅ Results display

### Phase 2 (Planned)
- 🔄 **Undo/Redo functionality**
- 🔄 **Save/Load flowsheets**
- 🔄 **Template library**
- 🔄 **Advanced validation rules**
- 🔄 **Real-time parameter updates**

### Phase 3 (Future)
- 🚀 **AI-assisted design optimization**
- 🚀 **Dynamic simulation visualization**
- 🚀 **Multi-scenario comparison**
- 🚀 **Integration with control systems**
- 🚀 **Mobile app support**

## Troubleshooting

### Common Issues
1. **Units not dropping**: Check if canvas area is accessible
2. **Connections not working**: Ensure units are properly positioned
3. **Parameters not saving**: Verify input values are valid
4. **Simulation failing**: Check flowsheet validation rules

### Browser Compatibility
- **Chrome**: Full support
- **Firefox**: Full support
- **Safari**: Full support
- **Edge**: Full support

### Performance Tips
- **Close unused properties panels**
- **Use reasonable unit counts** (< 50 units)
- **Group related units** for better organization
- **Use templates** for common configurations

## API Documentation

### Process Builder API
The Process Builder integrates with the existing Yaku API:

```typescript
// Simulation execution
POST /api/v1/classic/design
Content-Type: application/json

{
  "id": "ptap-builder",
  "name": "PTAP Process Builder",
  "units": [...],
  "streams": [...]
}
```

### Response Format
```json
{
  "plant_id": "ptap-builder",
  "plant_name": "PTAP Process Builder",
  "units": {
    "unit_id": {
      "parameter1": value1,
      "parameter2": value2,
      ...
    }
  }
}
```

## Support and Feedback

For support, questions, or feature requests:
- **Documentation**: Check this guide and existing API docs
- **GitHub Issues**: Report bugs and request features
- **Community**: Join discussions in the Yaku repository

---

*Yaku Classic v0.2: Process Builder - Making PTAP design intuitive and accessible*