import httpx
from fastapi import FastAPI, Request, HTTPException, WebSocket
from fastapi.responses import JSONResponse, Response
import os
import websockets
import asyncio

app = FastAPI(title="API Gateway")

# Service URLs (Environment Variables with defaults for Docker)
AUTH_SERVICE = os.getenv("AUTH_SERVICE", "http://auth-service:8000")
INVENTORY_SERVICE = os.getenv("INVENTORY_SERVICE", "http://inventory-service:8000")
ORDER_SERVICE = os.getenv("ORDER_SERVICE", "http://order-service:8000")
ANALYTICS_SERVICE = os.getenv("ANALYTICS_SERVICE", "http://analytics-service:8000")
AI_SERVICE = os.getenv("AI_SERVICE", "http://ai-service:8000")

# WebSocket Target (Assuming Order Service handles real-time alerts for now)
# If not, we might need a dedicated Notification Service. 
# For now, let's point to Order Service as it generates order events.
WEBSOCKET_SERVICE = ORDER_SERVICE.replace("http", "ws") 

async def forward_request(service_url: str, path: str, request: Request):
    async with httpx.AsyncClient() as client:
        try:
            url = f"{service_url}{path}"
            headers = dict(request.headers)
            headers.pop("host", None) # Let httpx set host
            headers.pop("content-length", None)
            
            # Simple body forwarding
            body = await request.body()
            
            resp = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                data=body, 
                params=request.query_params,
                timeout=60.0
            )
            
            return Response(
                content=resp.content,
                status_code=resp.status_code,
                headers=dict(resp.headers)
            )
        except httpx.RequestError as e:
            return JSONResponse(status_code=503, content={"detail": f"Service Unavailable: {str(e)}"})

# WebSocket Proxy
@app.websocket("/ws/{client_id}")
async def websocket_proxy(client: WebSocket, client_id: str):
    await client.accept()
    # Connect to backend WebSocket
    try:
        async with websockets.connect(f"{WEBSOCKET_SERVICE}/ws/{client_id}") as target_ws:
            # Bi-directional forwarding
            async def forward_client_to_target():
                try:
                    while True:
                        data = await client.receive_text()
                        await target_ws.send(data)
                except Exception:
                    pass

            async def forward_target_to_client():
                try:
                    while True:
                        data = await target_ws.recv()
                        await client.send_text(data)
                except Exception:
                    pass

            await asyncio.gather(forward_client_to_target(), forward_target_to_client())
    except Exception as e:
        print(f"WebSocket Error: {e}")
        await client.close(code=1011)

# Routes
@app.api_route("/api/v1/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def auth_proxy(path: str, request: Request):
    return await forward_request(AUTH_SERVICE, f"/api/v1/auth/{path}", request)

@app.api_route("/api/v1/inventory/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def inventory_proxy(path: str, request: Request):
    return await forward_request(INVENTORY_SERVICE, f"/api/v1/inventory/{path}", request)
    
@app.api_route("/api/v1/suppliers/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def supplier_proxy(path: str, request: Request):
    return await forward_request(INVENTORY_SERVICE, f"/api/v1/suppliers/{path}", request)

@app.api_route("/api/v1/orders/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def orders_proxy(path: str, request: Request):
    return await forward_request(ORDER_SERVICE, f"/api/v1/orders/{path}", request)

@app.api_route("/api/v1/analytics/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def analytics_proxy(path: str, request: Request):
    return await forward_request(ANALYTICS_SERVICE, f"/api/v1/analytics/{path}", request)

@app.api_route("/api/v1/ai/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def ai_proxy(path: str, request: Request):
    return await forward_request(AI_SERVICE, f"/api/v1/ai/{path}", request)

@app.get("/health")
def health():
    return {"status": "ok"}
