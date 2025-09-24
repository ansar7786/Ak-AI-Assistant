from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

# Suppress gRPC logs
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_TRACE"] = ""

# Configure Gemini API key
API_KEY = "AIzaSyDvOGFz_xm_C1JzqabwPgr33lWxDH-TnYE"  # replace with your actual key
genai.configure(api_key=API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

# Create FastAPI app
app = FastAPI(title="AK Gemini Chat API")

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to your frontend in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(body: ChatRequest):
    try:
        response = chat.send_message(body.message)
        reply_text = response.text if hasattr(response, "text") and response.text else response.candidates[0].content.parts[0].text
        return {"reply": reply_text}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
