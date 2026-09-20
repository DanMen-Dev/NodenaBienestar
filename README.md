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
