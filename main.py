from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse


app = FastAPI(
    title="SUPERGAS Documentos QR",
    version="1.0.0"
)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=()"
    )

    return response


BASE_DIR = Path(__file__).resolve().parent
DOCUMENTOS_DIR = BASE_DIR / "documentos"


DOCUMENTOS = {
    "manual-manejo-seguro-glp": {
        "archivo": "manual-glp.pdf",
        "nombre_descarga": "Manual-Manejo-Seguro-GLP.pdf",
    },

    "manual-usuario": {
        "archivo": "manual-usuario.pdf",
        "nombre_descarga": "Manual-Usuario.pdf",
    },
}


@app.get("/")
def inicio():
    return {
        "status": "ok",
        "message": "SUPERGAS Documentos QR funcionando"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/documentos/{slug}")
def ver_documento(slug: str):

    documento = DOCUMENTOS.get(slug)

    if not documento:
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    archivo = DOCUMENTOS_DIR / documento["archivo"]

    if not archivo.exists():
        raise HTTPException(
            status_code=404,
            detail="Archivo PDF no disponible"
        )

    return FileResponse(
        path=archivo,
        media_type="application/pdf",
        filename=documento["nombre_descarga"],
        content_disposition_type="inline"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001
    )