"""Genera el modelo ArchiMate de 3.3 (datos) y exporta las vistas a PNG con Archi.

Uso:  python datos/generar_datos.py
Salida: datos_3_3.archimate y D1..D6 *.png en esta carpeta.
"""
import os, shutil, subprocess, tempfile, uuid, glob
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHI = r"C:\Program Files\Archi\Archi.exe"

TYPE = {
    "business-actor": ("BusinessActor", "business"),
    "business-process": ("BusinessProcess", "business"),
    "application-component": ("ApplicationComponent", "application"),
    "application-interface": ("ApplicationInterface", "application"),
    "application-service": ("ApplicationService", "application"),
    "application-event": ("ApplicationEvent", "application"),
    "application-process": ("ApplicationProcess", "application"),
    "data-object": ("DataObject", "application"),
    "system-software": ("SystemSoftware", "technology"),
    "artifact": ("Artifact", "technology"),
    "node": ("Node", "technology"),
}
RTYPE = {"triggering": "TriggeringRelationship", "access": "AccessRelationship", "serving": "ServingRelationship",
         "assignment": "AssignmentRelationship", "realization": "RealizationRelationship",
         "association": "AssociationRelationship", "composition": "CompositionRelationship",
         "flow": "FlowRelationship"}

def nid(): return "id-" + uuid.uuid4().hex

ELS, RELS, VIEWS = {}, {}, []

def E(key, typ, name):
    if key not in ELS: ELS[key] = dict(id=nid(), type=typ, name=name)
    return ELS[key]

class View:
    def __init__(self, name, file):
        self.id, self.name, self.file = nid(), name, file
        self.D, self.top = {}, []
        VIEWS.append(self)
    def put(self, key, typ, name, x, y, w=170, h=55, parent=None):
        e = E(key, typ, name)
        if parent:  # Archi usa coordenadas relativas al grupo
            px, py = self.D[parent]["b"][:2]; x, y = x - px, y - py
        n = dict(kind="el", id=nid(), el=e, b=(x, y, w, h), children=[], conns=[], style={})
        self.D[key] = n
        (self.D[parent]["children"] if parent else self.top).append(n)
        return n
    def group(self, key, name, x, y, w, h):
        n = dict(kind="group", id=nid(), name=name, b=(x, y, w, h), children=[], conns=[], style={})
        self.D[key] = n; self.top.append(n); return n
    def note(self, text, x, y, w=200, h=40):
        self.top.append(dict(kind="note", id=nid(), text=text, b=(x, y, w, h), children=[], conns=[], style={}))
    def rel(self, rtype, a, b, name="", access=None, via=()):
        rid = (rtype, a, b, name)
        if rid not in RELS:
            RELS[rid] = dict(id=nid(), type=RTYPE[rtype], s=ELS[a]["id"], t=ELS[b]["id"], name=name, access=access)
        def ctr(k):
            x, y, w, h = self.D[k]["b"]; return x + w / 2, y + h / 2
        (sx, sy), (tx, ty) = ctr(a), ctr(b)
        bps = [(int(px - sx), int(py - sy), int(px - tx), int(py - ty)) for px, py in via]
        self.D[a]["conns"].append(dict(id=nid(), s=self.D[a]["id"], t=self.D[b]["id"], rel=RELS[rid]["id"], bps=bps))
    def bold(self, *keys):
        for k in keys: self.D[k]["style"] = {"lineWidth": "3", "fillColor": "#a8d8f0"}

APP = "application-component"
DO = "data-object"
SW = "system-software"
AR = "artifact"
ND = "node"

# ------------------------------------------------------------------ D1 mapa AS-IS
v = View("D1 Mapa de datos AS-IS", "D1_mapa_datos_asis.png")
v.group("g1", "Servidor local (SQL Server)", 20, 20, 460, 190)
v.group("g2", "Archivos y papel", 500, 20, 460, 190)
v.group("g3", "Datos en terceros (SaaS)", 20, 230, 940, 110)
v.put("dPac", DO, "Paciente", 40, 55, 200, 55, "g1")
v.put("dHc", DO, "Historia clínica", 260, 55, 200, 55, "g1")
v.put("dPag", DO, "Pago (base de caja)", 40, 130, 200, 55, "g1")
v.put("dFar", DO, "Inventario y ventas de farmacia", 260, 130, 200, 55, "g1")
v.put("dCitX", DO, "Cita (hoja de Excel)", 520, 55, 200, 55, "g2")
v.put("dVou", DO, "Voucher impreso (hora fija)", 740, 55, 200, 55, "g2")
v.put("dLab", DO, "Resultados de laboratorio (Excel)", 520, 130, 200, 55, "g2")
v.put("dWa", DO, "Mensajes de reserva (WhatsApp)", 740, 130, 200, 55, "g2")
v.put("dFe", DO, "Comprobante electrónico (OSE/PSE)", 40, 265, 220, 55, "g3")
v.put("dCon", DO, "Registros contables", 280, 265, 220, 55, "g3")
v.note("No existe la entidad Turno: la hora de atención solo está impresa en el voucher. No hay datos históricos de espera.", 520, 265, 420, 55)

# ------------------------------------------------------------------ D2 mapa TO-BE
v = View("D2 Mapa de datos TO-BE", "D2_mapa_datos_tobe.png")
v.group("gR", "Datos relacionales", 20, 20, 1180, 270)
v.group("gN", "Datos no relacionales", 20, 310, 1180, 110)
v.group("gA", "Datos analíticos", 20, 440, 1180, 110)
v.put("tPac", DO, "Paciente (maestro)", 40, 55, 180, 50, "gR")
v.put("tMed", DO, "Médico (maestro)", 240, 55, 180, 50, "gR")
v.put("tEsp", DO, "Especialidad (maestro)", 440, 55, 180, 50, "gR")
v.put("tCon", DO, "Consultorio (maestro)", 640, 55, 180, 50, "gR")
v.put("tTar", DO, "Tarifa social (maestro)", 840, 55, 180, 50, "gR")
v.put("tAge", DO, "Agenda médica", 40, 130, 180, 50, "gR")
v.put("tCit", DO, "Cita", 240, 130, 180, 50, "gR")
v.put("tPag", DO, "Pago", 440, 130, 180, 50, "gR")
v.put("tTur", DO, "Turno", 640, 130, 180, 50, "gR")
v.put("tEst", DO, "Estimación de tiempo", 840, 130, 180, 50, "gR")
v.put("tHc", DO, "Historia clínica", 40, 205, 180, 50, "gR")
v.put("tRec", DO, "Receta", 240, 205, 180, 50, "gR")
v.put("tCe", DO, "Comprobante electrónico", 440, 205, 180, 50, "gR")
v.put("nEv", DO, "Evento de consulta (JSON)", 40, 345, 200, 50, "gN")
v.put("nNot", DO, "Registro de notificaciones (JSON)", 260, 345, 220, 50, "gN")
v.put("nRaw", DO, "Archivos crudos del ETL (data lake)", 500, 345, 240, 50, "gN")
v.put("nMod", DO, "Modelo de IA entrenado", 760, 345, 200, 50, "gN")
v.put("aHec", DO, "Hechos de atención y espera", 40, 475, 220, 50, "gA")
v.put("aDim", DO, "Dimensiones: fecha, especialidad, médico, consultorio", 280, 475, 300, 50, "gA")
v.put("aInd", DO, "Indicadores de espera y desfase", 600, 475, 220, 50, "gA")
v.bold("tTur", "tEst", "nEv", "nNot", "nRaw", "nMod", "aHec", "aDim", "aInd")
v.note("Resaltadas: entidades nuevas del TO-BE.", 860, 475, 320, 45)

# ------------------------------------------------------------------ D3 modelo lógico
v = View("D3 Modelo lógico de datos", "D3_modelo_logico.png")
v.put("tPac", DO, "Paciente (maestro)", 20, 220, 170, 55)
v.put("tCit", DO, "Cita", 280, 220, 170, 55)
v.put("tPag", DO, "Pago", 540, 220, 170, 55)
v.put("tTur", DO, "Turno", 800, 220, 170, 55)
v.put("tEst", DO, "Estimación de tiempo", 1060, 220, 170, 55)
v.put("tAge", DO, "Agenda médica", 280, 60, 170, 55)
v.put("tMed", DO, "Médico (maestro)", 20, 60, 170, 55)
v.put("tEsp", DO, "Especialidad (maestro)", 540, 60, 170, 55)
v.put("tCon", DO, "Consultorio (maestro)", 800, 60, 170, 55)
v.put("tTar", DO, "Tarifa social (maestro)", 280, 380, 170, 55)
v.put("tCe", DO, "Comprobante electrónico", 540, 500, 170, 55)
v.put("tHc", DO, "Historia clínica", 20, 380, 170, 55)
v.put("tRec", DO, "Receta", 20, 500, 170, 55)
v.put("nEv", DO, "Evento de consulta (JSON)", 800, 380, 170, 55)
v.put("nNot", DO, "Registro de notificaciones (JSON)", 1060, 380, 170, 55)
for a, b, n in [("tPac", "tCit", "1 : N"), ("tMed", "tAge", "1 : N"), ("tAge", "tCit", "1 : N"), ("tEsp", "tAge", "1 : N"),
                ("tCit", "tPag", "1 : 1"), ("tPag", "tTur", "1 : 1"), ("tCon", "tTur", "1 : N"), ("tTur", "tEst", "1 : N"),
                ("tTar", "tPag", "1 : N"), ("tPag", "tCe", "1 : 1"), ("tPac", "tHc", "1 : 1"), ("tHc", "tRec", "1 : N"),
                ("tTur", "nEv", "1 : N"), ("tTur", "nNot", "1 : N"), ("tEsp", "tCon", "N : M")]:
    v.rel("association", a, b, n)
v.note("Claves: Paciente (DNI), Cita (id_cita), Pago (id_pago), Turno (id_turno). El turno se crea con el pago y se recalcula con cada evento de consulta.", 20, 600, 620, 45)

# ------------------------------------------------------------------ D4 AS-IS ArchiMate
v = View("D4 Modelo de datos AS-IS", "D4_datos_asis.png")
v.put("hc", APP, "Software de gestión de historias clínicas", 20, 20, 200, 55)
v.put("caja", APP, "Módulo de caja", 260, 20, 200, 55)
v.put("far", APP, "Software de farmacia", 500, 20, 200, 55)
v.put("xls", APP, "Agenda de citas en Excel", 740, 20, 200, 55)
v.put("dHc", DO, "Historia clínica", 20, 140, 200, 55)
v.put("dPag", DO, "Pago (base de caja)", 260, 140, 200, 55)
v.put("dFar", DO, "Inventario y ventas de farmacia", 500, 140, 200, 55)
v.put("dCitX", DO, "Cita (hoja de Excel)", 740, 140, 200, 55)
v.put("aHc", AR, "bd_historias", 20, 260, 200, 55)
v.put("aCaj", AR, "bd_caja", 260, 260, 200, 55)
v.put("aFar", AR, "bd_farmacia", 500, 260, 200, 55)
v.put("aXls", AR, "agenda.xlsx", 740, 260, 200, 55)
v.put("sql", SW, "SQL Server (SGBD)", 140, 380, 440, 55)
v.put("srv", ND, "Servidor físico local", 20, 490, 680, 55)
v.put("pc", ND, "PC de admisión", 740, 490, 200, 55)
for a, b in [("hc", "dHc"), ("caja", "dPag"), ("far", "dFar"), ("xls", "dCitX")]:
    v.rel("access", a, b)
for a, b in [("aHc", "dHc"), ("aCaj", "dPag"), ("aFar", "dFar"), ("aXls", "dCitX")]:
    v.rel("realization", a, b)
for a in ["aHc", "aCaj", "aFar"]:
    v.rel("assignment", "sql", a)
v.rel("assignment", "srv", "sql"); v.rel("assignment", "pc", "aXls")
v.note("Una sola instancia, sin réplica ni respaldo automático. Las bases no comparten datos entre sí.", 980, 380, 300, 55)

# ------------------------------------------------------------------ D5 TO-BE ArchiMate
v = View("D5 Modelo de datos TO-BE", "D5_datos_tobe.png")
v.put("tur", APP, "Sistema de citas y turnos", 20, 20, 200, 55)
v.put("hc", APP, "Software de gestión de historias clínicas", 260, 20, 200, 55)
v.put("caja", APP, "Módulo de caja", 500, 20, 200, 55)
v.put("ia", APP, "Motor de IA de estimación", 740, 20, 200, 55)
v.put("dw", APP, "Repositorio analítico y tablero", 980, 20, 200, 55)
v.put("tTur", DO, "Turno, cita, agenda", 20, 140, 200, 55)
v.put("dHc", DO, "Historia clínica", 260, 140, 200, 55)
v.put("dPag2", DO, "Pago", 500, 140, 200, 55)
v.put("nEv", DO, "Eventos y estimaciones (JSON)", 740, 140, 200, 55)
v.put("aHec", DO, "Hechos e indicadores de espera", 980, 140, 200, 55)
v.put("iTur", AR, "Instancia bd_turnos", 20, 260, 200, 55)
v.put("iHc", AR, "Instancia bd_historias", 260, 260, 200, 55)
v.put("iCaj", AR, "Instancia bd_caja", 500, 260, 200, 55)
v.put("iEv", AR, "Contenedor de eventos", 740, 260, 200, 55)
v.put("iDw", AR, "Instancia dw_atencion", 980, 260, 200, 55)
v.put("sAz", SW, "Azure SQL Database (SGBD)", 20, 390, 200, 55)
v.put("sSql", SW, "SQL Server (SGBD local)", 260, 390, 440, 55)
v.put("sCos", SW, "Azure Cosmos DB (SGBD NoSQL)", 740, 390, 200, 55)
v.put("sSyn", SW, "Azure SQL Database (analítico)", 980, 390, 200, 55)
for a, b in [("tur", "tTur"), ("hc", "dHc"), ("caja", "dPag2"), ("ia", "nEv"), ("dw", "aHec")]:
    v.rel("access", a, b)
for a, b in [("iTur", "tTur"), ("iHc", "dHc"), ("iCaj", "dPag2"), ("iEv", "nEv"), ("iDw", "aHec")]:
    v.rel("realization", a, b)
for a, b in [("sAz", "iTur"), ("sSql", "iHc"), ("sSql", "iCaj"), ("sCos", "iEv"), ("sSyn", "iDw")]:
    v.rel("assignment", a, b)
v.bold("tur", "ia", "dw", "tTur", "nEv", "aHec", "iTur", "iEv", "iDw", "sAz", "sCos", "sSyn")
v.note("Cada instancia de base de datos se dibuja fuera de su SGBD y se le asigna. Resaltados: elementos nuevos.", 20, 480, 520, 45)

# ------------------------------------------------------------------ D6 flujo ETL
v = View("D6 Flujo ETL", "D6_flujo_etl.png")
v.put("iHc", AR, "bd_historias (local)", 20, 20, 190, 55)
v.put("iCaj", AR, "bd_caja (local)", 20, 120, 190, 55)
v.put("iTur", AR, "bd_turnos (Azure)", 20, 220, 190, 55)
v.put("iEv", AR, "Contenedor de eventos", 20, 320, 190, 55)
v.put("pE", "application-process", "Extraer (cada noche, 23:00)", 270, 170, 180, 55)
v.put("nRaw", DO, "Archivos crudos (data lake)", 270, 300, 180, 55)
v.put("pT", "application-process", "Transformar: anonimizar, limpiar, calcular desfase", 510, 170, 200, 65)
v.put("pC", "application-process", "Cargar en el modelo estrella", 770, 170, 180, 55)
v.put("iDw", AR, "dw_atencion", 1010, 170, 180, 55)
v.put("tab", APP, "Tablero de indicadores", 1010, 40, 180, 55)
v.put("ia", APP, "Motor de IA (reentrenamiento)", 1010, 300, 180, 55)
for s_ in ["iHc", "iCaj", "iTur", "iEv"]:
    v.rel("flow", s_, "pE")
v.rel("access", "pE", "nRaw"); v.rel("triggering", "pE", "pT"); v.rel("triggering", "pT", "pC")
v.rel("access", "pC", "iDw"); v.rel("flow", "iDw", "tab"); v.rel("flow", "iDw", "ia")
v.note("Se usa el orquestador Azure Data Factory. La transformación quita nombres y diagnósticos: al repositorio solo llegan tiempos, especialidad y consultorio.", 270, 420, 560, 55)

# ------------------------------------------------------------------ XML
ACC = {None: None, "write": None, "read": "1", "access": "2", "readwrite": "3"}
INCOMING = {}

def node_xml(n, ind):
    p = " " * ind
    tc = INCOMING.get(n["id"])
    tcs = f' targetConnections="{" ".join(tc)}"' if tc else ""
    x, y, w, h = n["b"]
    st = "".join(f' {k}="{v}"' for k, v in n["style"].items())
    if n["kind"] == "el":
        head = f'{p}<child xsi:type="archimate:DiagramObject" id="{n["id"]}"{st}{tcs} archimateElement="{n["el"]["id"]}">'
    elif n["kind"] == "group":
        head = f'{p}<child xsi:type="archimate:Group" id="{n["id"]}" name="{escape(n["name"])}">'
    else:
        head = f'{p}<child xsi:type="archimate:Note" id="{n["id"]}" textAlignment="1">'
    out = [head, f'{p}  <bounds x="{x}" y="{y}" width="{w}" height="{h}"/>']
    for c in n["conns"]:
        bp = "".join(f'<bendpoint startX="{a}" startY="{b}" endX="{c_}" endY="{d}"/>' for a, b, c_, d in c["bps"])
        out.append(f'{p}  <sourceConnection xsi:type="archimate:Connection" id="{c["id"]}" source="{c["s"]}" target="{c["t"]}" archimateRelationship="{c["rel"]}">{bp}</sourceConnection>')
    if n["kind"] == "note":
        out.append(f'{p}  <content>{escape(n["text"])}</content>')
    for ch in n["children"]:
        out.append(node_xml(ch, ind + 2))
    out.append(f"{p}</child>")
    return "\n".join(out)

def build():
    def walk(ns):
        for n in ns:
            for c in n["conns"]:
                INCOMING.setdefault(c["t"], []).append(c["id"])
            walk(n["children"])
    for vw in VIEWS: walk(vw.top)
    fold = {"business": [], "application": [], "technology": []}
    for e in ELS.values():
        t, f = TYPE[e["type"]]
        fold[f].append(f'    <element xsi:type="archimate:{t}" name="{escape(e["name"])}" id="{e["id"]}"/>')
    rels = []
    for r in RELS.values():
        a = f' accessType="{ACC[r["access"]]}"' if ACC.get(r["access"]) else ""
        nm = f' name="{escape(r["name"])}"' if r["name"] else ""
        rels.append(f'    <element xsi:type="archimate:{r["type"]}" id="{r["id"]}"{nm} source="{r["s"]}" target="{r["t"]}"{a}/>')
    views = []
    for vw in VIEWS:
        views.append(f'    <element xsi:type="archimate:ArchimateDiagramModel" name="{escape(vw.name)}" id="{vw.id}">')
        for n in vw.top: views.append(node_xml(n, 6))
        views.append("    </element>")
    return "\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<archimate:model xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:archimate="http://www.archimatetool.com/archimate" name="TF G4 - Arquitectura de Datos" id="{nid()}" version="5.0.0">',
        '  <folder name="Strategy" id="%s" type="strategy"/>' % nid(),
        '  <folder name="Business" id="%s" type="business">' % nid(), *fold["business"], "  </folder>",
        '  <folder name="Application" id="%s" type="application">' % nid(), *fold["application"], "  </folder>",
        '  <folder name="Technology &amp; Physical" id="%s" type="technology">' % nid(), *fold["technology"], "  </folder>",
        '  <folder name="Motivation" id="%s" type="motivation"/>' % nid(),
        '  <folder name="Implementation &amp; Migration" id="%s" type="implementation_migration"/>' % nid(),
        '  <folder name="Other" id="%s" type="other"/>' % nid(),
        '  <folder name="Relations" id="%s" type="relations">' % nid(), *rels, "  </folder>",
        '  <folder name="Views" id="%s" type="diagrams">' % nid(), *views, "  </folder>",
        "</archimate:model>", ""])

model_path = os.path.join(HERE, "datos_3_3.archimate")
with open(model_path, "w", encoding="utf-8") as f:
    f.write(build())

rep = tempfile.mkdtemp(prefix="archi_rep_")
subprocess.run([ARCHI, "-application", "com.archimatetool.commandline.app", "-consoleLog", "-nosplash",
                "--loadModel", model_path, "--html.createReport", rep], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for vw in VIEWS:
    hits = glob.glob(os.path.join(rep, "**", vw.id + ".png"), recursive=True)
    if not hits:
        print("SIN IMAGEN:", vw.name); continue
    shutil.copy(hits[0], os.path.join(HERE, vw.file))
    print("OK", vw.file)
shutil.rmtree(rep, ignore_errors=True)
