from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Import CORS Middleware
import whisper
from pathlib import Path
import os
import torch 

# Directory to save uploaded files
UPLOAD_DIR = Path("./uploaded_audios")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# check if the device is a cuda device, else use CPU
device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"Using Device: {device}")

# for a full list of models see https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages
model = whisper.load_model("medium", device=device)

app = FastAPI()

# Add CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict to specific domains here)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.post("/transcribe-audio/")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
       # Generate a unique file name
        file_path = f"{UPLOAD_DIR}/{file.filename}"

        # Save the uploaded audio file to the specified path
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # transcribe the audio using whisper model
        result = model.transcribe(file_path)

        # Extract the transcription text from the result
        transcribed_text = result['text']

        return JSONResponse(content={"lang": result["language"], "transcribed_text": transcribed_text})

    except Exception as e:
        print(e.__cause__)
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
    # finally:
        # Optionally, remove the saved file after transcription
       #  os.remove(file_path)


