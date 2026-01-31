# LLM Council - Quick Setup Guide

## Step-by-Step Setup

### 1. Install LM Studio
1. Download LM Studio from https://lmstudio.ai/
2. Install and open LM Studio
3. Download 3-4 models (recommendations below)
4. Load your models in LM Studio
5. Go to "Local Server" tab and click "Start Server"
6. Verify it's running at http://localhost:1234

### 2. Configure the Project

```bash
# Copy the environment file
cp .env.example .env
```

Edit `.env` and update the model names to match your LM Studio models:

```bash
# Example configuration
COUNCIL_MODELS=mistral-7b-instruct-v0.2,llama-2-13b-chat,neural-chat-7b-v3
CHAIRMAN_MODEL=mistral-7b-instruct-v0.2
```

**Important**: Model names must match exactly what's shown in LM Studio!

### 3. Install Dependencies

**Option A: Using Conda (Recommended)**

```bash
# Create and activate the conda environment
conda env create -f environment.yml
conda activate llm-council
```

**Option B: Using pip**

```bash
# Install from requirements.txt
pip install -r requirements.txt
```

**Option C: Using uv** (if you have uv installed)

```bash
uv sync
```

### 4. Run the Application

**Windows:**
```powershell
.\start.ps1
```

**macOS/Linux:**
```bash
./start.sh
```

### 5. Open in Browser

Navigate to: http://localhost:8501

## Recommended Models by System

### 16GB+ RAM (Best Experience)
- Mistral 7B Instruct v0.2
- Llama 2 13B Chat
- Neural Chat 7B v3
- OpenHermes 2.5 Mistral 7B

### 8-16GB RAM (Good Balance)
- Mistral 7B Instruct v0.2
- Llama 2 7B Chat
- Phi-2
- TinyLlama 1.1B Chat

### Less than 8GB RAM (Light Models)
- Phi-2 (2.7B)
- TinyLlama 1.1B
- Qwen 1.8B
- Use heavily quantized versions (Q4 or Q5)

## How to Find Model Names in LM Studio

1. Open LM Studio
2. Go to "Local Server" tab
3. Load your models
4. Look at the model name shown (e.g., "mistral-7b-instruct-v0.2")
5. Copy that exact name to your `.env` file

## Verification Checklist

Before running, make sure:
- [ ] LM Studio is installed and running
- [ ] At least 3 models are loaded in LM Studio
- [ ] Local server is started in LM Studio (port 1234)
- [ ] `.env` file is created with correct model names
- [ ] Conda environment created and activated (`conda activate llm-council`)
- [ ] Dependencies are installed

## Testing LM Studio Connection

Open http://localhost:1234/v1/models in your browser.
You should see a JSON response with your loaded models.

## Troubleshooting

**Can't connect to LM Studio:**
- Make sure LM Studio's local server is started
- Check it's running on port 1234
- Visit http://localhost:1234/v1/models to verify

**Models not found:**
- Model names in `.env` must match LM Studio exactly
- Check spelling and capitalization
- Look at LM Studio's "Local Server" tab for exact names

**Out of memory:**
- Use smaller models or better quantization
- Reduce number of council members to 2-3
- Close other applications

**Slow responses:**
- Normal for larger models (13B+)
- Consider using smaller models
- Check your GPU is being utilized in LM Studio

## Next Steps

Once running:
1. Ask a question in the Streamlit UI
2. Watch the three-stage process
3. Review individual responses in the tabs
4. Check logs for detailed process information
5. Experiment with different model combinations

## Advanced Configuration

### Custom Port
If LM Studio is on a different port, update `.env`:
```bash
LM_STUDIO_BASE_URL=http://localhost:YOUR_PORT/v1
```

### Different Backend Port
To change backend port, edit `backend/main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=YOUR_PORT)
```

### Timeout Adjustment
For slower models, increase timeout in `backend/lmstudio.py`:
```python
async def query_model(model, messages, timeout=300.0):  # 5 minutes
```

## Getting Help

Check these resources:
1. `logs/council.log` - Detailed application logs
2. Streamlit sidebar - Real-time process logs
3. Backend console - API request logs
4. LM Studio documentation - https://lmstudio.ai/docs

Enjoy your LLM Council! 🏛️
