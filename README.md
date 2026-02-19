# OmniTool: Autonomous AI Agent

A lightweight, highly capable AI agent built using the Google Agent Development Kit (ADK). OmniTool acts as an intelligent orchestrator that can reason through user queries, maintain conversation state, and autonomously execute tools to fetch real-world data.

Currently powered by Google's Gemini 2.5 Flash model, this project serves as a modular skeletal framework for building complex, multi-tool AI assistants.

## Architecture & Workflow



Unlike a standard linear chatbot, OmniTool operates on an Agentic execution loop.

| Feature | Description |
| :--- | :--- |
| **Reasoning Engine** | Uses `LlmAgent` to analyze the user's intent before generating text. |
| **Execution Environment** | The `InMemoryRunner` handles asynchronous orchestration between the user, the LLM, and the tools. |
| **State Management** | Uses strict ADK `Session` objects to maintain conversation history and user identity across turns. |
| **Dynamic Context** | Injects real-time system variables (like current date and time) directly into the agent's system prompt at runtime. |
| **Autonomous Tools** | Equipped with Google Search Grounding (native `Google Search` object) for real-time web access, with modular support for custom Python tools. |

## Key Features

* **Native Google Integration:** Built entirely on the official `google-adk` and `google-genai` libraries for maximum compatibility and speed.
* **"Hands & Brain" Separation:** * **Brain:** System prompts define strict guardrails (no hallucinating, no conversational filler).
  * **Hands:** Modular tool list allows for infinite expansion. Just write a Python function and plug it in.
* **Secure API Key Management:** Uses the `getpass` module for secure, invisible terminal input of API keys if they are not found in the local environment variables.
* **Clean Error Handling:** Gracefully intercepts Google API rate limits (429) and server overloads (503) to prevent terminal crashes, notifying the user intelligently.
* **Zero-Shot Tool Use:** The agent dynamically decides if it needs to hit the internet via Google Search Grounding or if it can answer from its internal training data.

## Tech Stack

* **Language:** Python 3.10+
* **Orchestration:** Google Agent Development Kit (ADK)
* **SDK:** Google Gen AI SDK
* **LLM Engine:** `gemini-2.5-flash`
* **Search Integration:** Google Search Grounding via ADK (`Google Search`)

## Prerequisites

Before running the project, ensure you have:
* Python 3.10+ installed.
* A Google Gemini API Key.

## Installation

1. **Clone the repository:**
            ```bash
            git clone https://github.com/thesparshpandya/OmniTool.git
            cd omnitool

            ```

2. **Create a Virtual Environment (Recommended):**
            ```bash
            python -m venv venv
            source venv/bin/activate  # On Windows use: venv\Scripts\activate

            ```


3. **Install Dependencies:**
            ```bash
            pip install -r requirements.txt

            ```


*(Ensure `google-adk` and `google-genai` are in your requirements file)*

## Usage

Start the agent by running the main execution script:

```bash
python main.py

```

If your API key is not set in your environment variables, the terminal will securely prompt you to paste it (the input will be hidden for security).

Once initialized, you will see a `User>` prompt. Try asking:

* "What is the exact time right now?" (Tests dynamic context)
* "What is the latest news regarding the Google Gemini API today?" (Tests the Google Search Grounding tool)

Type `exit` or `quit` to gracefully shut down the agent.

## Project Structure

* `main.py`: The entry point. Handles the `InMemoryRunner`, session registration, secure API key prompting, user input loop, and API error catching.
* `root_agent/agent.py`: The brain of the operation. Contains the `LlmAgent` definition, the dynamic system prompt, and the native `Google Search` tool injection.
* `check_models.py` (Optional): A diagnostic script to verify which Gemini models are available to your specific API key.

## Troubleshooting

* **"The Google API is currently overloaded" (503 Error):** You are using a free-tier API key during a high-traffic period. OmniTool catches this so it won't crash. Just wait 30-60 seconds and ask your question again.
* **"Quota exceeded" (429 Error):** You have hit your requests-per-minute limit. Wait one minute.
* **"Model not found" (404 Error):** The model string in `agent.py` is incorrect or unavailable in your region. Ensure it is set to a standard model like `gemini-2.5-flash`.
* **Validation Error / ImportError on Tools:** The ADK is very strict. Ensure you are importing and passing the pre-built `Google Search` object (`from google.adk.tools import google_search`), rather than raw SDK schemas or legacy class instances.