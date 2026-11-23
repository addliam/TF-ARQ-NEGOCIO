# Diagramas 3.1: Arquitectura de negocio

Especificación de los diagramas. Se generan con `python negocio/generar_negocio.py`, que crea `negocio_3_1.archimate` (se abre en Archi) y exporta F1 a F7 en PNG usando Archi en línea de comandos. Usa **solo elementos de la capa de negocio (amarillo)**, salvo en el mapa de capacidades, donde las capacidades son elementos de estrategia.

Notación: `Tipo: Nombre`. Relaciones: `A --tipo--> B`.

---

## F1. Mapa de capacidades AS-IS (3.1.4.1, reemplaza la imagen de 2.3)
Agrupaciones (Grouping), cada una con capacidades (Capability):
- **Front office:** Gestión de citas · Gestión de orientación al paciente · Gestión de cobros
- **Middle office:** Gestión de agendas médicas (vacía en la práctica; marcar con una nota: "turno controlado por voucher")
- **Back office core:** Atención médica ambulatoria · Gestión de apoyo al diagnóstico · Gestión farmacéutica · Gestión de terapia y rehabilitación · Gestión de historias clínicas
- **Back office soporte:** Gestión administrativa · Gestión financiera y contable · Gestión de recursos humanos · Gestión de compras y abastecimiento · Gestión de la infraestructura · Gestión pastoral y de responsabilidad social

No llevan actores, procesos, sistemas ni bloque de TI.

## F2. Mapa de capacidades TO-BE (3.1.4.2)
Igual que F1, y en el **middle office** se agregan:
- Gestión de turnos (nueva)
- Gestión de la información al paciente (nueva)
- Gestión del desempeño de la atención (nueva)

Las capacidades nuevas se resaltan con un borde grueso o con una nota "Nueva".

## F3. Servicio e información de negocio (3.1.5.1)
Elementos:
- Business Service: SN-02 Gestión de citas, SN-03 Cobro, SN-04 Gestión de turnos, SN-05 Información al paciente, SN-06 Atención médica, SN-08 Farmacéutico
- Business Object: Solicitud de atención, Cita, Comprobante de pago, Turno, Aviso de turno, Historia clínica, Receta u orden

Relaciones (access):
- SN-02 --access(write)--> Cita
- SN-03 --access(read)--> Cita
- SN-03 --access(write)--> Comprobante de pago
- SN-04 --access(read)--> Comprobante de pago
- SN-04 --access(write)--> Turno
- SN-05 --access(read)--> Turno
- SN-05 --access(write)--> Aviso de turno
- SN-06 --access(read)--> Turno
- SN-06 --access(write)--> Historia clínica
- SN-06 --access(write)--> Receta u orden
- SN-08 --access(read)--> Receta u orden

## F4. Descomposición funcional (3.1.5.2)
- Business Function raíz: **Atención ambulatoria**, con 5 funciones hijas (composition):
  1. Admisión del paciente → Orientar, Gestionar cita, Cobrar el servicio
  2. Gestión del flujo de atención → Generar turno, Actualizar turno, Informar estado del turno, Llamar al paciente
  3. Atención clínica → Atender consulta, Registrar historia clínica, Emitir receta u orden
  4. Apoyo al diagnóstico y tratamiento → Realizar exámenes, Dispensar medicamentos, Brindar terapia
  5. Gestión institucional → Monitorear desempeño, Gestionar personal, Gestionar compras, Gestionar finanzas

## F5. Ciclo de vida de la atención (3.1.5.3)
Business Event por estado, unidos por triggering:
Solicitada → Agendada → Pagada → En espera → Llamada → En consulta → Atendida → Cerrada o derivada
- Bucle: En espera → **Turno actualizado** → En espera (disparado por el evento Cambio en el avance de la consulta)

## F6. Modelo de negocio AS-IS (3.1.5.4, reemplaza la imagen de 2.6)
Igual al diagrama actual del 2.6, **eliminando** los elementos celestes: Historia Clínica del paciente (objeto de datos), Receta/Orden de exámenes (objeto de datos), Servicio de Historia Clínica digital y el sistema de historias clínicas. Se mantiene el objeto de negocio amarillo Receta/Orden de exámenes.

Actores: Paciente, Recepcionista, Cajero, Enfermera, Médico, Químico-Farmacéutico.
Flujo: Solicitud de una consulta (evento) → Reservar cita → Realizar triaje → Cobro de pago de cita reservada (registra Comprobante de pago) → Recepcionar comprobante → Esperar turno de atención / Atender consulta médica (registra Receta/Orden) → Proporcionar medicamentos / Recepcionar orden de exámenes.

## F7. Modelo de negocio TO-BE (3.1.5.5)
Actores (Business Actor) y asignación (assignment):
- Paciente; Recepcionista → Gestionar cita; Cajero → Registrar pago; Enfermera → Gestionar turno, Actualizar turno, Informar estado del turno; Médico → Atender consulta médica; Químico-farmacéutico → Dispensar medicamentos

Procesos y eventos (triggering):
- Evento **Solicitud de atención** → Gestionar cita → Registrar pago → Gestionar turno → Informar estado del turno
- Gestionar turno → Atender consulta médica → Dispensar medicamentos
- Atender consulta médica → evento **Cambio en el avance de la consulta** → Actualizar turno → evento **Turno actualizado** → Informar estado del turno

Servicios (realization proceso → servicio; serving servicio → Paciente):
- Gestionar cita → Servicio de gestión de citas
- Registrar pago → Servicio de cobro
- Gestionar turno y Actualizar turno → Servicio de gestión de turnos
- Informar estado del turno → Servicio de información al paciente
- Atender consulta médica → Servicio de atención médica

Objetos de negocio (access): Registrar pago → Comprobante de pago; Gestionar turno → Turno; Actualizar turno → Turno; Atender consulta médica → Historia clínica, Receta.
