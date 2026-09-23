# CFD con FreeCAD + CFDOF — Ejemplo: Tanque de descarga (vaciado)

Ejemplo educativo de simulación CFD dentro del proyecto **Yaku-Digital Twin**
usando [CFDOF](https://github.com/CFDOF/CFDOF), el módulo de Dinámica de
Fluidos Computacional para FreeCAD 1.0+ basado en OpenFOAM.

## Archivo

- `tanque_descarga_cfdof.py` — script Python paramétrico que se ejecuta en la
  consola de FreeCAD y genera:
  1. **Geometría**: tanque cilíndrico vertical (D=200 mm, H=300 mm) con orificio
     de drenaje 20×20 mm en el fondo, dentro de un dominio CFD de 400×400×600 mm.
  2. **Regiones de frontera** clasificadas automáticamente por caras
     (`inlet_aire`, `outlet_drenaje`, `walls_tanque`, `defaultFaces`).
  3. **Condiciones de contorno** para el solver multiphasico `interFoam`
     (agua + aire, superficie libre VOF): entrada de aire superior a presión
     atmosférica, descarga inferior, paredes no-slip con ángulo de contacto.
  4. **Física**: agua (ρ=1000, ν=1e-6), aire (ρ=1, ν=1.5e-5), g=(0,0,-9.81),
     20 s de vaciado, Δt adaptativo con Co < 0.5.
  5. **Malla**: tamaño base 10 mm + cajas de refinamiento alrededor del drenaje
     y del frente libre (objetos visibles en 3D para usar como RegionMN).
  6. **Fragmentos de diccionarios OpenFOAM** (`0/U`, `0/p_rgh`, `0/alpha.water`,
     `setFieldsDict`) listos por si hay que copiarlos a mano.

## Requisitos

- FreeCAD 1.0 o superior
- Addon **CFDOF** (menú *Herramientas → Addon Manager → "CFD"*)
- OpenFOAM instalado y accesible desde CFDOF

## Uso rápido

```text
1. FreeCAD → menú CFD → New case...  (Incompressible → Multiphase, interFoam)
2. Ver → Panes → Consola Python, y ejecutar:
   exec(open("/workspace/cad/freecad/tanque_descarga_cfdof.py").read())
3. Seguir las instrucciones impresas: asignar caras, crear BCs, generar malla.
4. Write case → Run → Read results; animar alpha.water.
```

## Validación

El caudal de descarga debe compararse con la ley de Torricelli:

    Q(t) = Cd · A_orificio · √(2·g·h(t)),   Cd ≈ 0.60–0.62

> Modelo de ejemplo educativo: validar malla/paso temporal antes de usarlo
> para diseño real de una PTAP.
