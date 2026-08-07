# PLAN-FRONTEND.md — Helpdesk Core UI

> Roadmap por pasos cortos (~30 min cada uno), ordenados por **dependencia técnica**.
> Cada paso dice: qué sprint cubre, qué archivos toca, qué concepto de React
> introduce y cómo se prueba.

**Contexto:** segundo proyecto, construido sobre el backend ITSM ya entregado
(HD-101 a HD-104). El backend **no se modifica**, salvo el `RegisterView` que
quedó pendiente y que hace falta para la pantalla de registro.

---

## Decisiones confirmadas (2026-08-06)

| Decisión | Elegido | Por qué |
|---|---|---|
| Stack | React 19 + Vite + TypeScript + Tailwind v4 + axios + react-router-dom | Igual que `Castlevania/frontend` |
| Stepper | Adaptado a los **5 estados reales** del backend | El backend ya está entregado y probado; el mockup era referencia visual. `ESCALADO` no existe en el modelo |
| Mensajes de sistema | Solo el de creación, **derivado en el frontend** | Se construye con `fecha_creacion` + `prioridad`, que la API ya devuelve. Cero cambios al backend |
| Pantallas extra | Login · Crear ticket · Registro · Logout | Sin Login la app no funciona (todo el backend exige auth); sin crear ticket un CLIENTE no puede hacer nada |
| Nivel avanzado | **Fuera por ahora** (Optimistic UI / React Query) | El enunciado los marca como opcionales. Se pueden agregar al cierre si sobra tiempo |
| Puerto | `5161` externo / `5173` interno | Ya está en `CORS_ALLOWED_ORIGINS` desde el Paso 0.3 del backend. Castlevania usa 5160 |
| Ubicación | `Proyecto Final/frontend/` | Al lado de `backend/`, mismo repo, mismo `docker-compose.yml` |

---

## Bloque 0 — Cimientos

### Paso F0.1 — Crear el proyecto Vite
- **Comando:** `npm create vite@latest frontend -- --template react-ts`
- **Archivos:** todo `frontend/` (generado)
- **Concepto React:** qué es un componente, qué hace `main.tsx`, qué es JSX
- **Prueba:** `npm run dev` → página por defecto de Vite en el navegador

### Paso F0.2 — Tailwind v4 + paleta del enunciado
- **Archivos:** `vite.config.ts`, `src/index.css`, `package.json`
- **Qué se hace:** plugin de Tailwind + bloque `@theme` con los 4 colores del enunciado (`#0D9488`, `#EF4444`, `#F59E0B`, `#F3F4F6`)
- **Cubre:** parte de **SUP-201-1** (variables de la paleta)
- **Prueba:** un `<div className="bg-teal">` se pinta del color correcto

### Paso F0.3 — Docker: el tercer servicio
- **Archivos:** `frontend/Dockerfile` (nuevo), `docker-compose.yml` (editar)
- **Qué se hace:** servicio `frontend` con `build: ./frontend`, puerto `5161:5173`, sin tocar `db` ni `backend`
- **Prueba:** `docker compose up -d` levanta los tres contenedores

### Paso F0.4 — `api/client.ts` y `types.ts`
- **Archivos nuevos:** `src/api/client.ts`, `src/types.ts`
- **Qué se hace:** instancia de axios con `baseURL: 'http://localhost:8001/api'` y **`withCredentials: true`** (la línea que hace funcionar las cookies HttpOnly); tipos TS de `Ticket`, `Comentario`, `Usuario`, `Departamento` — copiados de lo que devuelve tu API real
- **Concepto React/TS:** por qué tipar las respuestas de la API
- **Prueba:** desde la consola del navegador, una petición a `/tickets/` devuelve 401 (aún no hay sesión) — eso confirma que la URL es correcta

---

## Bloque 1 — Autenticación

### Paso F1.0 — `RegisterView` en el backend *(prerrequisito, Paso 5.5 pendiente)*
- **Archivos:** `backend/core/serializers.py` (nuevo), `backend/core/views.py`, `backend/core/urls.py`
- **Qué se hace:** `POST /api/register/` con `AllowAny`, rol forzado a `CLIENTE` server-side
- **Prueba:** registro sin sesión → `201`, usuario creado con `rol=CLIENTE`

### Paso F1.1 — `AuthContext`
- **Archivo nuevo:** `src/context/AuthContext.tsx`
- **Qué se hace:** al montar la app llama a `GET /me/`; expone `isAuthenticated`, `user`, `login()`, `logout()`, `loading`
- **Conceptos React:** `useState`, `useEffect`, Context API, por qué el estado de sesión es global
- **Prueba:** un `console.log` del contexto muestra `loading: false, isAuthenticated: false`

### Paso F1.2 — Rutas + `ProtectedRoute`
- **Archivos:** `src/App.tsx`, `src/components/ProtectedRoute.tsx` (nuevo)
- **Conceptos React:** react-router-dom, rutas anidadas, `<Outlet />`, `<Navigate />`
- **Prueba:** entrar a `/tickets` sin sesión rebota a `/login`

### Paso F1.3 — Página de Login
- **Archivo nuevo:** `src/pages/Login.tsx`
- **Qué se hace:** formulario controlado → `POST /token/` → `GET /me/` → `login(data)` → redirigir
- **Conceptos React:** formularios controlados, `onSubmit`, `useNavigate`, manejo de errores
- **Prueba:** login correcto entra al panel; login incorrecto muestra mensaje de error

### Paso F1.4 — Registro y Logout
- **Archivos:** `src/pages/Registro.tsx` (nuevo), `src/components/BotonLogout.tsx` (nuevo)
- **Prueba:** registrar un cliente nuevo, entrar con él, cerrar sesión y volver al login

---

## Bloque 2 — Vista Lista (Master)

### Paso F2.1 — Header global y layout base — **SUP-201-1**
- **Archivos:** `src/layouts/DashboardLayout.tsx` (nuevo)
- **Qué se hace:** header teal de 60px, `body` en `100vh` con `overflow: hidden`, contenedor principal que ocupa el resto
- **Criterio de aceptación:** la página nunca scrollea completa, solo sus secciones internas
- **Prueba:** redimensionar la ventana — el header no se mueve y no aparece scroll global

### Paso F2.2 — Tabla de tickets — **SUP-201-2**
- **Archivos:** `src/pages/ListaTickets.tsx` (nuevo)
- **Qué se hace:** `GET /tickets/`, columnas ID / Asunto / Solicitante / Prioridad / Estado / SLA
- **Conceptos React:** `useEffect` para pedir datos, `.map()` para renderizar filas, la prop `key`, estados de `loading` y `error`
- **Criterio de aceptación:** `<thead>` con `position: sticky`
- **Prueba:** con más de 20 tickets, al scrollear el encabezado se queda fijo

### Paso F2.3 — Badges de colores — **SUP-201-2**
- **Archivo nuevo:** `src/components/Badge.tsx`
- **Qué se hace:** componente que recibe el valor y devuelve el color correcto (CRITICA→rojo, ALTA→amarillo, resto→teal)
- **Conceptos React:** props, componentes reutilizables, renderizado condicional
- **Prueba:** cada prioridad y estado se pinta con su color

### Paso F2.4 — Columna SLA con cuenta regresiva
- **Archivo:** `src/components/Badge.tsx` o helper aparte
- **Qué se hace:** convertir `fecha_vencimiento_sla` (fecha absoluta de la API) en "45 mins restantes"; rojo si faltan menos de 2h
- **Prueba:** un ticket forzado a vencer en 30 min se ve en rojo

### Paso F2.5 — Barra de filtros — **SUP-201-2**
- **Archivo:** `src/pages/ListaTickets.tsx`
- **Los tres filtros:** "Todos" (`GET /tickets/`) · "Solo mis tickets" (filtrado en cliente por `solicitante`) · **"Urgentes (SLA < 2h)"** (`GET /tickets/urgencias/` — encaja exacto con tu endpoint de HD-102.2)
- **Conceptos React:** estado que controla qué se muestra, clase `active` condicional
- **Prueba:** el filtro de urgentes trae solo los que vencen pronto

---

## Bloque 3 — Vista Detalle (estructura)

> Nota: se construye el contenedor 30/70 (SUP-201-4) **antes** que el stepper
> (SUP-201-3), aunque el sprint los numere al revés. Razón: el stepper vive
> dentro de esa estructura; hacerlo al revés obligaría a rehacer el contenedor.

### Paso F3.1 — Master-Detail y botón Volver
- **Archivos:** `src/App.tsx`, `src/pages/DetalleTicket.tsx` (nuevo)
- **Qué se hace:** ruta `/tickets/:id`; clic en una fila navega al detalle; botón "← Volver a la lista"
- **Conceptos React:** parámetros de ruta, `useParams`, `useNavigate`
- **Criterio de aceptación:** flujo Master-Detail con botón volver funcional
- **Prueba:** ida y vuelta entre lista y detalle sin recargar la página

### Paso F3.2 — Layout 30/70 — **SUP-201-4**
- **Archivo:** `src/pages/DetalleTicket.tsx`
- **Qué se hace:** flexbox con `flex: 0 0 30%` y `flex: 1`; el `min-height: 0` que hace funcionar el scroll de los hijos
- **Criterio de aceptación:** proporción 30/70 estricta
- **Prueba:** medir en el inspector del navegador

### Paso F3.3 — Panel izquierdo (30%) — **SUP-201-4**
- **Archivo nuevo:** `src/components/PanelDetalle.tsx`
- **Qué se hace:** ID, alerta de SLA en rojo, prioridad, solicitante, agente asignado
- **Prueba:** los datos coinciden con lo que devuelve `GET /tickets/{id}/`

### Paso F3.4 — Stepper de estados — **SUP-201-3**
- **Archivo nuevo:** `src/components/Stepper.tsx`
- **Los 5 pasos reales:** NUEVO → EN_REVISION → ESPERANDO_CLIENTE → RESUELTO → CERRADO
- **Qué se hace:** líneas conectoras con `::after`; teal para completado, amarillo para el actual
- **Conceptos React:** derivar UI de datos (el índice del estado actual decide los colores)
- **Prueba:** cambiar el estado del ticket y ver avanzar el stepper

### Paso F3.5 — Cambiar el estado desde el stepper
- **Archivo:** `src/components/Stepper.tsx`
- **Qué se hace:** `PATCH /tickets/{id}/` al hacer clic en un paso; **mostrar el error 400** cuando la transición está prohibida
- **Prueba:** intentar NUEVO → CERRADO muestra el mensaje de tu validación de HD-101.2 en pantalla

---

## Bloque 4 — Panel de chat — **SUP-201-5**

### Paso F4.1 — Historial de comentarios
- **Archivo nuevo:** `src/components/HiloComentarios.tsx`
- **Qué se hace:** `GET /tickets/{id}/comentarios/`, con `overflow-y: auto` propio
- **Criterio de aceptación:** scroll aislado — solo el chat scrollea
- **Prueba:** con 20 comentarios, el stepper y la textarea no se mueven

### Paso F4.2 — Mensaje de sistema derivado
- **Archivo:** `src/components/HiloComentarios.tsx`
- **Qué se hace:** primer mensaje del hilo, fondo amarillo tenue: *"Ticket creado el {fecha_creacion} con prioridad {prioridad}"*, construido con datos que la API ya devuelve
- **Criterio de aceptación:** diferenciar visualmente mensajes de sistema
- **Prueba:** aparece arriba del todo, con estilo distinto a los comentarios reales

### Paso F4.3 — Área de respuesta fija
- **Archivo:** `src/components/HiloComentarios.tsx`
- **Qué se hace:** textarea + botón "Guardar Comentario" → `POST /tickets/{id}/comentarios/`, recargar el hilo
- **Criterio de aceptación:** textarea siempre visible, no desaparece al scrollear
- **Prueba:** comentar como CLIENTE en un ticket `ESPERANDO_CLIENTE` → aparece el comentario **y el stepper avanza solo** (tu trigger atómico de HD-104.2 visto desde la UI)

---

## Bloque 5 — Crear ticket

### Paso F5.1 — Modal/formulario de creación
- **Archivos:** `src/components/ModalCrearTicket.tsx` (nuevo), `src/pages/ListaTickets.tsx`
- **Qué se hace:** título, descripción, prioridad, departamento → `POST /tickets/`
- **A demostrar:** no se manda `solicitante` ni `fecha_vencimiento_sla` — los pone el servidor
- **Prueba:** crear un ticket CRITICA y ver que la columna SLA ya trae +4h

---

## Bloque 6 — Cierre

### Paso F6.1 — Checklist de los 4 criterios de aceptación
- **Archivo nuevo:** `CHECKLIST-FRONTEND.md`

### Paso F6.2 — Los tres contenedores juntos
- **Prueba final:** `docker compose up -d` → `db` + `backend` + `frontend` funcionando de punta a punta

### Paso F6.3 — Notas y preguntas de defensa
- Igual que en el backend

---

## Riesgos conocidos

1. **Nunca has usado React.** Los Bloques 0 y 1 van a sentirse lentos: ahí aparecen `useState`, `useEffect`, Context y rutas todos juntos. Del Bloque 2 en adelante se repite el mismo patrón y acelera.
2. **El backend debe estar corriendo** para ver cualquier dato. Primer reflejo ante una pantalla vacía: `docker compose ps`.
3. **CORS.** Si aparece un error de CORS en la consola del navegador, revisar que el frontend esté en el puerto **5161**, que es el único autorizado en `settings.py`.
4. **Las cookies HttpOnly no se ven desde JavaScript.** Es a propósito (protección XSS). Para depurar la sesión hay que mirar la pestaña Network/Application del navegador, no `document.cookie`.
