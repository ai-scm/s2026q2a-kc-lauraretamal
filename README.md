# Keycloak + Google + FastAPI

Integración de Keycloak con Google como proveedor externo de identidad y una aplicación web desarrollada con FastAPI mediante OpenID Connect.

## Arquitectura

```text
Google
   │
   │ Autenticación
   ↓
Keycloak
   │
   │ OpenID Connect
   ↓
FastAPI
```

## Tecnologías

* Keycloak
* Docker
* Google Cloud
* OpenID Connect
* Python
* FastAPI
* Authlib

## Keycloak

Keycloak se ejecuta localmente mediante Docker utilizando:

```text
quay.io/keycloak/keycloak:latest
```

Se utiliza el modo `start-dev` y un volumen para persistir los datos:

```text
./keycloak_data:/opt/keycloak/data
```

Keycloak está disponible en:

```text
http://localhost:8080
```

### Realm

Se creó el realm:

```text
s2026q2a-kc
```

independiente del realm `master`.

### Cliente

La aplicación se registró como:

```text
hola-mundo-app
```

Configuración principal:

* OpenID Connect
* Client Authentication: Enabled
* Standard Flow: Enabled
* Authorization: Disabled

Redirect URI:

```text
http://localhost:8000/callback
```

## Google Identity Provider

Google se configuró como proveedor externo de identidad dentro del realm `s2026q2a-kc`.

Se registró una aplicación OAuth en Google Cloud y las credenciales generadas se configuraron en Keycloak.

Redirect URI utilizada por Google:

```text
http://localhost:8080/realms/s2026q2a-kc/broker/google/endpoint
```

Esto permite que Keycloak delegue la autenticación en Google y reciba posteriormente la respuesta de autenticación.

## Aplicación

Se desarrolló una aplicación web sencilla con FastAPI.

La integración con Keycloak se realiza mediante Authlib utilizando OpenID Connect y el flujo Authorization Code.

La aplicación permite:

* Iniciar sesión mediante Keycloak.
* Autenticarse mediante Google.
* Recibir la respuesta de autenticación mediante un callback.
* Mostrar la información del usuario autenticado.
* Cerrar sesión.

Después de autenticarse correctamente, la aplicación muestra:

```text
Hola Mundo, <usuario>
```

## Ejecución

Activar el entorno virtual:

```bash
source venv/bin/activate
```

Configurar el Client Secret:

```bash
export KEYCLOAK_CLIENT_SECRET="CLIENT_SECRET"
```

Iniciar la aplicación:

```bash
uvicorn main:app --host localhost --port 8000
```

La aplicación estará disponible en:

```text
http://localhost:8000
```

## Flujo de autenticación

```text
Usuario
   ↓
FastAPI
   ↓
Keycloak
   ↓
Google
   ↓
Keycloak
   ↓
FastAPI
   ↓
Hola Mundo, <usuario>
```
