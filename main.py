import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="clave-local-de-prueba"
)

oauth = OAuth()

oauth.register(
    name="keycloak",
    client_id="hola-mundo-app",
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    server_metadata_url=(
        "http://localhost:8080/realms/s2026q2a-kc/"
        ".well-known/openid-configuration"
    ),
    client_kwargs={
        "scope": "openid profile email"
    },
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = request.session.get("user")

    if not user:
        return """
        <h1>Hola Mundo</h1>
        <a href="/login">Iniciar sesión</a>
        """

    username = user.get("preferred_username") or user.get("email")

    return f"""
    <h1>Hola Mundo, {username}</h1>
    <a href="/logout">Cerrar sesión</a>
    """


@app.get("/login")
async def login(request: Request):
    redirect_uri = "http://localhost:8000/callback"

    return await oauth.keycloak.authorize_redirect(
        request,
        redirect_uri
    )


@app.get("/callback")
async def callback(request: Request):
    token = await oauth.keycloak.authorize_access_token(request)

    user = token.get("userinfo")

    if not user:
        user = await oauth.keycloak.userinfo(token=token)

    request.session["user"] = dict(user)

    return RedirectResponse(url="/")


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()

    return RedirectResponse(url="/")