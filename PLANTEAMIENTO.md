# Planteamiento Arquitectónico - Plataforma de Bienestar
**Autor:** Daniel Mendoza (Automation & Backend Engineer)

Este documento detalla las decisiones arquitectónicas, de infraestructura y de diseño de datos adoptadas para la migración del sistema de reservas del centro de bienestar desde Google Sheets hacia una plataforma web propietaria, escalable y conectada con n8n.

---

### 1. Aplicacion Web 
*   **Tecnología elegida:** La aplicación web está construida utilizando un backend asíncrono en Python FastAPI acoplado a una interfaz de usuario (frontend) limpia en HTML5, CSS3 y JavaScript Vanilla (puro) sin dependencias de frameworks pesados (como React o Next.js).
*   **Justificación:** En concordancia con el principio de eficiencia operativa de NODENA (*"La tecnología debe simplificar, no complicar"*). Evita el over-engineering y la deuda técnica, garantizando tiempos de carga instantáneos en dispositivos móviles y un empaquetamiento ligero ideal para MVPs de rápido despliegue

### 2. Infraestructura y Alojamiento (Hosting Cloud)
*   **Alojamiento elegido:** La plataforma se encuentra actualmente desplegada en producción real dentro de un servidor privado virtual (VPS) en Hetzner (Alemania), totalmente contenerizada bajo Docker Compose y gobernada perimetralmente por un proxy inverso Nginx nativo con certificados SSL criptográficos de Let's Encrypt
*   **Justificación:** Otorga un control absoluto sobre el entorno, elimina los costos variables de plataformas como Railway o Vercel y permite una interconexión nativa de sub-segundo tiempo con el orquestador n8n alojado en la misma máquina

### 3. Persistencia y Motor de Datos (Base de Datos)
*   **Base de Datos elegida:** **SQLite3 (Relacional y Persistente)** Los datos de clientas, catálogo maestro de servicios, tablas de disponibilidad y el registro histórico de citas se guardan en una base de datos relacional SQLite3, mapeada de forma inmutable mediante volúmenes persistentes de Docker en la VPS.
*   **Justificación:** Es un motor embebido de alta velocidad que almacena la información en un solo archivo plano en disco, eliminando la latencia de red de sockets externos y garantizando la portabilidad total del estado de la aplicación. SQLite3 es la opción más performante del mercado por dos razones científicas:
    1.  **Baja Latencia Extrema:** Al operar como una base de datos embebida en un archivo plano en el disco duro del volumen de Docker, elimina el overhead y las llamadas de red TCP necesarias para comunicarse con un servidor externo (como Supabase o PostgreSQL), ejecutando transacciones en microsegundos.
    2.  **Portabilidad Enterprise:** La base de datos completa se encapsula en un archivo de almacenamiento, permitiendo hacer respaldos o migraciones en caliente en un simple comando de copiado. Se implementaron llaves foráneas (*Foreign Keys*) para amarrar la integridad relacional entre los servicios, recursos disponibles y las citas agendadas de forma inmutable.

### 4. Estructura Mínima de la Aplicación (UX/UI)
La aplicación se organiza en una arquitectura modular de vista única (Single Page Application) optimizada para móviles, estructurada bajo el siguiente mapa de pantallas mínimo::
1. **Pantalla del Cliente (/):** Catálogo dinámico de servicios leídos desde la base de datos y el formulario de agendamiento rápido.
2. **Mis Reservas (/mis-reservas):** Pantalla de consulta individualizada ingresando el número telefónico para verificar el estatus de las citas 
3. **Panel Administrativo (/admin):**  Consola restringida del centro de bienestar para visualizar el consolidado maestro de las citas que ingresan en vivo por la web y WhatsApp.
*  **Justificacion:** Satisface las necesidades del embudo de conversión del cliente final y la operación diaria del negocio en un flujo visual intuitivo y sin fricciones de carga

### 5. Integración e Interconexión con el Bot de WhatsApp (n8n)
El bot de WhatsApp y la plataforma web se conectan de forma desacoplada y asíncrona mediante una API REST corporativa. El bot que corre en n8n no comparte la base de datos directamente con la app; en su lugar, utiliza un nodo HTTP Request para golpear un endpoint seguro en el backend (POST /api/v1/reservar), enviándole un payload estructurado en JSON con las variables recolectadas en el chat

**Justificacion:** Preserva la independencia de las capas del software (patrón de microservicios), aislando el canal de mensajería para que mutaciones o caídas en n8n jamás comprometan la integridad de la base de datos principal de la empresa.

### 6. Diagrama de Flujo e Interconexion

 [ CLIENTA ] ➔ Envia mensaje de WhatsApp ➔ [ PUENTE WAHA / COMPUETA CLARO ]
                                                        │
                                                        ▼
 [ ENDPOINT PYTHON ] 🗄️ 💾 [ SQLite3 ] ◀══ HTTP ═══ [ n8n ORQUESTADOR ]
  /api/v1/reservar       (Persistencia)     POST       (Lógica Conversacional)
         ▲
         │ HTTP POST
         │
 [ INTERFAZ WEB ] 🌿 💻 (Formulario de Reserva en index.html)

