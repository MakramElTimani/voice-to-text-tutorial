## Setup

(I'm, using windows 😉)

```

cd api

python -m venv venv

.\venv\Scripts\activate

```

## Required Packages

```
pip install fastapi uvicorn python-multipart

pip install torch==1.11.0+cu113 torchaudio===0.11.0+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html

pip install transformers accelerate "numpy<2"

pip install git+https://github.com/openai/whisper.git

```

## Run the API

```

cd api

uvicorn main:app --reload

```
