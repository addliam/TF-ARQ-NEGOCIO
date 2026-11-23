# Supuestos del negocio (validados por defecto)

Se usan para completar el TF donde no hay datos reales del policlínico. En el informe se presentan como supuestos del equipo.

| # | Tema | Supuesto |
|---|---|---|
| 1 | Historias clínicas | Software de gestión de historias clínicas, licenciado e instalado en un servidor local (on-premise), con BD SQL Server. |
| 2 | Caja y comprobantes | Módulo de caja propio más facturación electrónica SUNAT mediante un proveedor (OSE/PSE). No está integrado con el software de historias. |
| 3 | Reserva web | Formulario de la página web que llega al WhatsApp Business normal (no la API). La agenda se lleva en Excel o en un cuaderno por especialidad. |
| 4 | Farmacia y laboratorio | Farmacia: software de inventario y ventas local. Laboratorio: cuaderno y Excel; los resultados se entregan impresos. |
| 5 | Back office | Contabilidad tercerizada con software contable. Los médicos se incorporan por convenio y cobran por honorarios con un porcentaje por consulta. Administración trabaja con Office y correo. |
| 6 | Infraestructura AS-IS | 1 servidor físico, router del ISP, switches sin administrar, unas 30 PC, sin firewall dedicado, respaldo manual en disco externo, sin alta disponibilidad. Un encargado de TI. |
| 7 | Volumen | Unos 350 pacientes/día, 20 consultorios, 27 especialidades, más de 60 médicos y 2 turnos. |
| 8 | Gobierno | Director (fraile franciscano) y administrador general. Las inversiones grandes las aprueba la parroquia/Orden. |
| 9 | Financiamiento | Fondos propios más donaciones; tope de S/ 150 000. |
| 10 | Enfoque TO-BE | Híbrido. Azure para el sistema de turnos, el motor de IA y las notificaciones. El software de historias se queda local, integrado mediante ESB y ETL. Pantallas de turno y WhatsApp Business API mediante un proveedor. |
| 11 | Seguros | Sin EPS ni SIS: atención particular a tarifa social, más convenios parroquiales. |
