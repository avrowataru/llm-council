# Conda Installation Guide

This guide walks you through setting up the LLM Council project using conda.

## Prerequisites

- [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed
- [LM Studio](https://lmstudio.ai/) installed and running

## Quick Start with Conda

### 1. Create the Conda Environment

Navigate to the project directory and create the environment:

```bash
cd c:\Users\Rambo\Documents\source\llm-council
conda env create -f environment.yml
```

This creates a new conda environment named `llm-council` with Python 3.10+ and all required dependencies.

### 2. Activate the Environment

```bash
conda activate llm-council
```

You should see `(llm-council)` appear in your terminal prompt.

### 3. Verify Installation

Check that all packages are installed:

```bash
python -c "import fastapi, streamlit, httpx; print('All dependencies installed successfully!')"
```

### 4. Configure LM Studio

Create your `.env` file:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Or manually copy
# Copy .env.example to .env and edit it
```

Edit `.env` and update the model names to match your LM Studio models:

```bash
COUNCIL_MODELS=mistral-7b-instruct-v0.2,llama-2-13b-chat,neural-chat-7b-v3
CHAIRMAN_MODEL=mistral-7b-instruct-v0.2
```

### 5. Start LM Studio

1. Open LM Studio
2. Load your models (at least 3 for a good council)
3. Go to "Local Server" tab
4. Click "Start Server"
5. Verify at http://localhost:1234/v1/models

### 6. Run the Application

**Windows:**
```powershell
.\start.ps1
```

**macOS/Linux:**
```bash
./start.sh
```

**Or run manually:**

Terminal 1 - Backend:
```bash
conda activate llm-council
python -m backend.main
```

Terminal 2 - Streamlit:
```bash
conda activate llm-council
streamlit run streamlit_app.py
```

### 7. Access the Application

Open your browser to:
- **Streamlit UI**: http://localhost:8501
- **Backend API**: http://localhost:8001

## Managing the Conda Environment

### Update Dependencies

If new packages are added to `requirements.txt`:

```bash
conda activate llm-council
pip install -r requirements.txt
```

### List Installed Packages

```bash
conda activate llm-council
conda list
```

### Export Current Environment

If you want to save your current environment state:

```bash
conda activate llm-council
conda env export > environment_backup.yml
```

### Remove the Environment

If you need to start fresh:

```bash
conda deactivate
conda env remove -n llm-council
```

Then recreate it:

```bash
conda env create -f environment.yml
```

## Troubleshooting

### "conda: command not found"

Make sure Anaconda or Miniconda is installed and in your PATH.

**Windows:** Restart your terminal or use "Anaconda Prompt"
**macOS/Linux:** Run `source ~/.bashrc` or `source ~/.zshrc`

### "Environment already exists"

If the environment already exists, either remove it first:
```bash
conda env remove -n llm-council
```

Or update it:
```bash
conda env update -f environment.yml
```

### Package conflicts

If you encounter package conflicts, try creating a fresh environment:
```bash
conda env remove -n llm-council
conda env create -f environment.yml
```

### Wrong Python version

Make sure you're using Python 3.10+:
```bash
conda activate llm-council
python --version
```

## Using Multiple Environments

If you have other conda environments, make sure to activate the correct one:

```bash
# List all environments
conda env list

# Activate llm-council
conda activate llm-council

# Deactivate when done
conda deactivate
```

## Windows-Specific Notes

On Windows, you may need to:

1. Use "Anaconda Prompt" or "Anaconda PowerShell Prompt"
2. Run PowerShell as Administrator for the first setup
3. Make sure conda is in your system PATH

## Next Steps

Once everything is running:

1. Open http://localhost:8501
2. Check that the backend is connected (green checkmark in sidebar)
3. Submit your first query to the council
4. View the full deliberation process in the tabs
5. Check the logs for detailed information

Enjoy your LLM Council! 🏛️
