# -*- coding: utf-8 -*-
"""
Ejemplo FreeCAD + CFDOF (OpenFOAM): TANQUE DE DESCARGA / VACIADO
================================================================

Simula el drenaje (vaciado) de un tanque cilíndrico vertical con una boca
de salida en el fondo. El aire entra por la parte superior y el agua sale
por el orificio inferior: problema bifásico agua+aire con superficie libre
que CFDOF resuelve con el solver `interFoam` (método VOF).

Geometría (unidades FreeCAD = mm; OpenFOAM usa metros vía escala del caso):
    - Tanque:   cilindro D = 200 mm, H = 300 mm, espesor pared 10 mm
    - Nivel inicial de agua: 250 mm (~75 % de llenado)
    - Drenaje:  orificio cuadrado 20 x 20 mm centrado en el fondo
    - Dominio CFD: caja 400 x 400 x 600 mm que envuelve el tanque

CÓMO USARLO
-----------
1) Instala CFDOF: menú Herramientas -> Addon Manager -> busca "CFD"
   (FreeCAD 1.0+, con OpenFOAM instalado y accesible).
2) Menú CFD -> New case... : crea una carpeta de caso vacía
   (p. ej. ~/tanque_descarga), tipo "Incompressible -> Multiphase",
   solver interFoam. Deja la ventana del caso abierta.
3) Abre la consola Python de FreeCAD (Ver -> Panes -> Consola Python) y ejecuta:
       exec(open("/workspace/cad/freecad/tanque_descarga_cfdof.py").read())
   El script genera la geometría paramétrica (Dominio, SolidoTanque,
   AguaInicial, cajas de refinamiento de malla) e intenta configurar el
   caso; para lo que la API no exponga, imprime en consola los valores
   exactos que debes poner en el panel de propiedades.
4) En el panel CFD del caso: asigna las caras a cada región (inlet_aire,
   outlet_drenaje, walls_tanque), pulsa "Write case", genera malla y
   "Run". Carga resultados con "Read results" y anima alpha.water.

VALIDACIÓN ANALÍTICA (Torricelli) para comparar el caudal simulado:
    Q(t) = Cd * A_orificio * sqrt(2 g h(t)),   Cd ~ 0.60 - 0.62

Los valores son de ejemplo educativo: refina malla y timestep (Co < 0.5)
antes de usar los resultados para diseño real.

Autor: ejemplo para Yaku-Digital Twin (PTAP) — septiembre 2026
"""

import FreeCAD as App
import Part

try:
    import CFDObj  # noqa: F401  (módulo principal de CFDOF)
    HAVE_CFDOF = True
except ImportError:
    HAVE_CFDOF = False
    print("[ADVERTENCIA] No se pudo importar CFDObj: CFDOF parece no estar")
    print("              instalado. Se generará solo la geometría paramétrica.")

# ----------------------------------------------------------------------
# 0. Parámetros del problema (edítalos aquí)
# ----------------------------------------------------------------------
TANQUE_D_EXT   = 200.0     # mm, diámetro exterior del tanque
TANQUE_H       = 300.0     # mm, altura del tanque
ESPESOR_PARED  = 10.0      # mm, espesor de pared y fondo
NIVEL_AGUA_INI = 250.0     # mm, nivel inicial de agua medido desde el fondo
DRENAGE_LADO   = 20.0      # mm, lado del orificio cuadrado de drenaje

DOM_X, DOM_Y, DOM_Z = 400.0, 400.0, 600.0   # mm, dominio computacional

G          = -9.81         # m/s^2 (gravedad, eje Z hacia abajo)
RHO_AGUA   = 1000.0        # kg/m3
NU_AGUA    = 1.0e-6        # m2/s, viscosidad cinemática del agua
RHO_AIRE   = 1.0           # kg/m3
NU_AIRE    = 1.5e-5        # m2/s
T_FINAL    = 20.0          # s, tiempo simulado de vaciado
WRITE_EVERY = 0.5          # s, intervalo de volcado de resultados
DELTA_T    = 0.001         # s, timestep inicial (adjustTimeStep = yes)


# ----------------------------------------------------------------------
# 1. Documento y geometría paramétrica
# ----------------------------------------------------------------------
DOC_NAME = "TanqueDescargaCFDOF"
doc = (App.getDocument(DOC_NAME)
       if DOC_NAME in App.listDocuments()
       else App.newDocument(DOC_NAME))


def solido_tanque():
    """Cuerpo sólido de pared + fondo del tanque, con orificio de drenaje."""
    r_ext = TANQUE_D_EXT / 2.0
    r_int = r_ext - ESPESOR_PARED
    a = DRENAGE_LADO / 2.0
    ext = Part.makeCylinder(r_ext, TANQUE_H)
    cavidad = Part.makeCylinder(r_int, TANQUE_H - ESPESOR_PARED,
                                App.Vector(0, 0, ESPESOR_PARED))
    agujero = Part.makeBox(2 * a, 2 * a, ESPESOR_PARED + 2.0,
                           App.Vector(-a, -a, -1.0))
    return ext.cut(cavidad).cut(agujero)


def volumen_agua_inicial():
    """Volumen de agua contenido en el tanque al inicio (con canal abierto)."""
    r_int = TANQUE_D_EXT / 2.0 - ESPESOR_PARED
    h_agua = NIVEL_AGUA_INI - ESPESOR_PARED
    a = DRENAGE_LADO / 2.0
    agua = Part.makeCylinder(r_int, h_agua, App.Vector(0, 0, ESPESOR_PARED))
    conducto = Part.makeBox(2 * a, 2 * a, ESPESOR_PARED,
                            App.Vector(-a, -a, 0.0))
    return agua.fuse(conducto)


def crear_geometria():
    """Crea/actualiza los objetos Part::Feature del documento."""
    for nombre in ("Dominio", "SolidoTanque", "AguaInicial"):
        if doc.getObject(nombre):
            doc.removeObject(nombre)

    tanque = solido_tanque()
    agua = volumen_agua_inicial()
    caja = Part.makeBox(DOM_X, DOM_Y, DOM_Z,
                        App.Vector(-DOM_X / 2.0, -DOM_Y / 2.0, 0.0))
    dominio = caja.cut(tanque)   # fluido: interior + exterior del tanque

    objs = {}
    for nombre, shape in (("Dominio", dominio),
                          ("SolidoTanque", tanque),
                          ("AguaInicial", agua)):
        o = doc.addObject("Part::Feature", nombre)
        o.Shape = shape
        objs[nombre] = o

    doc.recompute()
    print("[OK] Geometría creada: Dominio (fluido), SolidoTanque (walls),"
          " AguaInicial (campo alpha)")
    return objs


objs = crear_geometria()


# ----------------------------------------------------------------------
# 2. Regiones de frontera (caras del Dominio)
# ----------------------------------------------------------------------
EPS = 1e-6


def _hypot_xy(v):
    return (v.x ** 2 + v.y ** 2) ** 0.5


def clasificar_caras(shape):
    """Devuelve dict region -> [índices de cara] (1-based sobre shape.Faces)."""
    regiones = {"inlet_aire": [], "outlet_drenaje": [],
                "walls_tanque": [], "defaultFaces": []}
    r_ext = TANQUE_D_EXT / 2.0
    r_int = r_ext - ESPESOR_PARED
    a = DRENAGE_LADO / 2.0
    for i, cara in enumerate(shape.Faces, start=1):
        c = cara.CenterOfMass
        # Cara superior del dominio (aire entrando)
        if abs(c.z - DOM_Z) < EPS:
            regiones["inlet_aire"].append(i)
        # Boca de drenaje: cara en z=0 dentro del cuadrado del orificio
        elif abs(c.z) < EPS and abs(c.x) <= a + EPS and abs(c.y) <= a + EPS:
            regiones["outlet_drenaje"].append(i)
        # Pared/fondo del tanque: caras a radio ~r_ext o ~r_int, o anillo del fondo
        elif _hypot_xy(c) >= r_int - EPS and _hypot_xy(c) <= r_ext + EPS \
                and c.z <= TANQUE_H + EPS:
            regiones["walls_tanque"].append(i)
        elif abs(c.z - ESPESOR_PARED) < EPS and _hypot_xy(c) <= r_int:
            regiones["walls_tanque"].append(i)   # fondo interior
        else:
            regiones["defaultFaces"].append(i)
    return regiones


regiones = clasificar_caras(objs["Dominio"].Shape)
print("\nClasificación automática de caras del Dominio:")
for reg, idx in regiones.items():
    print(f"  {reg:>15}: caras {idx}")
print("\nEn el panel 'Boundary conditions' de CFDOF, agrupa estas caras con")
print("'Add faces to new object' y nómbralas igual que la región.")


# ----------------------------------------------------------------------
# 3. Caso CFDOF: solver, física y condiciones de contorno
# ----------------------------------------------------------------------
BCs = [
    # (región, campo, tipo OpenFOAM, valor, comentario)
    ("inlet_aire",     "U",           "pressureInletOutletVelocity", "(0 0 0)",
     "entrada libre de aire"),
    ("inlet_aire",     "p_rgh",       "totalPressure",               "0",
     "presión atmosférica relativa"),
    ("inlet_aire",     "alpha.water", "inletOutlet",                 "uniform 0",
     "entra solo aire"),

    ("outlet_drenaje", "U",           "pressureInletOutletVelocity", "(0 0 0)",
     "salida de agua / posible entrada de aire"),
    ("outlet_drenaje", "p_rgh",       "totalPressure",               "0",
     "descarga a atmósfera"),
    ("outlet_drenaje", "alpha.water", "inletOutlet",                 "uniform 1",
     "fluido saliente: agua"),

    ("walls_tanque",   "U",           "noSlip",                      "-",
     "paredes y fondo del tanque"),
    ("walls_tanque",   "p_rgh",       "fixedFluxPressure",           "uniform 0",
     "pared impermeable"),
    ("walls_tanque",   "alpha.water", "contactAngle",                "90",
     "mojabilidad neutra (ángulo de contacto)"),

    ("defaultFaces",   "U",           "slip",                        "-",
     "resto de fronteras externas"),
    ("defaultFaces",   "p_rgh",       "fixedFluxPressure",           "uniform 0", "-"),
    ("defaultFaces",   "alpha.water", "zeroGradient",                "-", "-"),
]

print("\nCondiciones de contorno a crear en el caso (CFD -> Add boundary condition):")
for reg, campo, tipo, valor, desc in BCs:
    print(f"  [{reg:>15}] {campo:<12} {tipo:<28} {valor:<12} # {desc}")

if HAVE_CFDOF:
    case = None
    try:
        casos = App.listObjectsOfType("CFDOF::Case")
        case = casos[0] if casos else None
    except Exception:
        case = None
    if case is None:
        for d in App.listDocuments().values():
            for o in d.Objects:
                if "Case" in o.TypeId and "CFD" in o.TypeId.upper():
                    case = o
                    break
    if case is not None:
        print(f"\n[INFO] Caso CFDOF encontrado: {case.Name}. "
              "Aplicando configuración básica...")
        try:
            case.SolverSelected = "interFoam"
        except Exception:
            print("       -> pon Solver = interFoam manualmente en el panel.")
        try:
            case.AnalysisType = "Multiphase"
        except Exception:
            pass
    else:
        print("\n[INFO] No hay caso CFDOF en este documento: créalo con el menú"
              "\n       CFD -> New case... y vuelve a ejecutar esta sección.")

print(f"""
Parámetros físicos a fijar en el panel Physics del caso:
  phases: waterAir | rhoWater={RHO_AGUA}, nuWater={NU_AGUA:.0e},
          rhoAir={RHO_AIRE}, nuAir={NU_AIRE:.1e} | gravity=(0 0 {G})
  controlDict: startTime 0; endTime {T_FINAL}; deltaT {DELTA_T};
               adjustTimeStep yes; maxCo 0.5; writeInterval {WRITE_EVERY}
  Volumen inicial: usa el objeto 'AguaInicial' como RegionMN/setSet de
  alpha.water (setAlphaFieldByRegion o setSet + setFields en terminal).
""")


# ----------------------------------------------------------------------
# 4. Malla: caja base + regiones de refinamiento (objetos visibles 3D)
# ----------------------------------------------------------------------
REF_BOXES = {
    # nombre: (largo, ancho, alto, posición base)  -- todo en mm
    "RefDrenaje": (60, 60, 80, App.Vector(-30, -30, -40)),  # alrededor del orificio
    "RefFrenteLibre": (TANQUE_D_EXT + 40, TANQUE_D_EXT + 40, 30,
                       App.Vector(-(TANQUE_D_EXT + 40) / 2.0,
                                  -(TANQUE_D_EXT + 40) / 2.0,
                                  NIVEL_AGUA_INI - 15)),    # banda del frente libre
}

for nombre, (lx, ly, lz, pos) in REF_BOXES.items():
    if doc.getObject(nombre):
        doc.removeObject(nombre)
    o = doc.addObject("Part::Feature", nombre)
    o.Shape = Part.makeBox(lx, ly, lz, pos)
    o.ViewObject.Transparency = 70
    o.ViewObject.Visibility = False
doc.recompute()

print("""Malla recomendada (panel Mesh del caso CFDOF):
  Base mesh (BaseMeshSize): 10 mm sobre el dominio 400x400x600 mm
  RegionMN (refinamiento): RefDrenaje -> 2 niveles; RefFrenteLibre -> 1 nivel
  BlendingLayers: 1-2 capas en walls_tanque
  Tras generar: checkMesh sin non-manifold y skewness < 0.9
""")


# ----------------------------------------------------------------------
# 5. Fragmentos de diccionarios OpenFOAM (referencia / copia manual)
# ----------------------------------------------------------------------
OPENFOAM_SNIPPETS = {
"0/U": """
 inlet_aire     { type pressureInletOutletVelocity; value uniform (0 0 0); }
 outlet_drenaje { type pressureInletOutletVelocity; value uniform (0 0 0); }
 walls_tanque   { type noSlip; }
 defaultFaces   { type slip; }
""",
"0/p_rgh": """
 inlet_aire     { type totalPressure; p0 uniform 0; value uniform 0; }
 outlet_drenaje { type totalPressure; p0 uniform 0; value uniform 0; }
 walls_tanque   { type fixedFluxPressure; value uniform 0; }
 defaultFaces   { type fixedFluxPressure; value uniform 0; }
""",
"0/alpha.water": """
 inlet_aire     { type inletOutlet; inletValue uniform 0; value uniform 0; }
 outlet_drenaje { type inletOutlet; inletValue uniform 1; value uniform 1; }
 walls_tanque   { type contactAngle; contactAngle uniform 90; value uniform 1; }
 defaultFaces   { type zeroGradient; }
""",
"system/setFieldsDict (nivel inicial de agua)": """
 defaultFieldValues ( alpha.water 0 );
 regions
 {
     cells
     {
         fieldValues ( boxToCell (-90 -90 0.01) (90 90 %.3f) (alpha.water 1) );
     }
 }
""" % (NIVEL_AGUA_INI * 0.001,),
}

print("Fragmentos OpenFOAM de referencia (por si 'Write case' no los genera):")
for archivo, contenido in OPENFOAM_SNIPPETS.items():
    print(f"\n--- {archivo} ---{contenido}")

print("""
RESUMEN DE PASOS
 1. Ejecuta este script en la consola Python de FreeCAD (geometría lista).
 2. Crea el caso CFDOF (New case -> interFoam) si aún no existe.
 3. Asigna caras -> regiones (tabla de la sección 2).
 4. Crea las BCs de la sección 3 y la física airWater.
 5. Genera malla con las cajas de refinamiento (sección 4).
 6. Write case -> Run -> Read results.
 7. Anima alpha.water: verás el chorro de descarga, el descenso del nivel y
    el vórtice de arrastre de aire final. Compara Q(t) con Torricelli.
""")
