from fastapi import FastAPI
from app.routers import clientes, mesas, reservas, estadisticas

app = FastAPI(title="API Sistema de Reservas - La Mesa Dorada", version="0.1.0")

# Incluir routers
app.include_router(clientes.router)
app.include_router(mesas.router)
app.include_router(reservas.router)
app.include_router(estadisticas.router)

# Endpoint raíz para verificar que la API está funcionando
@app.get("/")
def root():
    return {"mensaje": "API de La Mesa Dorada funcionando (Creado por SAAD FAHAM)"}

# Endpoint para obtener la versión de la API
@app.get("/version")
def version():
    return {"version": "0.1.0"}

