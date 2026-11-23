# Índice propuesto: Trabajo Final (G4, Policlínico Parroquial Nuestra Señora de los Ángeles)

Convención de niveles:
- **Capítulo** (3): Título 1
- **Nivel 1** (3.1): Título 2, va en el índice de Word
- **Nivel 2** (3.1.2): Título 3, va en el índice de Word
- **Nivel 3** (3.1.2.1): Título 4, aparece solo en el cuerpo del documento

El índice de Word cerca de la carátula se genera hasta el nivel 2 (TOC \o "1-3"). El cuerpo llega hasta el nivel 3.

Cada dominio del capítulo 3 repite los mismos 7 bloques de nivel 2: principios, catálogos, matrices, mapa de capacidades, diagramas, brechas y conclusión. Cada artefacto lleva un resumen o una conclusión.

---

## Preliminares
- Carátula
- Objetivo del estudiante (Student Outcome)
- Índice de contenido / Índice de figuras / Índice de tablas
- Introducción

## 1. MARCO TEÓRICO
- 1.1 Arquitectura empresarial y arquitectura de negocio
- 1.2 TOGAF 10 y el ADM
  - 1.2.1 Fase Preliminar y Fase A
  - 1.2.2 Fase B: arquitectura de negocio
  - 1.2.3 Fase C: arquitectura de sistemas de información
    - 1.2.3.1 Arquitectura de aplicaciones
    - 1.2.3.2 Arquitectura de datos
  - 1.2.4 Fase D: arquitectura de tecnología
  - 1.2.5 Fases E a H y gestión de requerimientos
  - 1.2.6 Análisis de brechas (gap analysis)
- 1.3 ArchiMate
  - 1.3.1 Capas y colores (negocio, aplicación, tecnología)
  - 1.3.2 Elementos y relaciones
- 1.4 Artefactos de arquitectura
  - 1.4.1 Principios
  - 1.4.2 Catálogos
  - 1.4.3 Matrices
  - 1.4.4 Diagramas
- 1.5 Herramientas de diagnóstico estratégico
  - 1.5.1 Misión, visión, objetivos y estrategia
  - 1.5.2 PESTEL
  - 1.5.3 Cinco fuerzas de Porter
  - 1.5.4 Mapa de procesos
  - 1.5.5 Modelo de negocio Canvas
  - 1.5.6 Cadena de valor
  - 1.5.7 Mapa de capacidades empresariales
- 1.6 Herramientas de desempeño y problema
  - 1.6.1 SIPOC
  - 1.6.2 Indicadores de desempeño (KPI) y Balanced Scorecard
  - 1.6.3 5W2H
  - 1.6.4 Ishikawa
  - 1.6.5 SSM
- 1.7 Conceptos de datos y tecnología
  - 1.7.1 Bases de datos relacionales y NoSQL, motor e instancia
  - 1.7.2 Integración: ESB y ETL
  - 1.7.3 Redes, seguridad perimetral y DMZ
  - 1.7.4 Servidores, sistemas operativos y cloud (IaaS, PaaS, SaaS)
  - 1.7.5 Alta disponibilidad y continuidad
- 1.8 Inteligencia artificial como tecnología emergente

## 2. ANÁLISIS Y DIAGNÓSTICO
Igual que en el TP, ya con las observaciones levantadas: de 2.1 a 2.7, con sus niveles 2 y 3 actuales.

## 3. ARQUITECTURA EMPRESARIAL (AS-IS → TO-BE)

### 3.1 Arquitectura de negocio (Fase B)
- 3.1.1 Principios de negocio
  - 3.1.1.1 Tabla de principios (Principio, Significado, Aplicación)
  - 3.1.1.2 Conclusión de principios
- 3.1.2 Catálogos de negocio
  - 3.1.2.1 Catálogo de capacidades de negocio
  - 3.1.2.2 Catálogo de actores y roles
  - 3.1.2.3 Catálogo de procesos de negocio
  - 3.1.2.4 Catálogo de servicios de negocio
- 3.1.3 Matrices de negocio
  - 3.1.3.1 Matriz capacidad – unidad organizacional
  - 3.1.3.2 Matriz actor – proceso (RACI)
  - 3.1.3.3 Matriz proceso – servicio de negocio
- 3.1.4 Mapa de capacidades de negocio
  - 3.1.4.1 Mapa de capacidades AS-IS
  - 3.1.4.2 Mapa de capacidades TO-BE
  - 3.1.4.3 Capacidades nuevas, modificadas y retiradas
- 3.1.5 Diagramas de negocio
  - 3.1.5.1 Diagrama de servicio e información de negocio
  - 3.1.5.2 Diagrama de descomposición funcional
  - 3.1.5.3 Diagrama del ciclo de vida del servicio (atención ambulatoria)
  - 3.1.5.4 Modelo de negocio AS-IS en ArchiMate
  - 3.1.5.5 Modelo de negocio TO-BE en ArchiMate
- 3.1.6 Brechas de negocio
  - 3.1.6.1 Matriz de brechas (N.º, Dominio, Brecha, Solución potencial, Dependencia)
  - 3.1.6.2 Análisis de las brechas
- 3.1.7 Conclusión de la arquitectura de negocio

### 3.2 Arquitectura de aplicaciones (Fase C)
- 3.2.1 Principios de aplicaciones
  - 3.2.1.1 Tabla de principios (Principio, Significado, Aplicación)
  - 3.2.1.2 Conclusión de principios
- 3.2.2 Catálogos de aplicaciones
  - 3.2.2.1 Catálogo de aplicaciones
  - 3.2.2.2 Catálogo de interfaces (API y protocolo)
  - 3.2.2.3 Catálogo de servicios de aplicación
- 3.2.3 Matrices de aplicaciones
  - 3.2.3.1 Matriz aplicación – datos (CRUD)
  - 3.2.3.2 Matriz aplicación – capacidad de negocio
  - 3.2.3.3 Matriz aplicación – proceso
- 3.2.4 Mapa de capacidades de aplicaciones
  - 3.2.4.1 Mapa AS-IS
  - 3.2.4.2 Mapa TO-BE (front, middle con ESB, back)
  - 3.2.4.3 Aplicaciones SaaS e interfaces
- 3.2.5 Diagramas de aplicaciones
  - 3.2.5.1 Modelo de aplicaciones AS-IS en ArchiMate
  - 3.2.5.2 Modelo de aplicaciones TO-BE en ArchiMate
  - 3.2.5.3 Diagrama de integración (ESB y ETL)
  - 3.2.5.4 Arquitecturas de transición (si aplica)
- 3.2.6 Brechas de aplicaciones
  - 3.2.6.1 Matriz de brechas
  - 3.2.6.2 Análisis de las brechas
- 3.2.7 Conclusión de la arquitectura de aplicaciones

### 3.3 Arquitectura de datos (Fase C)
- 3.3.1 Principios de datos
  - 3.3.1.1 Tabla de principios (Principio, Significado, Aplicación)
  - 3.3.1.2 Conclusión de principios
- 3.3.2 Catálogos de datos
  - 3.3.2.1 Catálogo de entidades de datos
  - 3.3.2.2 Catálogo de bases de datos (tipo, motor, instancia, ubicación, propósito)
  - 3.3.2.3 Catálogo de datos maestros
- 3.3.3 Matrices de datos
  - 3.3.3.1 Matriz datos – aplicación (CRUD)
  - 3.3.3.2 Matriz datos – proceso
- 3.3.4 Mapa de capacidades de datos
  - 3.3.4.1 Mapa AS-IS
  - 3.3.4.2 Mapa TO-BE (relacional y no relacional)
- 3.3.5 Diagramas de datos
  - 3.3.5.1 Modelo lógico de datos
  - 3.3.5.2 Modelo de datos AS-IS en ArchiMate
  - 3.3.5.3 Modelo de datos TO-BE en ArchiMate (instancia fuera del SGBD)
  - 3.3.5.4 Flujo ETL
  - 3.3.5.5 Arquitecturas de transición (si aplica)
- 3.3.6 Brechas de datos
  - 3.3.6.1 Matriz de brechas
  - 3.3.6.2 Análisis de las brechas
- 3.3.7 Conclusión de la arquitectura de datos

### 3.4 Arquitectura de tecnología (Fase D)
- 3.4.1 Principios de tecnología
  - 3.4.1.1 Tabla de principios (Principio, Significado, Aplicación)
  - 3.4.1.2 Conclusión de principios
- 3.4.2 Catálogos de tecnología
  - 3.4.2.1 Catálogo de servidores (plataforma, SO, CPU, RAM, estado)
  - 3.4.2.2 Catálogo de dispositivos de comunicación
  - 3.4.2.3 Catálogo de software de soporte (SO, ETL, BUS, backup)
- 3.4.3 Matrices de tecnología
  - 3.4.3.1 Matriz aplicación – tecnología
  - 3.4.3.2 Matriz servidor – ubicación
- 3.4.4 Mapa de capacidades de tecnología
  - 3.4.4.1 Mapa AS-IS
  - 3.4.4.2 Mapa TO-BE (seguridad perimetral, comunicaciones, redes, servidores y cloud, software de soporte)
  - 3.4.4.3 Capacidad computacional
- 3.4.5 Diagramas de tecnología
  - 3.4.5.1 Modelo de tecnología AS-IS en ArchiMate
  - 3.4.5.2 Data center y red de servidores
  - 3.4.5.3 Cloud
  - 3.4.5.4 Integraciones
  - 3.4.5.5 Ciberseguridad (DMZ hacia middle, firewall, IPS/IDS, VPN, WAF)
- 3.4.6 Modelo de continuidad
  - 3.4.6.1 Copias de respaldo
  - 3.4.6.2 Alta disponibilidad (cluster y balanceador de carga)
  - 3.4.6.3 Seguridad perimetral
  - 3.4.6.4 Arquitecturas de transición (si aplica)
- 3.4.7 Brechas de tecnología
  - 3.4.7.1 Matriz de brechas
  - 3.4.7.2 Análisis de las brechas
- 3.4.8 Conclusión de la arquitectura de tecnología

### 3.5 Arquitectura empresarial integral
- 3.5.1 Modelo integrado TO-BE en ArchiMate
  - 3.5.1.1 Diagrama de las cuatro capas
  - 3.5.1.2 Trazabilidad entre capas
- 3.5.2 Consolidado de brechas
  - 3.5.2.1 Matriz consolidada de brechas
  - 3.5.2.2 Priorización de brechas

## 4. PLAN DE IMPLEMENTACIÓN (Fases E y F)
- 4.1 Oportunidades y soluciones
  - 4.1.1 Paquetes de trabajo
  - 4.1.2 Dependencias entre paquetes
- 4.2 Roadmap de arquitectura
  - 4.2.1 Arquitecturas de transición
  - 4.2.2 Hoja de ruta
- 4.3 Plan de inversión
  - 4.3.1 Presupuesto por paquete
  - 4.3.2 Beneficios esperados
- 4.4 Plan de desmantelamiento
  - 4.4.1 Componentes que se retiran (voucher físico)
  - 4.4.2 Secuencia de retiro
- 4.5 Plan de implementación
  - 4.5.1 Cronograma
  - 4.5.2 Riesgos y mitigación
  - 4.5.3 Plan de operación y soporte

## 5. GOBIERNO DE ARQUITECTURA (Fases G y H)
- 5.1 Marco de gobierno propuesto
  - 5.1.1 Estructura y roles (comité de arquitectura)
  - 5.1.2 Cumplimiento y revisión de arquitectura
  - 5.1.3 Indicadores de gobierno
- 5.2 Gestión del cambio de arquitectura
  - 5.2.1 Gestión de requerimientos
  - 5.2.2 Gestión del cambio organizacional

## Cierre
- Conclusiones
- Recomendaciones
- Glosario
- Bibliografía
- Anexos

---

## Matriz de verificación PPT → índice

| PPT (diap.) | Exigencia | Dónde va |
|---|---|---|
| 29–31 | AS-IS, TO-BE y brechas de negocio | 3.1.5.4, 3.1.5.5, 3.1.6 |
| 32 | Principios de negocio | 3.1.1 |
| 33 | Catálogo de capacidades, matriz capacidad–organización | 3.1.2.1, 3.1.3.1 |
| 35 | Diagrama de servicio e información de negocio | 3.1.5.1 |
| 36 | Descomposición funcional | 3.1.5.2 |
| 37 | Ciclo de vida del producto o servicio | 3.1.5.3 |
| 38 | Mapa de capacidades (procesos, servicios, stakeholders, áreas) | 3.1.4 |
| 39 | Mapa de brechas de negocio | 3.1.6.1 |
| 40–42 | Línea base, objetivo y brechas de aplicaciones | 3.2.5.1, 3.2.5.2, 3.2.6 |
| 44 | Principios de aplicaciones | 3.2.1 |
| 45 | Catálogo de aplicaciones e interfaces | 3.2.2.1, 3.2.2.2 |
| 46 | Matrices CRUD y aplicación–capacidad | 3.2.3.1, 3.2.3.2 |
| 47 | Mapa de capacidades de aplicaciones (apps, interfaces, SaaS) | 3.2.4 |
| 48 | Diagramas ArchiMate y brechas de aplicaciones (ETL, ESB) | 3.2.5, 3.2.6 |
| 50–52 | BD relacional y NoSQL, motor e instancia, ETL | 1.7.1, 3.3.2.2, 3.3.5.4 |
| 53 | Principios de datos | 3.3.1 |
| 54 | Catálogo de entidades y de BD | 3.3.2.1, 3.3.2.2 |
| 55 | Mapa de capacidades de datos | 3.3.4 |
| 56 | Matrices CRUD y datos–proceso | 3.3.3 |
| 57 | Diagramas ArchiMate y brechas de datos | 3.3.5, 3.3.6 |
| 59–61 | Redes, seguridad perimetral, nodos, servidores, SO, cloud | 1.7.3, 1.7.4, 3.4.5 |
| 62 | AS-IS y TO-BE de tecnología | 3.4.5.1 a 3.4.5.5 |
| 63 | Principios de tecnología (HA, cluster, balanceador) | 3.4.1, 3.4.6.2 |
| 64 | Catálogo de servidores y de dispositivos de comunicación | 3.4.2.1, 3.4.2.2 |
| 65 | Mapa de capacidades de tecnología | 3.4.4 |
| 66 | Matrices aplicación–tecnología y servidor–ubicación | 3.4.3 |
| 67 | Diagramas ArchiMate y brechas de tecnología (WAF) | 3.4.5.5, 3.4.7 |
| Enunciado TF | Capacidad computacional | 3.4.4.3 |
| Enunciado TF | Data center, cloud, integraciones, ciberseguridad | 3.4.5.2 a 3.4.5.5 |
| Enunciado TF | Continuidad: respaldo, HA, perímetro | 3.4.6 |
| Enunciado TF | Roadmap, inversión, desmantelamiento, gobierno | Cap. 4 y 5 |
| Apuntes | Arquitectura integral al final | 3.5 |
