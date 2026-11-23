"""Genera el modelo ArchiMate de 3.2 (aplicaciones) y exporta las vistas a PNG con Archi.

Uso:  python aplicaciones/generar_aplicaciones.py
Salida: aplicaciones_3_2.archimate y A1..A5 *.png en esta carpeta.
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

# ------------------------------------------------------------------ A1 mapa AS-IS
v = View("A1 Mapa de aplicaciones AS-IS", "A1_mapa_aplicaciones_asis.png")
v.group("gF", "Front office", 20, 20, 900, 110)
v.group("gM", "Middle office", 20, 150, 900, 110)
v.group("gB", "Back office", 20, 280, 900, 190)
v.put("web", APP, "Página web con formulario de reserva", 40, 55, 190, 55)
v.put("wa", APP, "WhatsApp Business (app básica)", 250, 55, 190, 55)
v.put("caja", APP, "Módulo de caja", 460, 55, 190, 55)
v.put("fe", APP, "Facturación electrónica (OSE/PSE, SaaS)", 670, 55, 220, 55)
v.put("xls", APP, "Agenda de citas en Excel", 40, 185, 190, 55)
v.note("Sin aplicación de turnos ni integración: la hora de atención viaja en el voucher impreso.", 260, 185, 420, 55)
v.put("hc", APP, "Software de gestión de historias clínicas (SQL Server)", 40, 315, 220, 60)
v.put("far", APP, "Software de farmacia", 280, 315, 190, 55)
v.put("lab", APP, "Laboratorio en Excel", 490, 315, 190, 55)
v.put("cont", APP, "Software contable (tercerizado, SaaS)", 700, 315, 200, 55)
v.put("off", APP, "Office y correo", 40, 395, 190, 55)

# ------------------------------------------------------------------ A2 mapa TO-BE
v = View("A2 Mapa de aplicaciones TO-BE", "A2_mapa_aplicaciones_tobe.png")
v.group("gF", "Front office", 20, 20, 1120, 110)
v.group("gM", "Middle office", 20, 150, 1120, 190)
v.group("gB", "Back office", 20, 360, 1120, 190)
v.put("portal", APP, "Portal web de citas", 40, 55, 190, 55)
v.put("waapi", APP, "Plataforma de notificaciones (WhatsApp Business API, SaaS)", 250, 55, 240, 55)
v.put("pant", APP, "Pantallas de turno", 510, 55, 180, 55)
v.put("caja", APP, "Módulo de caja", 710, 55, 180, 55)
v.put("fe", APP, "Facturación electrónica (OSE/PSE, SaaS)", 910, 55, 210, 55)
v.put("esb", APP, "Bus de servicios empresariales (ESB)", 40, 185, 1080, 45)
v.put("tur", APP, "Sistema de citas y turnos (Azure)", 40, 255, 220, 55)
v.put("ia", APP, "Motor de IA de estimación de tiempos (Azure)", 280, 255, 240, 55)
v.put("etl", APP, "Procesos ETL", 540, 255, 160, 55)
v.put("dw", APP, "Repositorio analítico y tablero de indicadores", 720, 255, 240, 55)
v.put("hc", APP, "Software de gestión de historias clínicas (SQL Server)", 40, 395, 230, 60)
v.put("far", APP, "Software de farmacia", 290, 395, 180, 55)
v.put("lab", APP, "Laboratorio en Excel", 490, 395, 180, 55)
v.put("cont", APP, "Software contable (tercerizado, SaaS)", 690, 395, 210, 55)
v.put("off", APP, "Office y correo", 920, 395, 180, 55)
v.bold("portal", "waapi", "pant", "esb", "tur", "ia", "etl", "dw")
v.note("Resaltadas: aplicaciones nuevas. El portal web de citas reemplaza al formulario y el sistema de citas y turnos a la agenda en Excel.", 40, 475, 600, 45)

# ------------------------------------------------------------------ A3 modelo AS-IS
v = View("A3 Modelo de aplicaciones AS-IS", "A3_aplicaciones_asis.png")
for k, n, x in [("bRes", "Reservar cita", 20), ("bCob", "Cobro de pago de cita reservada", 250),
                ("bRcp", "Recepcionar comprobante", 480), ("bAte", "Atender consulta médica", 710), ("bDis", "Proporcionar medicamentos", 940)]:
    v.put(k, "business-process", n, x, 20, 190, 55)
for k, n, x in [("sAg", "Registro manual de citas", 20), ("sCob", "Registro de cobro", 250),
                ("sHc", "Gestión de historia clínica", 710), ("sFar", "Venta de medicamentos", 940)]:
    v.put(k, "application-service", n, x, 140, 190, 55)
v.put("sFe", "application-service", "Emisión de comprobante electrónico", 480, 140, 190, 55)
v.put("xls", APP, "Agenda de citas en Excel", 20, 260, 190, 55)
v.put("wa", APP, "WhatsApp Business (app básica)", 250, 500, 190, 55)
v.put("web", APP, "Página web con formulario", 20, 500, 190, 55)
v.put("caja", APP, "Módulo de caja", 250, 260, 190, 55)
v.put("fe", APP, "Facturación electrónica (OSE/PSE)", 480, 260, 190, 55)
v.put("hc", APP, "Software de gestión de historias clínicas", 710, 260, 190, 55)
v.put("far", APP, "Software de farmacia", 940, 260, 190, 55)
v.put("dVou", "data-object", "Comprobante impreso (hora fija)", 250, 380, 190, 55)
v.put("dHc", "data-object", "Historia clínica", 710, 380, 190, 55)
v.put("dCita", "data-object", "Cita (hoja de cálculo)", 20, 380, 190, 55)
v.rel("realization", "xls", "sAg"); v.rel("realization", "caja", "sCob"); v.rel("realization", "fe", "sFe")
v.rel("realization", "hc", "sHc"); v.rel("realization", "far", "sFar")
v.rel("serving", "sAg", "bRes"); v.rel("serving", "sCob", "bCob"); v.rel("serving", "sFe", "bCob")
v.rel("serving", "sHc", "bAte"); v.rel("serving", "sFar", "bDis")
v.rel("flow", "web", "wa"); v.rel("access", "xls", "dCita")
v.rel("flow", "caja", "fe"); v.rel("access", "caja", "dVou")
v.rel("access", "hc", "dHc")
v.note("Punto de dolor: ningún servicio de aplicación sirve a Recepcionar comprobante; entre caja y consultorio no hay flujo de datos, solo el papel.", 480, 500, 420, 55)

# ------------------------------------------------------------------ A4 modelo TO-BE
v = View("A4 Modelo de aplicaciones TO-BE", "A4_aplicaciones_tobe.png")
X = [20, 240, 460, 680, 900, 1120, 1340]
for k, n, x in [("bGc", "Gestionar cita", X[0]), ("bRp", "Registrar pago", X[1]), ("bGt", "Gestionar turno", X[2]),
                ("bAct", "Actualizar turno", X[3]), ("bIt", "Informar estado del turno", X[4]), ("bAte", "Atender consulta médica", X[6])]:
    v.put(k, "business-process", n, x, 20, 180, 55)
for k, n, x in [("sCit", "Registro de citas", X[0]), ("sPag", "Registro de pagos", X[1]), ("sTur", "Generación de turnos", X[2]),
                ("sEst", "Estimación de tiempo de atención", X[3]), ("sNot", "Notificación al paciente", X[4]),
                ("sVis", "Visualización de turnos", X[5]), ("sHc", "Gestión de historia clínica", X[6])]:
    v.put(k, "application-service", n, x, 140, 180, 55)
for k, n, x in [("portal", "Portal web de citas", X[0]), ("caja", "Módulo de caja", X[1]), ("tur", "Sistema de citas y turnos", X[2]),
                ("ia", "Motor de IA de estimación", X[3]), ("waapi", "Plataforma de notificaciones (WhatsApp API)", X[4]),
                ("pant", "Pantallas de turno", X[5]), ("hc", "Software de gestión de historias clínicas", X[6])]:
    v.put(k, APP, n, x, 280, 180, 60)
v.put("esb", APP, "Bus de servicios empresariales (ESB)", 20, 400, 1500, 45)
for c_, s_ in [("portal", "sCit"), ("caja", "sPag"), ("tur", "sTur"), ("ia", "sEst"), ("waapi", "sNot"), ("pant", "sVis"), ("hc", "sHc")]:
    v.rel("realization", c_, s_)
for s_, b in [("sCit", "bGc"), ("sPag", "bRp"), ("sTur", "bGt"), ("sEst", "bAct"), ("sNot", "bIt"), ("sVis", "bIt"), ("sHc", "bAte")]:
    v.rel("serving", s_, b)
for c_ in ["portal", "caja", "tur", "ia", "waapi", "pant", "hc"]:
    v.rel("serving", "esb", c_)
v.bold("tur", "ia", "waapi", "pant", "esb", "portal", "sTur", "sEst", "sNot", "sVis")
v.note("Resaltados: aplicaciones y servicios nuevos. Todas las aplicaciones se comunican a través del ESB; no hay conexiones punto a punto.", 20, 470, 600, 45)

# ------------------------------------------------------------------ A5 integración
v = View("A5 Integración ESB y ETL", "A5_integracion_esb_etl.png")
v.put("caja", APP, "Módulo de caja", 20, 40, 190, 55)
v.put("hc", APP, "Software de gestión de historias clínicas", 20, 170, 190, 60)
v.put("portal", APP, "Portal web de citas", 20, 300, 190, 55)
v.put("eP", "application-event", "Pago registrado", 270, 40, 170, 55)
v.put("eC", "application-event", "Consulta iniciada / finalizada", 270, 170, 170, 60)
v.put("eR", "application-event", "Cita registrada", 270, 300, 170, 55)
v.put("esb", APP, "Bus de servicios empresariales (ESB)", 490, 40, 190, 315)
v.put("iTur", "application-interface", "API de turnos (REST/JSON)", 730, 40, 190, 55)
v.put("tur", APP, "Sistema de citas y turnos", 980, 40, 190, 55)
v.put("ia", APP, "Motor de IA de estimación", 730, 170, 190, 55)
v.put("iWa", "application-interface", "API de mensajería (HTTPS)", 1230, 40, 190, 55)
v.put("waapi", APP, "Plataforma de notificaciones", 1230, 170, 190, 55)
v.put("pant", APP, "Pantallas de turno", 1230, 300, 190, 55)
v.put("etl", "application-process", "ETL nocturno: extraer, transformar y cargar", 20, 440, 190, 65)
v.put("dw", APP, "Repositorio analítico y tablero de indicadores", 490, 440, 230, 65)
v.put("dInd", "data-object", "Indicadores de espera y desfase", 760, 440, 200, 65)
v.rel("triggering", "caja", "eP"); v.rel("triggering", "hc", "eC"); v.rel("triggering", "portal", "eR")
v.rel("flow", "eP", "esb"); v.rel("flow", "eC", "esb"); v.rel("flow", "eR", "esb")
v.rel("flow", "esb", "iTur"); v.rel("assignment", "tur", "iTur")
v.rel("serving", "ia", "tur", "hora estimada", via=[(1075, 197)])
v.rel("flow", "tur", "iWa", "aviso"); v.rel("assignment", "waapi", "iWa")
v.rel("flow", "tur", "pant", "estado en tiempo real", via=[(1075, 327)])
v.rel("flow", "caja", "etl", via=[(240, 67), (240, 472)])
v.rel("flow", "hc", "etl", via=[(240, 200), (240, 472)])
v.rel("flow", "tur", "etl", via=[(1205, 67), (1205, 620), (115, 620)])
v.rel("flow", "etl", "dw"); v.rel("access", "dw", "dInd")
v.rel("flow", "dw", "ia", "histórico de tiempos", via=[(705, 472), (705, 197)])
v.note("Tiempo real por el ESB (eventos). Diario por el ETL (histórico para los indicadores y para entrenar la IA).", 1230, 420, 260, 80)

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
    fold = {"business": [], "application": []}
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
        f'<archimate:model xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:archimate="http://www.archimatetool.com/archimate" name="TF G4 - Arquitectura de Aplicaciones" id="{nid()}" version="5.0.0">',
        '  <folder name="Strategy" id="%s" type="strategy"/>' % nid(),
        '  <folder name="Business" id="%s" type="business">' % nid(), *fold["business"], "  </folder>",
        '  <folder name="Application" id="%s" type="application">' % nid(), *fold["application"], "  </folder>",
        '  <folder name="Technology &amp; Physical" id="%s" type="technology"/>' % nid(),
        '  <folder name="Motivation" id="%s" type="motivation"/>' % nid(),
        '  <folder name="Implementation &amp; Migration" id="%s" type="implementation_migration"/>' % nid(),
        '  <folder name="Other" id="%s" type="other"/>' % nid(),
        '  <folder name="Relations" id="%s" type="relations">' % nid(), *rels, "  </folder>",
        '  <folder name="Views" id="%s" type="diagrams">' % nid(), *views, "  </folder>",
        "</archimate:model>", ""])

model_path = os.path.join(HERE, "aplicaciones_3_2.archimate")
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
