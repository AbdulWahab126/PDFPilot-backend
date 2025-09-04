from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import uvicorn
from src.routers.pdf import router

app = FastAPI(
    title="PDFPilot",
    description=(
        "AI-powered CAG service for PDFs. "
        "Upload a document, ask questions, get contextual answers."
    ),
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1", tags=["Routes"])


# Simple HTML & CSS page that represent the PDFPilot
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>PDFPilot</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style>
            body{
                margin:0;
                height:100vh;
                display:flex;
                align-items:center;
                justify-content:center;
                background:linear-gradient(135deg,#667eea 0%, #764ba2 100%);
                font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
            }
            .card{
                background:#fff;
                border-radius:16px;
                box-shadow:0 8px 32px rgba(0,0,0,.2);
                padding:48px 56px;
                max-width:420px;
                text-align:center;
            }
            .card h1{
                margin:0 0 8px;
                font-size:32px;
                color:#333;
            }
            .card p{
                margin:0 0 24px;
                font-size:18px;
                color:#555;
            }
            .card a.btn{
                display:inline-block;
                background:#667eea;
                color:#fff;
                padding:12px 24px;
                border-radius:8px;
                text-decoration:none;
                font-weight:600;
                transition:background .2s;
            }
            .card a.btn:hover{
                background:#5a67d8;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>PDFPilot</h1>
            <p>AI-powered Chat-Attached-to-GPT for PDFs</p>
            <a class="btn" href="/docs">Explore API</a>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="127.0.0.1", port=8000, reload=True
    )  # replace app with "main:app" in prod
