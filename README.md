# LLM Council

![llmcouncil](header.jpg)

The idea of this repo is that instead of asking a question to your favorite LLM provider, you can group them into your "LLM Council". This repo is a web app that uses **LM Studio** to send your query to multiple local LLMs, asks them to review and rank each other's work, and finally a Chairman LLM produces the final response.

## 🌟 What's New

This version has been updated to:
- ✅ **Use LM Studio** instead of cloud providers (run everything locally!)
- ✅ **Streamlit Web Interface** with beautiful UI showing the full council process
- ✅ **Comprehensive Logging** - see every step of the council deliberation
- ✅ **Multi-tab Display** - view responses, rankings, and final synthesis separately

## How It Works

When you submit a query, here's what happens:

1. **Stage 1: First opinions**. The user query is given to all LLMs individually, and the responses are collected.
2. **Stage 2: Review**. Each individual LLM is given the responses of the other LLMs. The LLM identities are anonymized so that the LLM can't play favorites. Each LLM ranks all responses.
3. **Stage 3: Final response**. The designated Chairman of the LLM Council takes all of the model's responses and rankings to compile a single final answer.

All stages are displayed in a beautiful Streamlit interface with full logging!

## Prerequisites

### 1. Install LM Studio

Download and install [LM Studio](https://lmstudio.ai/) for your operating system.

### 2. Load Models in LM Studio

1. Open LM Studio
2. Download at least 3 models (recommended: 3-4 models for good debate)
3. Load the models you want to use
4. Start the local server:
   - In LM Studio, go to the "Local Server" tab
   - Click "Start Server"
   - Note the port (default: 1234) and models loaded

**Recommended Models** (choose based on your system):
- For 16GB+ RAM: Mistral 7B, Llama 2 13B, Neural Chat 7B, OpenHermes 2.5
- For 8-16GB RAM: Mistral 7B, Llama 2 7B, Phi-2
- For 8GB or less: Phi-2, TinyLlama, smaller quantized models

## Setup

### 1. Install Dependencies

The project supports both **conda** and **uv** for package management.

**Option A: Using Conda (Recommended for Conda users)**

Create and activate the conda environment:
```bash
# Create environment from environment.yml
conda env create -f environment.yml

# Activate the environment
conda activate llm-council
```

**Option B: Using pip with requirements.txt**
```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Option C: Using uv**

```bash
uv sync
```

### 2. Configure LM Studio Connection

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` with your LM Studio configuration:

```bash
# LM Studio base URL (default: http://localhost:1234/v1)
LM_STUDIO_BASE_URL=http://localhost:1234/v1

# Council Models (comma-separated, match names in LM Studio)
COUNCIL_MODELS=mistral-7b-instruct,llama-2-13b-chat,neural-chat-7b

# Chairman Model (synthesizes final answer)
CHAIRMAN_MODEL=mistral-7b-instruct
```

**Important**: The model names in `COUNCIL_MODELS` must match the exact names shown in LM Studio when you load models!

## Running the Application

### Windows (PowerShell)

```powershell
.\start.ps1
```

### macOS/Linux (Bash)

```bash
./start.sh
```

### Manual Start (if you prefer)

**Terminal 1 - Backend:**
```bash
# Make sure your conda environment is activated first
conda activate llm-council

# Start backend
python -m backend.main
```

**Terminal 2 - Streamlit UI:**
```bash
# Make sure your conda environment is activated first
conda activate llm-council

# Start Streamlit
streamlit run streamlit_app.py
```

### Access the Application

Once started, open your browser to:
- **Streamlit UI**: http://localhost:8501 (main interface)
- **Backend API**: http://localhost:8001 (API docs at /docs)

## Using the Application

1. **Make sure LM Studio is running** with your models loaded and server started
2. Open http://localhost:8501 in your browser
3. Enter your question in the text area
4. Click "Submit to Council"
5. Watch the progress as the council deliberates:
   - Stage 1: Each model provides their initial response
   - Stage 2: Models rank each other's responses anonymously
   - Stage 3: Chairman synthesizes the final answer
6. View results in multiple tabs:
   - **Final Answer**: The chairman's synthesis
   - **Stage 1: Responses**: All individual model responses
   - **Stage 2: Rankings**: How models ranked each other
   - **Full Process**: Complete view of all stages

## Logging

The application provides comprehensive logging:

- **In Streamlit**: Real-time process logs in the sidebar
- **Console**: Detailed logs in the terminal running the backend
- **Log Files**: Full logs saved to `logs/council.log`

Log files include:
- Each model's response time and success/failure
- All three stages with detailed information
- Errors and warnings for troubleshooting

## Configuration Tips

### Model Selection

Choose diverse models for better results:
- Mix different architectures (Mistral, Llama, Phi, etc.)
- Include both instruction-tuned and chat models
- Ensure models have similar capabilities

### Performance Tuning

If models are responding slowly:
- Use smaller models or better quantization
- Reduce the number of council members
- Increase timeout in `backend/lmstudio.py`

### Debugging

If you encounter issues:
1. Check `logs/council.log` for detailed error messages
2. Verify LM Studio is running: http://localhost:1234/v1/models
3. Ensure model names in `.env` match LM Studio exactly
4. Check the Streamlit logs panel for real-time status

## Tech Stack

- **Backend**: FastAPI (Python 3.10+), async httpx
- **Frontend**: Streamlit with custom CSS
- **LLM Integration**: LM Studio (OpenAI-compatible API)
- **Storage**: JSON files in `data/conversations/`
- **Logging**: Python logging module with file and console handlers
- **Package Management**: Conda / pip (requirements.txt provided)

## Project Structure

```
llm-council/
├── backend/
│   ├── __init__.py
│   ├── config.py          # LM Studio configuration
│   ├── council.py         # 3-stage orchestration with logging
│   ├── lmstudio.py        # LM Studio API client
│   ├── main.py            # FastAPI backend
│   └── storage.py         # Conversation storage
├── logs/
│   └── council.log        # Application logs
├── data/
│   └── conversations/     # Stored conversations
├── streamlit_app.py       # Streamlit web interface
├── start.ps1              # Windows start script
├── start.sh               # Unix start script
├── .env.example           # Example configuration
└── pyproject.toml         # Python dependencies
```

## Troubleshooting

### "Backend connection failed"
- Ensure backend is running on port 8001
- Check firewall settings

### "All models failed to respond"
- Verify LM Studio server is running
- Check model names in `.env` match LM Studio
- Review logs in `logs/council.log`

### Slow responses
- Use smaller/faster models
- Reduce number of council members
- Check your system resources

### Model not found
- Ensure the model is loaded in LM Studio
- Verify exact model name spelling in `.env`
- Check LM Studio's loaded models list

## Credits

Original concept inspired by the idea of leveraging multiple LLMs for better responses. This is an educational project demonstrating local LLM orchestration with LM Studio.

## License

MIT License - Feel free to modify and use as you wish!
