# Índice propuesto: Trabajo Final (G4, Policlínico Parroquial Nuestra Señora de los Ángeles)

Regla de oro: los capítulos 1 y 2 ya existen (TP). El capítulo 3 repite **la misma plantilla de 7 bloques** en cada dominio (negocio, aplicaciones, datos y tecnología). Cada artefacto lleva un párrafo de resumen o conclusión, porque el lineamiento dice que "debe comunicar".

## Preliminares
- Carátula (TRABAJO FINAL, integrantes por apellido paterno con código)
- Objetivo del estudiante (Student Outcome): para EAC, CAC, ICACIT C, ICACIT H y Logro se indica **dónde** y **cómo** se desarrolla, con la numeración nueva
- Índice de contenido, índice de figuras y de tablas
- Introducción

## Capítulo 1. Marco teórico (se amplía)
1.1–1.15 como ahora, y además:
- 1.16 Fase B: arquitectura de negocio y análisis de brechas
- 1.17 Fase C: arquitectura de aplicaciones y de datos (BD relacional y NoSQL, motor e instancia)
- 1.18 Fase D: arquitectura de tecnología (redes, seguridad perimetral, servidores, cloud IaaS/PaaS/SaaS)
- 1.19 Artefactos TOGAF: principios, catálogos, matrices y diagramas
- 1.20 Integración y continuidad: ESB, ETL, alta disponibilidad, respaldo y DMZ
- 1.21 Fases E a H y gobierno de arquitectura

## Capítulo 2. Análisis y diagnóstico (TP con observaciones levantadas)
Se mantiene igual: 2.1 a 2.7.

## Capítulo 3. Arquitectura empresarial (AS-IS → TO-BE)

Plantilla de cada dominio X:

| N.º | Bloque | Contenido mínimo |
|---|---|---|
| 3.x.1 | Principios de X | Tabla: Principio, Significado, **Aplicación** (reemplaza a "Impacto") |
| 3.x.2 | Catálogos de X | Los que pide el PPT para el dominio |
| 3.x.3 | Matrices de X | Las que pide el PPT para el dominio |
| 3.x.4 | Mapa de capacidades de X | Front, middle y back office |
| 3.x.5 | Diagramas ArchiMate de X | AS-IS y TO-BE, solo con los colores de esa capa |
| 3.x.6 | Brechas de X | Tabla: N.º, Dominio, Brecha, Solución potencial, Dependencia |
| 3.x.7 | Conclusión del dominio | Qué cambia y qué requisito pasa a la fase siguiente |

### 3.1 Arquitectura de negocio (Fase B)
- 3.1.1 Principios de negocio
- 3.1.2 Catálogos: capacidades de negocio, actores y roles, procesos y servicios de negocio
- 3.1.3 Matrices: capacidad–unidad organizacional, actor–proceso (RACI)
- 3.1.4 Mapa de capacidades de negocio TO-BE (procesos, servicios, stakeholders y áreas)
- 3.1.5 Diagramas: servicio e información de negocio, descomposición funcional, ciclo de vida del servicio (la atención), ArchiMate AS-IS y TO-BE (solo en amarillo)
- 3.1.6 Brechas de negocio
- 3.1.7 Modelo de negocio TO-BE en ArchiMate

### 3.2 Arquitectura de aplicaciones (Fase C)
- 3.2.1 Principios de aplicaciones
- 3.2.2 Catálogos: de aplicaciones y de interfaces (API y protocolo)
- 3.2.3 Matrices: aplicación–datos (CRUD) y aplicación–capacidad de negocio
- 3.2.4 Mapa de capacidades de aplicaciones (aplicaciones, interfaces y SaaS; si hay ESB, va en middle office)
- 3.2.5 Diagramas ArchiMate de aplicaciones AS-IS y TO-BE (en celeste)
- 3.2.6 Arquitecturas de transición (si aplica)
- 3.2.7 Brechas de aplicaciones (ESB e integración ETL)

### 3.3 Arquitectura de datos (Fase C)
- 3.3.1 Principios de datos (columna Aplicación)
- 3.3.2 Catálogos: entidades de datos y bases de datos (tipo, motor, ubicación y propósito)
- 3.3.3 Matrices: datos–aplicación (CRUD) y datos–proceso
- 3.3.4 Mapa de capacidades de datos (BD relacionales y no relacionales)
- 3.3.5 Diagramas ArchiMate de datos AS-IS y TO-BE (instancia dibujada fuera del SGBD, flujo ETL obligatorio)
- 3.3.6 Arquitecturas de transición (si aplica)
- 3.3.7 Brechas de datos

### 3.4 Arquitectura de tecnología (Fase D)
- 3.4.1 Principios de tecnología (resiliencia y alta disponibilidad)
- 3.4.2 Catálogos: servidores (con plataforma y SO) y dispositivos de comunicación
- 3.4.3 Matrices: aplicación–tecnología y servidor–ubicación
- 3.4.4 Mapa de capacidades de tecnología (seguridad perimetral, comunicaciones, redes y subredes, servidores y cloud, software de soporte: SO, ETL, BUS, backup)
- 3.4.5 Capacidad computacional (dimensionamiento)
- 3.4.6 Diagramas ArchiMate de tecnología AS-IS y TO-BE (en verde): data center, cloud, integraciones y ciberseguridad (red de servidores, DMZ hacia middle)
- 3.4.7 Modelo de continuidad: copias de respaldo, alta disponibilidad (cluster y balanceador de carga) y seguridad perimetral (firewall, IPS/IDS, VPN, WAF)
- 3.4.8 Arquitecturas de transición (si aplica)
- 3.4.9 Brechas de tecnología

### 3.5 Arquitectura empresarial integral
- 3.5.1 Modelo ArchiMate integrado TO-BE (las 4 capas juntas)
- 3.5.2 Consolidado de brechas, de las cuatro capas en una sola matriz

## Capítulo 4. Plan de implementación (Fases E y F)
- 4.1 Paquetes de trabajo derivados de las brechas
- 4.2 Roadmap de arquitectura
- 4.3 Plan de inversión
- 4.4 Plan de desmantelamiento (si aplica, por ejemplo el voucher físico)
- 4.5 Plan de implementación (cronograma y riesgos)

## Capítulo 5. Gobierno de arquitectura (Fases G y H)
- 5.1 Marco de gobierno propuesto (comité, roles y cumplimiento)
- 5.2 Gestión del cambio de arquitectura

## Cierre
- Conclusiones (una por capítulo u objetivo)
- Recomendaciones
- Glosario
- Bibliografía (APA 7)
- Anexos (sin enlaces a diagramas)

---

## Matriz de verificación PPT → índice

| PPT (diap.) | Exigencia | Dónde va |
|---|---|---|
| 29–31 | AS-IS, TO-BE y brechas de negocio | 3.1.5, 3.1.6 |
| 32 | Principios de negocio | 3.1.1 |
| 33 | Catálogo de capacidades, matriz capacidad–organización | 3.1.2, 3.1.3 |
| 35 | Diagrama de servicio e información de negocio | 3.1.5 |
| 36 | Descomposición funcional | 3.1.5 |
| 37 | Ciclo de vida del producto o servicio | 3.1.5 |
| 38 | Mapa de capacidades (procesos, servicios, stakeholders, áreas) | 3.1.4 |
| 39 | Mapa de brechas de negocio | 3.1.6 |
| 40–42 | Línea base, objetivo y brechas de aplicaciones | 3.2.5, 3.2.7 |
| 44 | Principios de aplicaciones | 3.2.1 |
| 45 | Catálogo de aplicaciones e interfaces | 3.2.2 |
| 46 | Matrices CRUD y aplicación–capacidad | 3.2.3 |
| 47 | Mapa de capacidades de aplicaciones (apps, interfaces, SaaS) | 3.2.4 |
| 48 | Diagramas ArchiMate y brechas de aplicaciones (ETL, ESB) | 3.2.5, 3.2.7 |
| 50–52 | BD relacional y NoSQL, motor e instancia, ETL | 1.17, 3.3.5 |
| 53 | Principios de datos | 3.3.1 |
| 54 | Catálogo de entidades y de BD | 3.3.2 |
| 55 | Mapa de capacidades de datos | 3.3.4 |
| 56 | Matrices CRUD y datos–proceso | 3.3.3 |
| 57 | Diagramas ArchiMate y brechas de datos | 3.3.5, 3.3.7 |
| 59–61 | Redes, seguridad perimetral, nodos, servidores, SO, cloud | 1.18, 3.4.6 |
| 62 | AS-IS y TO-BE de tecnología | 3.4.6 |
| 63 | Principios de tecnología (HA, cluster, balanceador) | 3.4.1, 3.4.7 |
| 64 | Catálogo de servidores y de dispositivos de comunicación | 3.4.2 |
| 65 | Mapa de capacidades de tecnología | 3.4.4 |
| 66 | Matrices aplicación–tecnología y servidor–ubicación | 3.4.3 |
| 67 | Diagramas ArchiMate y brechas de tecnología (WAF) | 3.4.6, 3.4.9 |
| Enunciado TF | Roadmap, inversión, desmantelamiento, gobierno | Cap. 4 y 5 |
| Apuntes | Arquitectura integral al final | 3.5 |
