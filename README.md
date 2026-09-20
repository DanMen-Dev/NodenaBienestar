# 🌿 Plataforma de Reservas Digitales - Centro de Bienestar (NODENA)

Esta plataforma web es un sistema inteligente diseñado para automatizar por completo el control de citas, clases de Pilates, Yoga y masajes de un centro de bienestar. 

Su objetivo principal es jubilar las viejas e inestables hojas de cálculo de Google Sheets por una aplicación propia y moderna que centraliza todo el negocio.

### 👥 ¿Cómo funciona en palabras llanas?

La plataforma opera bajo dos canales automáticos que se comunican con la misma base de datos:

1. **La Página Web:** Las clientas ingresan desde su computadora o celular a una dirección de internet, ven los servicios actualizados con sus respectivos precios y duraciones, rellenan un formulario simple con su nombre y teléfono, y agendan su cita al instante recibiendo un código de confirmación.
2. **El Bot de WhatsApp:** Si una clienta prefiere chatear por el celular en lugar de entrar a la web, el asistente virtual de WhatsApp (orquestado en n8n) habla con ella, le pide los datos y registra la reserva en el mismo libro contable de la empresa sin que ningún empleado tenga que tipear nada a mano.
3. **El Panel del Centro:** Los dueños o recepcionistas del local cuentan con una pantalla administrativa privada donde ven actualizarse en tiempo real una tabla con todas las citas que van entrando en el día, indicando claramente si la clienta reservó desde la página web o chateando por WhatsApp.

---

## 🤖 Fase 3 — Conexión e Integración con el Bot de n8n

Para conectar el bot conversacional de WhatsApp alojado en n8n con esta plataforma en sustitución de Google Sheets, se configura un único nodo **HTTP Request** dentro del lienzo del flujo, parametrizado bajo las siguientes especificaciones técnicas:

1. **Method:** `POST`
2. **URL:** `https://nodenabienestar.brecha-cero.com/api/v1/reservar`
3. **Authentication:** Ninguna (o API Key Token si se requiere producción restringida).
4. **Send Body:** `true`
5. **Body Parameters (JSON):** Se inyectan las llaves dinámicas mapeando los datos recolectados por el bot conversacional durante la charla con la clienta:
   - `nombre`: `{{ $json.body.cliente_nombre }}`
   - `telefono`: `{{ $json.body.cliente_telefono }}`
   - `fecha`: `{{ $json.body.fecha_reserva }}`
   - `servicio_id`: `{{ $json.body.servicio_seleccionado_id }}`

Al dispararse el nodo, n8n transmite el payload JSON, el backend asíncrono procesa la reserva en milisegundos, inserta la cita en SQLite y le retorna a n8n el código único de confirmación (`cita_id`) para que el bot se lo envíe de vuelta a la clienta por WhatsApp en un solo flujo continuo y automatizado.
