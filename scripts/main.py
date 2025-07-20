#!/usr/bin/env python3
"""
Production FastAPI application for Google Cloud Run
"""
import os
import sys
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Production configuration
PORT = int(os.environ.get("PORT", 8080))  # Cloud Run uses PORT env variable
HOST = "0.0.0.0"

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import AI agents
try:
    from agents.doc_agent.doc_generator import DocumentationAgent
    DOCUMENTATION_AGENT_AVAILABLE = True
    logger.info("✅ DocumentationAgent imported successfully")
except ImportError as e:
    DOCUMENTATION_AGENT_AVAILABLE = False
    logger.warning(f"⚠️ DocumentationAgent not available: {e}")

# Global agent instances
agents = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting AI Development Automation on Cloud Run...")
    try:
        if DOCUMENTATION_AGENT_AVAILABLE:
            agents["documentation"] = DocumentationAgent()
            logger.info("📝 DocumentationAgent initialized")
        else:
            logger.warning("DocumentationAgent is unavailable; skipping initialization")
    except Exception as e:
        logger.error(f"❌ Failed to initialize agents: {e}")
    yield
    logger.info("🛑 Shutting down AI Development Automation")

app = FastAPI(
    title="AI Development Automation",
    description="Cloud-deployed intelligent automation for development workflows",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class DocumentationRequest(BaseModel):
    file_path: str
    code_content: str

class DocumentationResponse(BaseModel):
    file_path: str
    documentation: str
    status: str
    processing_time: float

@app.get("/")
async def root():
    return {
        "status": "running",
        "message": "🤖 AI Development Automation - Cloud Deployed",
        "agents_available": list(agents.keys()),
        "deployment": "Google Cloud Run",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/agents/documentation/generate", response_model=DocumentationResponse)
async def generate_documentation(request: DocumentationRequest):
    """Generate documentation for the provided code."""
    if "documentation" not in agents:
        raise HTTPException(status_code=503, detail="Documentation agent not available")

    start = datetime.now()
    logger.info(f"📝 Processing documentation request for: {request.file_path}")

    try:
        documentation = await agents["documentation"].generate_documentation(
            file_path=request.file_path,
            code_content=request.code_content
        )
        duration = (datetime.now() - start).total_seconds()
        return DocumentationResponse(
            file_path=request.file_path,
            documentation=documentation,
            status="success",
            processing_time=duration
        )
    except Exception as e:
        duration = (datetime.now() - start).total_seconds()
        logger.error(f"❌ Documentation generation failed: {e}")
        return DocumentationResponse(
            file_path=request.file_path,
            documentation=f"Error: {e}",
            status="error",
            processing_time=duration
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agents": list(agents.keys()),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    """Prometheus metrics endpoint"""
    agent_count = len(agents)
    metric_data = f"""# HELP ai_agents_total Number of active AI agents
# TYPE ai_agents_total gauge
ai_agents_total {agent_count}

# HELP ai_agents_health_status Health status of the service
# TYPE ai_agents_health_status gauge
ai_agents_health_status 1
"""
    return metric_data

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
