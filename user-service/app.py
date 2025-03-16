from fastapi import FastAPI
from consul import Consul
import uvicorn
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}

def register():
    consul = Consul(host='127.0.0.1', port=8500)
    consul.agent.service.register(
        name="user-service",
        service_id="user-service-1",
        address="127.0.0.1",
        port=8000,
        tags=["user-service"],
    )


if __name__ == "__main__":
    register()
    uvicorn.run(app, host="0.0.0.0", port=8000)