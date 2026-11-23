"""Genera el modelo ArchiMate de 3.5 (integral) y exporta las vistas a PNG con Archi.

Uso:  python integral/generar_integral.py
Salida: integral_3_5.archimate e I1 *.png en esta carpeta.
"""
import os, shutil, subprocess, tempfile, uuid, glob
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHI = r"C:\Program Files\Archi\Archi.exe"

TYPE = {
    "business-actor": ("BusinessActor", "business"),
    "business-process": ("BusinessProcess", "business"),
    "business-event": ("BusinessEvent", "business"),
    "business-service": ("BusinessService", "business"),
    "application-component": ("ApplicationComponent", "application"),
    "application-interface": ("ApplicationInterface", "application"),
    "application-service": ("ApplicationService", "application"),
    "application-event": ("ApplicationEvent", "application"),
    "application-process": ("ApplicationProcess", "application"),
    "data-object": ("DataObject", "application"),
    "system-software": ("SystemSoftware", "technology"),
    "artifact": ("Artifact", "technology"),
    "node": ("Node", "technology"),
    "device": ("Device", "technology"),
    "communication-network": ("CommunicationNetwork", "technology"),
    "technology-service": ("TechnologyService", "technology"),
    "path": ("Path", "technology"),
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
        ab = (x, y, w, h)
        if parent:  # Archi usa coordenadas relativas al grupo
            px, py = self.D[parent]["ab"][:2]; x, y = x - px, y - py
        n = dict(kind="el", id=nid(), el=e, b=(x, y, w, h), ab=ab, children=[], conns=[], style={})
        self.D[key] = n
        (self.D[parent]["children"] if parent else self.top).append(n)
        return n
    def group(self, key, name, x, y, w, h):
        n = dict(kind="group", id=nid(), name=name, b=(x, y, w, h), ab=(x, y, w, h), children=[], conns=[], style={})
        self.D[key] = n; self.top.append(n); return n
    def note(self, text, x, y, w=200, h=40):
        self.top.append(dict(kind="note", id=nid(), text=text, b=(x, y, w, h), children=[], conns=[], style={}))
    def rel(self, rtype, a, b, name="", access=None, via=()):
        rid = (rtype, a, b, name)
        if rid not in RELS:
            RELS[rid] = dict(id=nid(), type=RTYPE[rtype], s=ELS[a]["id"], t=ELS[b]["id"], name=name, access=access)
        def ctr(k):
            x, y, w, h = self.D[k]["ab"]; return x + w / 2, y + h / 2
        (sx, sy), (tx, ty) = ctr(a), ctr(b)
        bps = [(int(px - sx), int(py - sy), int(px - tx), int(py - ty)) for px, py in via]
        self.D[a]["conns"].append(dict(id=nid(), s=self.D[a]["id"], t=self.D[b]["id"], rel=RELS[rid]["id"], bps=bps))
    def bold(self, *keys):
        for k in keys: self.D[k]["style"] = {"lineWidth": "3", "fillColor": "#a8d8f0"}

APP = "application-component"
v = View("I1 Arquitectura empresarial integral TO-BE", "I1_integral_tobe.png")
X = [40, 260, 480, 700, 920, 1140]
v.group("gN", "Capa de negocio", 20, 20, 1400, 230)
v.put("aPac", "business-actor", "Paciente", 40, 55, 180, 50, "gN")
v.put("aEnf", "business-actor", "Enfermera", 920, 55, 180, 50, "gN")
for k, n, x in [("bGc", "Gestionar cita", X[0]), ("bRp", "Registrar pago", X[1]), ("bGt", "Gestionar turno", X[2]),
                ("bAct", "Actualizar turno", X[3]), ("bIt", "Informar estado del turno", X[4]), ("bAte", "Atender consulta médica", X[5])]:
    v.put(k, "business-process", n, x, 130, 180, 55, "gN")
v.group("gA", "Capa de aplicaciones", 20, 270, 1400, 220)
for k, n, x in [("portal", "Portal web de citas", X[0]), ("caja", "Módulo de caja", X[1]), ("tur", "Sistema de citas y turnos", X[2]),
                ("ia", "Motor de IA de estimación", X[3]), ("waapi", "Plataforma de notificaciones y pantallas", X[4]), ("hc", "Software de historias clínicas", X[5])]:
    v.put(k, APP, n, x, 305, 180, 55, "gA")
v.put("esb", APP, "Bus de servicios empresariales (ESB)", 40, 410, 1280, 45, "gA")
v.group("gD", "Capa de datos", 20, 510, 1400, 120)
for k, n, x in [("dCit", "Cita", X[0]), ("dPag", "Pago", X[1]), ("dTur", "Turno", X[2]), ("dEst", "Estimación y eventos", X[3]), ("dInd", "Indicadores de espera (ETL)", X[4]), ("dHc", "Historia clínica", X[5])]:
    v.put(k, "data-object", n, x + 90, 550, 150, 55, "gD")
v.group("gT", "Capa de tecnología", 20, 650, 1400, 170)
v.put("dmz", "communication-network", "DMZ con WAF y balanceador de carga", 40, 690, 400, 45, "gT")
v.put("az", "node", "Azure: App Service, Azure SQL, Cosmos DB, Service Bus, ML, Data Factory", 480, 690, 620, 45, "gT")
v.put("vpn", "technology-service", "VPN sitio a sitio", 480, 755, 180, 45, "gT")
v.put("loc", "node", "Clúster local: SQL Server Always On y agente de integración", 700, 755, 620, 45, "gT")
v.put("fw", "device", "Firewall NGFW con IPS/IDS", 40, 755, 400, 45, "gT")
for a, b in [("bGc", "bRp"), ("bRp", "bGt"), ("bGt", "bAte"), ("bAte", "bAct"), ("bAct", "bIt")]:
    pass
v.rel("association", "aPac", "bGc"); v.rel("assignment", "aEnf", "bIt")
for c_, b in [("portal", "bGc"), ("caja", "bRp"), ("tur", "bGt"), ("ia", "bAct"), ("waapi", "bIt"), ("hc", "bAte")]:
    v.rel("serving", c_, b)
for c_ in ["portal", "caja", "tur", "ia", "waapi", "hc"]:
    v.rel("serving", "esb", c_)
for c_, dd in [("portal", "dCit"), ("caja", "dPag"), ("tur", "dTur"), ("ia", "dEst"), ("waapi", "dInd"), ("hc", "dHc")]:
    x0 = v.D[c_]["ab"][0]
    v.rel("access", c_, dd, via=[(x0 + 165, 370)])
v.rel("serving", "az", "esb", via=[(1000, 712), (1000, 470)])
v.rel("serving", "loc", "hc", via=[(1380, 777), (1380, 332)])
v.rel("association", "dmz", "az"); v.rel("association", "az", "vpn"); v.rel("association", "vpn", "loc")
v.rel("association", "fw", "dmz")
hl = lambda *k: [v.D.__getitem__(x)["style"].update({"lineWidth": "3"}) for x in k]
v.note("Trazabilidad: cada proceso de negocio recibe una aplicación; todas se integran por el ESB; los datos se guardan en Azure o en el clúster local y se analizan con ETL; la DMZ es la única entrada a la capa media.", 20, 840, 900, 50)

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
        f'<archimate:model xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:archimate="http://www.archimatetool.com/archimate" name="TF G4 - Arquitectura Empresarial Integral" id="{nid()}" version="5.0.0">',
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

model_path = os.path.join(HERE, "integral_3_5.archimate")
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
