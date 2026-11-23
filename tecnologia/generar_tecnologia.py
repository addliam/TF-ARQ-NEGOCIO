"""Genera el modelo ArchiMate de 3.4 (tecnología) y exporta las vistas a PNG con Archi.

Uso:  python tecnologia/generar_tecnologia.py
Salida: tecnologia_3_4.archimate y T1..T7 *.png en esta carpeta.
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
ND, DV, SW, NET, TS, AR = "node", "device", "system-software", "communication-network", "technology-service", "artifact"

def hl(v, *keys):
    for k in keys: v.D[k]["style"] = {"lineWidth": "3", "fillColor": "#a6e08a"}

# ------------------------------------------------------------------ T1 mapa AS-IS
v = View("T1 Mapa de tecnología AS-IS", "T1_mapa_tecnologia_asis.png")
G = [("g1", "Seguridad perimetral"), ("g2", "Comunicaciones"), ("g3", "Redes"), ("g4", "Servidores y cloud"), ("g5", "Software de soporte")]
for i, (k, n) in enumerate(G):
    v.group(k, n, 20, 20 + i * 100, 1000, 85)
v.put("rt", DV, "Router del proveedor de internet", 40, 50, 220, 45, "g1")
v.note("Sin firewall dedicado, sin IPS/IDS ni VPN.", 280, 50, 320, 45)
v.put("isp", NET, "Un enlace de internet (fibra, 100 Mbps)", 40, 150, 260, 45, "g2")
v.put("cel", DV, "Celular con WhatsApp Business", 320, 150, 230, 45, "g2")
v.put("sw", DV, "Switches no administrados", 40, 250, 220, 45, "g3")
v.put("lan", NET, "Red local plana (sin VLAN)", 280, 250, 220, 45, "g3")
v.put("wifi", DV, "Access point doméstico", 520, 250, 200, 45, "g3")
v.put("srv", ND, "Servidor físico único", 40, 350, 200, 45, "g4")
v.put("pcs", DV, "30 PC de usuario", 260, 350, 180, 45, "g4")
v.put("ext", DV, "Disco externo (respaldo manual)", 460, 350, 230, 45, "g4")
v.put("os", SW, "Windows Server", 40, 450, 180, 45, "g5")
v.put("sql", SW, "SQL Server", 240, 450, 180, 45, "g5")
v.put("av", SW, "Antivirus gratuito", 440, 450, 180, 45, "g5")

# ------------------------------------------------------------------ T2 mapa TO-BE
v = View("T2 Mapa de tecnología TO-BE", "T2_mapa_tecnologia_tobe.png")
for i, (k, n) in enumerate(G):
    v.group(k, n, 20, 20 + i * 100, 1240, 85)
v.put("fw", DV, "Firewall NGFW con IPS/IDS", 40, 50, 210, 45, "g1")
v.put("vpn", TS, "VPN sitio a sitio", 270, 50, 180, 45, "g1")
v.put("waf", TS, "WAF (Application Gateway)", 470, 50, 210, 45, "g1")
v.put("dmz", NET, "DMZ hacia la capa media", 700, 50, 200, 45, "g1")
v.put("isp1", NET, "Enlace principal de fibra (200 Mbps)", 40, 150, 260, 45, "g2")
v.put("isp2", NET, "Enlace de respaldo (otro proveedor)", 320, 150, 250, 45, "g2")
v.put("wapi", TS, "WhatsApp Business API (proveedor)", 590, 150, 250, 45, "g2")
v.put("swc", DV, "Switch core administrado", 40, 250, 210, 45, "g3")
v.put("vlan", NET, "VLAN: administración, clínica, invitados, pantallas", 270, 250, 340, 45, "g3")
v.put("ap", DV, "Access points administrados", 630, 250, 210, 45, "g3")
v.put("tv", DV, "Televisores de turno (6)", 860, 250, 200, 45, "g3")
v.put("clu", ND, "Clúster local de 2 servidores", 40, 350, 230, 45, "g4")
v.put("nas", DV, "NAS de respaldo", 290, 350, 170, 45, "g4")
v.put("az", ND, "Microsoft Azure", 480, 350, 180, 45, "g4")
v.put("lb", TS, "Balanceador de carga", 680, 350, 190, 45, "g4")
v.put("hv", SW, "Hyper-V con conmutación por error", 40, 450, 250, 45, "g5")
v.put("sqlag", SW, "SQL Server Always On", 310, 450, 200, 45, "g5")
v.put("sb", SW, "Azure Service Bus (ESB)", 530, 450, 200, 45, "g5")
v.put("adf", SW, "Azure Data Factory (ETL)", 750, 450, 200, 45, "g5")
v.put("bk", SW, "Azure Backup", 970, 450, 170, 45, "g5")
hl(v, "fw", "vpn", "waf", "dmz", "isp2", "wapi", "swc", "vlan", "ap", "tv", "clu", "nas", "az", "lb", "hv", "sqlag", "sb", "adf", "bk")
v.note("Resaltados: componentes nuevos.", 900, 50, 230, 45)

# ------------------------------------------------------------------ T3 modelo AS-IS
v = View("T3 Modelo de tecnología AS-IS", "T3_tecnologia_asis.png")
v.put("inet", NET, "Internet", 380, 20, 200, 50)
v.put("rt", DV, "Router del ISP", 380, 120, 200, 50)
v.put("lan", NET, "Red local plana (switches no administrados)", 280, 220, 400, 50)
v.put("srv", ND, "Servidor físico único", 20, 330, 420, 200)
v.put("os", SW, "Windows Server", 40, 370, 180, 45, "srv")
v.put("sql", SW, "SQL Server", 240, 370, 180, 45, "srv")
v.put("aHc", AR, "Software de historias clínicas", 40, 450, 180, 50, "srv")
v.put("aCa", AR, "Módulo de caja y farmacia", 240, 450, 180, 50, "srv")
v.put("pcs", DV, "30 PC de usuario", 500, 330, 200, 55)
v.put("ext", DV, "Disco externo", 500, 430, 200, 55)
v.put("cel", DV, "Celular con WhatsApp", 740, 120, 200, 55)
v.rel("association", "inet", "rt"); v.rel("association", "rt", "lan"); v.rel("association", "lan", "srv")
v.rel("association", "lan", "pcs"); v.rel("association", "srv", "ext", "copia manual"); v.rel("association", "inet", "cel")
v.note("Punto único de falla: si el servidor o el enlace caen, se detiene toda la atención. Sin firewall ni respaldo automático.", 740, 330, 300, 80)

# ------------------------------------------------------------------ T4 data center local
v = View("T4 Data center y red de servidores", "T4_data_center.png")
v.put("isp1", NET, "Enlace principal", 20, 20, 180, 50)
v.put("isp2", NET, "Enlace de respaldo", 240, 20, 180, 50)
v.put("fw", DV, "Firewall NGFW (IPS/IDS, VPN)", 100, 120, 240, 55)
v.put("swc", DV, "Switch core administrado", 100, 230, 240, 55)
v.put("vA", NET, "VLAN 10 Administración", 20, 340, 190, 50)
v.put("vC", NET, "VLAN 20 Clínica", 230, 340, 190, 50)
v.put("vP", NET, "VLAN 30 Pantallas", 440, 340, 190, 50)
v.put("vI", NET, "VLAN 40 Invitados", 650, 340, 190, 50)
v.put("rack", ND, "Clúster de servidores (rack local)", 460, 20, 560, 280)
v.put("h1", ND, "Host 1", 480, 60, 250, 150, "rack")
v.put("h2", ND, "Host 2", 750, 60, 250, 150, "rack")
v.put("vm1", SW, "VM SQL Server (primaria)", 495, 95, 220, 45, "rack")
v.put("vm2", SW, "VM integración (agente ESB y ETL)", 495, 150, 220, 50, "rack")
v.put("vm3", SW, "VM SQL Server (réplica)", 765, 95, 220, 45, "rack")
v.put("vm4", SW, "VM integración (réplica)", 765, 150, 220, 50, "rack")
v.put("nas", DV, "NAS de respaldo", 480, 230, 250, 50, "rack")
v.put("ups", DV, "UPS", 750, 230, 250, 50, "rack")
v.put("tv", DV, "Televisores de turno", 440, 440, 190, 50)
v.put("pcs", DV, "PC de caja, admisión y consultorios", 130, 440, 260, 50)
v.rel("association", "isp1", "fw"); v.rel("association", "isp2", "fw"); v.rel("association", "fw", "swc")
for n_ in ["vA", "vC", "vP", "vI"]: v.rel("association", "swc", n_)
v.rel("association", "swc", "rack"); v.rel("association", "vC", "pcs"); v.rel("association", "vP", "tv")
hl(v, "fw", "swc", "rack", "nas", "ups", "isp2", "vA", "vC", "vP", "vI", "tv")
v.note("SQL Server Always On replica entre hosts: si uno cae, el otro asume en segundos. El tráfico de invitados no ve la red clínica.", 660, 430, 300, 80)

# ------------------------------------------------------------------ T5 cloud
v = View("T5 Arquitectura cloud (Azure)", "T5_cloud.png")
v.put("inet", NET, "Internet (pacientes y personal)", 20, 200, 200, 55)
v.put("azr", ND, "Microsoft Azure (región Brazil South)", 260, 20, 960, 470)
v.put("dmz", NET, "Subred DMZ", 280, 60, 220, 410, "azr")
v.put("agw", TS, "Application Gateway con WAF (balanceador)", 295, 180, 190, 70, "azr")
v.put("mid", NET, "Subred media (aplicaciones)", 530, 60, 330, 410, "azr")
v.put("asp", ND, "App Service (2 instancias, autoescalado)", 545, 95, 300, 140, "azr")
v.put("aTur", AR, "Sistema de citas y turnos", 560, 140, 130, 55, "azr")
v.put("aPor", AR, "Portal web de citas", 700, 140, 130, 55, "azr")
v.put("sb", SW, "Azure Service Bus (ESB)", 545, 260, 300, 50, "azr")
v.put("ml", SW, "Azure Machine Learning (motor de IA)", 545, 330, 300, 50, "azr")
v.put("adf", SW, "Azure Data Factory (ETL)", 545, 400, 300, 50, "azr")
v.put("dat", NET, "Subred de datos (endpoints privados)", 890, 60, 310, 410, "azr")
v.put("sqlz", SW, "Azure SQL Database (redundancia de zona)", 905, 95, 280, 55, "azr")
v.put("cos", SW, "Azure Cosmos DB", 905, 170, 280, 50, "azr")
v.put("blob", SW, "Blob Storage (data lake)", 905, 240, 280, 50, "azr")
v.put("bk", SW, "Azure Backup (bóveda)", 905, 310, 280, 50, "azr")
v.put("vgw", TS, "VPN Gateway", 905, 400, 280, 50, "azr")
v.put("loc", ND, "Data center local", 905, 540, 280, 50)
v.put("pbi", SW, "Power BI (SaaS)", 20, 330, 200, 50)
v.put("wa", TS, "WhatsApp Business API (proveedor)", 20, 420, 200, 55)
v.rel("association", "inet", "agw"); v.rel("serving", "agw", "asp"); v.rel("association", "vgw", "loc", "túnel IPsec")
hl(v, "agw", "asp", "sb", "ml", "adf", "sqlz", "cos", "blob", "bk", "vgw")

# ------------------------------------------------------------------ T6 integraciones
v = View("T6 Integraciones tecnológicas", "T6_integraciones.png")
v.put("loc", ND, "Data center local", 20, 20, 300, 260)
v.put("sql", SW, "SQL Server (historias y caja)", 40, 60, 260, 50, "loc")
v.put("ag", SW, "Agente de integración (relay del ESB)", 40, 130, 260, 50, "loc")
v.put("ir", SW, "Integration runtime autohospedado (ETL)", 40, 200, 260, 50, "loc")
v.put("fw", DV, "Firewall NGFW", 380, 120, 180, 55)
v.put("vpn", NET, "Túnel VPN IPsec", 600, 120, 180, 55)
v.put("azr", ND, "Azure", 840, 20, 330, 260)
v.put("sb", SW, "Azure Service Bus", 860, 60, 290, 50, "azr")
v.put("adf", SW, "Azure Data Factory", 860, 130, 290, 50, "azr")
v.put("app", SW, "App Service (turnos)", 860, 200, 290, 50, "azr")
v.put("wa", TS, "WhatsApp Business API", 860, 330, 290, 50)
v.put("ose", TS, "OSE/PSE (SUNAT)", 20, 330, 300, 50)
v.rel("association", "loc", "fw"); v.rel("association", "fw", "vpn"); v.rel("association", "vpn", "azr")
v.rel("association", "app", "wa", "HTTPS")
v.rel("association", "loc", "ose", "HTTPS (XML UBL)")
v.note("El agente y el integration runtime solo abren conexiones de salida por la VPN: no se expone ningún puerto del servidor local a internet.", 380, 330, 400, 70)

# ------------------------------------------------------------------ T7 ciberseguridad
v = View("T7 Ciberseguridad", "T7_ciberseguridad.png")
v.put("inet", NET, "Internet", 20, 200, 160, 55)
v.put("z1", ND, "Zona externa", 220, 20, 220, 440)
v.put("waf", TS, "WAF (Application Gateway)", 235, 80, 190, 55, "z1")
v.put("ddos", TS, "Protección DDoS básica", 235, 170, 190, 55, "z1")
v.put("fw", DV, "Firewall NGFW con IPS/IDS", 235, 300, 190, 55, "z1")
v.put("z2", ND, "DMZ", 480, 20, 220, 440)
v.put("pub", AR, "Punto de entrada público (portal y API)", 495, 80, 190, 60, "z2")
v.put("vpn", TS, "VPN sitio a sitio y VPN de usuario (TI)", 495, 300, 190, 60, "z2")
v.put("z3", ND, "Capa media", 740, 20, 220, 440)
v.put("app7", SW, "App Service y Service Bus", 755, 80, 190, 55, "z3")
v.put("ag", SW, "Agente de integración", 755, 300, 190, 55, "z3")
v.put("z4", ND, "Capa de datos", 1000, 20, 220, 440)
v.put("db", SW, "Bases de datos (endpoints privados)", 1015, 80, 190, 60, "z4")
v.put("sql", SW, "SQL Server local", 1015, 300, 190, 55, "z4")
v.put("iam", TS, "Microsoft Entra ID (MFA)", 495, 500, 190, 55)
v.put("def", TS, "Microsoft Defender (antimalware)", 755, 500, 190, 55)
v.rel("association", "inet", "waf"); v.rel("association", "inet", "fw")
v.rel("association", "waf", "pub"); v.rel("association", "pub", "app7"); v.rel("association", "app7", "db")
v.rel("association", "fw", "vpn"); v.rel("association", "vpn", "ag"); v.rel("association", "ag", "sql")
hl(v, "waf", "ddos", "fw", "pub", "vpn", "iam", "def")
v.note("Defensa en capas: nadie llega a la capa media ni a los datos sin pasar por la DMZ.", 20, 500, 400, 55)

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
        f'<archimate:model xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:archimate="http://www.archimatetool.com/archimate" name="TF G4 - Arquitectura de Tecnologia" id="{nid()}" version="5.0.0">',
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

model_path = os.path.join(HERE, "tecnologia_3_4.archimate")
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
