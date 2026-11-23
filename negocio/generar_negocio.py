"""Genera el modelo ArchiMate de 3.1 (negocio) y exporta las vistas a PNG con Archi.

Uso:  python generar_negocio.py
Salida: negocio_3_1.archimate y F1..F7 *.png en esta carpeta.
Las imágenes se obtienen del reporte HTML de Archi (línea de comandos).
"""
import os, shutil, subprocess, tempfile, uuid, glob
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHI = r"C:\Program Files\Archi\Archi.exe"

TYPE = {
    "capability": ("Capability", "strategy"),
    "business-actor": ("BusinessActor", "business"),
    "business-process": ("BusinessProcess", "business"),
    "business-function": ("BusinessFunction", "business"),
    "business-event": ("BusinessEvent", "business"),
    "business-service": ("BusinessService", "business"),
    "business-object": ("BusinessObject", "business"),
}
RTYPE = {"triggering": "TriggeringRelationship", "access": "AccessRelationship", "serving": "ServingRelationship",
         "assignment": "AssignmentRelationship", "realization": "RealizationRelationship",
         "association": "AssociationRelationship", "composition": "CompositionRelationship"}

def nid(): return "id-" + uuid.uuid4().hex

ELS, RELS, VIEWS = {}, {}, []

def E(key, typ, name):
    if key not in ELS: ELS[key] = dict(id=nid(), type=typ, name=name)
    return ELS[key]

class View:
    def __init__(self, name, file):
        self.id, self.name, self.file = nid(), name, file
        self.nodes, self.D, self.top = {}, {}, []
        VIEWS.append(self)
    def _add(self, node, parent):
        (self.D[parent]["children"] if parent else self.top).append(node)
    def put(self, key, typ, name, x, y, w=170, h=55, parent=None):
        e = E(key, typ, name)
        n = dict(kind="el", id=nid(), el=e, b=(x, y, w, h), children=[], conns=[], style={})
        self.D[key] = n; self._add(n, parent); return n
    def group(self, key, name, x, y, w, h):
        n = dict(kind="group", id=nid(), name=name, b=(x, y, w, h), children=[], conns=[], style={})
        self.D[key] = n; self.top.append(n); return n
    def note(self, text, x, y, w=200, h=40):
        self.top.append(dict(kind="note", id=nid(), text=text, b=(x, y, w, h), children=[], conns=[], style={}))
    def rel(self, rtype, a, b, name="", access=None):
        rid = (rtype, a, b, name)
        if rid not in RELS:
            RELS[rid] = dict(id=nid(), type=RTYPE[rtype], s=ELS[a]["id"], t=ELS[b]["id"], name=name, access=access)
        r = RELS[rid]
        self.D[a]["conns"].append(dict(id=nid(), s=self.D[a]["id"], t=self.D[b]["id"], rel=r["id"]))
    def bold(self, key):
        self.D[key]["style"] = {"lineWidth": "3", "fillColor": "#fff2a8"}

# ------------------------------------------------------------------ capacidades
FRONT = [("cn01", "Gestión de citas"), ("cn02", "Gestión de orientación al paciente"), ("cn03", "Gestión de cobros")]
MID_AS = [("cn05", "Gestión de agendas médicas")]
MID_TO = [("cn04", "Gestión de turnos"), ("cn05", "Gestión de agendas médicas"), ("cn06", "Gestión de la información al paciente"), ("cn07", "Gestión del desempeño de la atención")]
CORE = [("cn08", "Atención médica ambulatoria"), ("cn09", "Gestión de apoyo al diagnóstico"), ("cn10", "Gestión farmacéutica"), ("cn11", "Gestión de terapia y rehabilitación"), ("cn12", "Gestión de historias clínicas")]
SOP = [("cn13", "Gestión administrativa"), ("cn14", "Gestión financiera y contable"), ("cn15", "Gestión de recursos humanos"), ("cn16", "Gestión de compras y abastecimiento"), ("cn17", "Gestión de la infraestructura"), ("cn18", "Gestión pastoral y de responsabilidad social")]
NEW = {"cn04", "cn06", "cn07"}

def cap_map(name, file, middle, tobe):
    v = View(name, file)
    y = 20
    for key, label, caps in [("g1", "Front office", FRONT), ("g2", "Middle office", middle), ("g3", "Back office core", CORE), ("g4", "Back office soporte", SOP)]:
        v.group(key, label, 20, y, 1180, 110)
        for i, (k, n) in enumerate(caps):
            v.put(k, "capability", n, 15 + i * 192, 35, 180, 60, parent=key)
            if tobe and k in NEW: v.bold(k)
        y += 130
    if tobe: v.note("Resaltadas: capacidades nuevas del TO-BE.", 20, y, 300, 35)
    else: v.note("La coordinación entre caja y consultorio no es una capacidad: la hace el paciente con el voucher en papel.", 20, y, 520, 40)

cap_map("F1 Mapa de capacidades de negocio AS-IS", "F1_mapa_capacidades_asis.png", MID_AS, False)
cap_map("F2 Mapa de capacidades de negocio TO-BE", "F2_mapa_capacidades_tobe.png", MID_TO, True)

# ------------------------------------------------------------------ F3
v = View("F3 Servicio e información de negocio", "F3_servicio_informacion.png")
v.put("pac", "business-actor", "Paciente", 20, 480, 140, 55)
for i, (k, n) in enumerate([("sn02", "Servicio de gestión de citas"), ("sn03", "Servicio de cobro"), ("sn04", "Servicio de gestión de turnos"),
                             ("sn05", "Servicio de información al paciente"), ("sn06", "Servicio de atención médica"), ("sn08", "Servicio farmacéutico")]):
    v.put(k, "business-service", n, 220 + i * 200, 250, 180, 60)
for k, n, x, y in [("boSol", "Solicitud de atención", 220, 60), ("boCita", "Cita", 420, 60), ("boComp", "Comprobante de pago", 620, 60),
                   ("boTurno", "Turno", 820, 60), ("boRec", "Receta u orden", 1220, 60),
                   ("boAviso", "Aviso de turno", 820, 440), ("boHc", "Historia clínica", 1020, 440)]:
    v.put(k, "business-object", n, x, y, 170, 55)
for s, o, a in [("sn02", "boSol", "read"), ("sn02", "boCita", None), ("sn03", "boCita", "read"), ("sn03", "boComp", None),
                ("sn04", "boComp", "read"), ("sn04", "boTurno", None), ("sn05", "boTurno", "read"), ("sn05", "boAviso", None),
                ("sn06", "boTurno", "read"), ("sn06", "boHc", None), ("sn06", "boRec", None), ("sn08", "boRec", "read")]:
    v.rel("access", s, o, access=a)
for s in ["sn02", "sn03", "sn05", "sn06", "sn08"]:
    v.rel("serving", s, "pac")

# ------------------------------------------------------------------ F4
v = View("F4 Descomposición funcional", "F4_descomposicion_funcional.png")
v.put("fRoot", "business-function", "Atención ambulatoria", 20, 20, 1300, 330)
FN = [("f1", "1. Admisión del paciente", ["Orientar", "Gestionar cita", "Cobrar el servicio"]),
      ("f2", "2. Gestión del flujo de atención", ["Generar turno", "Actualizar turno", "Informar estado del turno", "Llamar al paciente"]),
      ("f3", "3. Atención clínica", ["Atender consulta", "Registrar historia clínica", "Emitir receta u orden"]),
      ("f4", "4. Apoyo al diagnóstico y tratamiento", ["Realizar exámenes", "Dispensar medicamentos", "Brindar terapia"]),
      ("f5", "5. Gestión institucional", ["Monitorear desempeño", "Gestionar personal", "Gestionar compras", "Gestionar finanzas"])]
for i, (k, n, subs) in enumerate(FN):
    v.put(k, "business-function", n, 15 + i * 256, 40, 242, 275, parent="fRoot")
    E("fRoot", "", "")
    RELS[("composition", "fRoot", k, "")] = dict(id=nid(), type=RTYPE["composition"], s=ELS["fRoot"]["id"], t=ELS[k]["id"], name="", access=None)
    for j, s in enumerate(subs):
        kk = f"{k}_{j}"
        v.put(kk, "business-function", s, 16, 40 + j * 55, 206, 45, parent=k)
        RELS[("composition", k, kk, "")] = dict(id=nid(), type=RTYPE["composition"], s=ELS[k]["id"], t=ELS[kk]["id"], name="", access=None)

# ------------------------------------------------------------------ F5
v = View("F5 Ciclo de vida de la atención ambulatoria", "F5_ciclo_de_vida.png")
ST = ["Solicitada", "Agendada", "Pagada", "En espera", "Llamada", "En consulta", "Atendida", "Cerrada o derivada"]
for i, s in enumerate(ST):
    x = 20 + (i % 4) * 220 if i < 4 else 20 + (7 - i) * 220
    y = 60 if i < 4 else 300
    v.put(f"st{i}", "business-event", s, x, y, 170, 55)
    if i: v.rel("triggering", f"st{i-1}", f"st{i}")
v.put("stCambio", "business-event", "Cambio en el avance de la consulta", 450, 480, 210, 55)
v.put("stAct", "business-event", "Turno actualizado", 920, 180, 210, 55)
v.rel("triggering", "st5", "stCambio")
v.rel("triggering", "stCambio", "stAct")
v.rel("triggering", "stAct", "st3")
v.bold("stCambio"); v.bold("stAct")
v.note("Resaltado: bucle nuevo del TO-BE. El turno se recalcula mientras el paciente espera.", 700, 480, 260, 55)

# ------------------------------------------------------------------ F6 AS-IS
v = View("F6 Modelo de negocio AS-IS", "F6_negocio_asis.png")
for k, n, x in [("aPac", "Paciente", 20), ("aRec", "Recepcionista", 285), ("aCaj", "Cajero", 560), ("aEnf", "Enfermera", 800), ("aMed", "Médico", 1040), ("aQf", "Químico-farmacéutico", 1290)]:
    v.put(k, "business-actor", n, x, 20, 150, 55)
v.put("eSol", "business-event", "Solicitud de una consulta", 20, 170, 150, 55)
v.put("pRes", "business-process", "Reservar cita", 200, 170, 140, 55)
v.put("pTri", "business-process", "Realizar triaje", 370, 170, 140, 55)
v.put("pCob", "business-process", "Cobro de pago de cita reservada", 550, 170, 170, 60)
v.put("pRcp", "business-process", "Recepcionar comprobante", 790, 170, 165, 55)
v.put("pEsp", "business-process", "Esperar turno de atención", 790, 320, 165, 55)
v.put("pAte", "business-process", "Atender consulta médica", 1030, 170, 170, 55)
v.put("pDis", "business-process", "Proporcionar medicamentos / recepcionar orden de exámenes", 1270, 170, 210, 65)
v.put("oComp", "business-object", "Comprobante de pago (hora fija)", 550, 320, 170, 55)
v.put("oRec", "business-object", "Receta u orden de exámenes", 1030, 320, 170, 55)
for a, b in [("eSol", "pRes"), ("pRes", "pTri"), ("pTri", "pCob"), ("pCob", "pRcp"), ("pRcp", "pEsp"), ("pRcp", "pAte"), ("pAte", "pDis")]:
    v.rel("triggering", a, b)
v.rel("access", "pCob", "oComp"); v.rel("access", "pRcp", "oComp", access="read"); v.rel("access", "pAte", "oRec")
for a, p in [("aRec", "pRes"), ("aRec", "pTri"), ("aCaj", "pCob"), ("aEnf", "pRcp"), ("aMed", "pAte"), ("aQf", "pDis")]:
    v.rel("assignment", a, p)
v.rel("association", "aPac", "eSol")
v.note("Punto de dolor: el comprobante en papel es el único vínculo entre caja y consultorio y nada recalcula la hora del turno.", 300, 430, 520, 45)

# ------------------------------------------------------------------ F7 TO-BE
# Filas: servicios (arriba), procesos, actores debajo de su proceso, ciclo de actualización abajo.
v = View("F7 Modelo de negocio TO-BE", "F7_negocio_tobe.png")
v.put("aPac", "business-actor", "Paciente", 20, 420, 150, 55)
v.put("sn02", "business-service", "Servicio de gestión de citas", 240, 20, 180, 55)
v.put("sn03", "business-service", "Servicio de cobro", 500, 20, 180, 55)
v.put("sn04", "business-service", "Servicio de gestión de turnos", 760, 20, 180, 55)
v.put("sn06", "business-service", "Servicio de atención médica", 1020, 20, 180, 55)
v.put("eSolA", "business-event", "Solicitud de atención", 20, 160, 150, 55)
v.put("pGc", "business-process", "Gestionar cita", 240, 160, 180, 55)
v.put("pRp", "business-process", "Registrar pago", 500, 160, 180, 55)
v.put("pGt", "business-process", "Gestionar turno", 760, 160, 180, 55)
v.put("pAt", "business-process", "Atender consulta médica", 1020, 160, 180, 55)
v.put("pDm", "business-process", "Dispensar medicamentos", 1280, 160, 180, 55)
v.put("aRec", "business-actor", "Recepcionista", 240, 290, 180, 50)
v.put("aCaj", "business-actor", "Cajero", 500, 290, 180, 50)
v.put("aEnf", "business-actor", "Enfermera", 760, 290, 180, 50)
v.put("aMed", "business-actor", "Médico", 1020, 290, 180, 50)
v.put("aQf", "business-actor", "Químico-farmacéutico", 1280, 290, 180, 50)
v.put("boComp", "business-object", "Comprobante de pago", 500, 420, 180, 50)
v.put("pIt", "business-process", "Informar estado del turno", 760, 560, 180, 55)
v.put("pAct", "business-process", "Actualizar turno", 1020, 560, 180, 55)
v.put("eCam", "business-event", "Cambio en el avance de la consulta", 1280, 560, 200, 55)
v.put("eAct", "business-event", "Turno actualizado", 1020, 690, 180, 55)
v.put("boTurno", "business-object", "Turno", 1020, 420, 180, 50)
v.put("sn05", "business-service", "Servicio de información al paciente", 240, 560, 190, 55)
v.put("boHc", "business-object", "Historia clínica", 1280, 420, 180, 50)
for a, b in [("eSolA", "pGc"), ("pGc", "pRp"), ("pRp", "pGt"), ("pGt", "pAt"), ("pAt", "pDm"),
             ("pAt", "eCam"), ("eCam", "pAct"), ("pAct", "eAct"), ("eAct", "pIt"), ("pGt", "pIt")]:
    v.rel("triggering", a, b)
for p, s_ in [("pGc", "sn02"), ("pRp", "sn03"), ("pGt", "sn04"), ("pIt", "sn05"), ("pAt", "sn06")]:
    v.rel("realization", p, s_)
for a, p in [("aRec", "pGc"), ("aCaj", "pRp"), ("aEnf", "pGt"), ("aEnf", "pIt"), ("aEnf", "pAct"), ("aMed", "pAt"), ("aQf", "pDm")]:
    v.rel("assignment", a, p)
v.rel("serving", "sn05", "aPac")
v.rel("association", "aPac", "eSolA")
v.rel("access", "pRp", "boComp"); v.rel("access", "pAct", "boTurno"); v.rel("access", "pAt", "boHc")
for k in ["pGt", "pAct", "pIt", "eCam", "eAct"]: v.bold(k)
v.note("Resaltados: procesos y eventos nuevos respecto del AS-IS. La enfermera gestiona, actualiza e informa el turno.", 20, 690, 420, 55)

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
        out.append(f'{p}  <sourceConnection xsi:type="archimate:Connection" id="{c["id"]}" source="{c["s"]}" target="{c["t"]}" archimateRelationship="{c["rel"]}"/>')
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
    fold = {"strategy": [], "business": []}
    for e in ELS.values():
        if not e["type"]: continue
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
        f'<archimate:model xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:archimate="http://www.archimatetool.com/archimate" name="TF G4 - Arquitectura de Negocio" id="{nid()}" version="5.0.0">',
        '  <folder name="Strategy" id="%s" type="strategy">' % nid(), *fold["strategy"], "  </folder>",
        '  <folder name="Business" id="%s" type="business">' % nid(), *fold["business"], "  </folder>",
        '  <folder name="Application" id="%s" type="application"/>' % nid(),
        '  <folder name="Technology &amp; Physical" id="%s" type="technology"/>' % nid(),
        '  <folder name="Motivation" id="%s" type="motivation"/>' % nid(),
        '  <folder name="Implementation &amp; Migration" id="%s" type="implementation_migration"/>' % nid(),
        '  <folder name="Other" id="%s" type="other"/>' % nid(),
        '  <folder name="Relations" id="%s" type="relations">' % nid(), *rels, "  </folder>",
        '  <folder name="Views" id="%s" type="diagrams">' % nid(), *views, "  </folder>",
        "</archimate:model>", ""])

model_path = os.path.join(HERE, "negocio_3_1.archimate")
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
