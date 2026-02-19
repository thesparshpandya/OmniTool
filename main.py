import asyncio
from google.adk.runners import InMemoryRunner
from google.adk.runners import Session
from google.genai.types import Content, Part
from root_agent.agent import agent

def main():
    # --- 1. CONFIGURATION ---
    APP_NAME = "omnitool_cli"
    USER_ID = "local_user"
    SESSION_ID = "omnitool_session_01"

    # --- 2. DEFINE IDENTITY ---
    session = Session(
        id=SESSION_ID, 
        appName=APP_NAME,
        userId=USER_ID
    )

    # --- 3. INITIALIZE ENGINE ---
    runner = InMemoryRunner(
        agent=agent,
        app_name=APP_NAME
    )

    # --- 4. REGISTER SESSION ---
    print("Initializing session...")
    asyncio.run(
        runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )
    )
    print("Session Registered.")
    print("OmniTool (Google-native) — type 'exit' to quit")

    # --- 5. CHAT LOOP ---
    while True:
        # Main try-block to catch total crashes cleanly
        try:
            user_input = input("\nUser> ")
            if user_input.lower() in ("exit", "quit"):
                print("OmniTool: Shutting down.")
                break

            user_message = Content(
                role="user",
                parts=[Part(text=user_input)]
            )

            # Nested try-block specifically for Google API calls
            try:
                events = runner.run(
                    session_id=SESSION_ID, 
                    user_id=USER_ID, 
                    new_message=user_message
                )

                print("OmniTool: ", end="")
                for event in events:
                    if hasattr(event, "text") and event.text:
                        print(event.text, end="", flush=True)
                    elif hasattr(event, "content") and event.content:
                        if hasattr(event.content, "parts") and event.content.parts:
                            print(event.content.parts[0].text, end="", flush=True)
                        else:
                            print(str(event.content), end="", flush=True)
                
                print() # Print a clean newline after the response finishes

            # Catch and format the API errors so they don't look scary
            except Exception as api_err:
                err_str = str(api_err)
                if "503" in err_str or "UNAVAILABLE" in err_str:
                    print("OmniTool: The Google API is currently overloaded. Please wait a moment and try again.")
                elif "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    print("OmniTool: Quota exceeded. We need to wait a minute.")
                else:
                    print(f"OmniTool: API Error: {err_str}")

        except Exception as fatal_err:
            print(f"\nFatal Error: {fatal_err}")
            break

if __name__ == "__main__":
    main()