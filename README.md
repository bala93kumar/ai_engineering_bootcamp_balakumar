# AI Engineering Bootcamp

This repository contains code assignments and scripts for the AI Engineering Bootcamp. Currently, it includes a Python script to interact with NVIDIA NIM's API using the OpenAI SDK, supporting streaming responses, reasoning/thinking extraction, and saving outputs.

## Project Structure

```text
├── 1_call_ai.py         # Main script to query NVIDIA NIM models
├── 2_no_memory_call.py  # Interactive stateless script (Ollama vs NVIDIA NIM)
├── env/
│   └── .env             # Environment variables containing credentials (git-ignored)
├── ai-engine/           # Python virtual environment (git-ignored)
└── output/              # Directory where API responses are saved as text files (git-ignored)
```

## Setup Instructions

### 1. Configure the Virtual Environment
Activate your existing virtual environment (`ai-engine`):

* **On Windows (PowerShell):**
  ```powershell
  .\ai-engine\Scripts\Activate.ps1
  ```
* **On Windows (CMD):**
  ```cmd
  .\ai-engine\Scripts\activate.bat
  ```
* **On macOS/Linux:**
  ```bash
  source ai-engine/bin/activate
  ```

### 2. Install Dependencies
Install the required Python packages:
```bash
pip install openai python-dotenv
```

### 3. Environment Configuration
Create a `.env` file inside the `env/` directory and add your NVIDIA API Key:
1. Create the file `env/.env` (if it does not exist).
2. Add the following line:
   ```env
   NVIDIA_API_KEY=your_nvidia_api_key_here
   ```

## Usage

### 1. Simple Single-Shot Run (NVIDIA NIM)
Run the script to execute a set of predefined prompts against NVIDIA NIM:
```bash
python 1_call_ai.py
```

### 2. Interactive No-Memory Session (Ollama or NVIDIA NIM)
Run the interactive script to test queries with **fresh context** (no conversation memory) on either a local Ollama server or the remote NVIDIA NIM API:
```bash
python 2_no_memory_call.py
```

- When prompted, choose either **Local Ollama** (backend option `1`) or **NVIDIA NIM** (backend option `2`).
- Select or input the model name to run.
- Ask questions continuously in the terminal. The client is re-initialized / reset for each question to ensure that no conversational memory is passed to the LLM.
- Responses will stream directly to the console and save automatically to individual text files in the `output/` directory.

