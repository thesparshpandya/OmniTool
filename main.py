import asyncio
from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part
from root_agent.agent import agent

def main():
    # 1. Configuration
    APP_NAME = "omnitool_cli"
    USER_ID = "local_user"
    SESSION_ID = "omnitool_session_01"

    # 2. Initialize the Engine
    # app_name is set here so the runner knows which namespace to use.
    runner = InMemoryRunner(
        agent=agent,
        app_name=APP_NAME
    )

    # 3. REGISTER THE SESSION (The Missing Step)
    # explicitly save the session to the runner's internal "database"
    # before we can use it. We use asyncio.run because create_session is async.
    print("⏳ Initializing session...")
    asyncio.run(
        runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )
    )
    print(" Session Registered.")

    print(" OmniTool (Google-native) — type 'exit' to quit")

    while True:
        try:
            user_input = input("User> ")
            if user_input.lower() in ("exit", "quit"):
                print("OmniTool: Shutting down.")
                break

            user_message = Content(
                role="user",
                parts=[Part(text=user_input)]
            )

            # 4. Run the Agent
            # Now that the session is registered, the runner will find it.
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
                    # Handle complex content objects safely
                    if hasattr(event.content, "parts") and event.content.parts:
                        print(event.content.parts[0].text, end="", flush=True)
                    else:
                        print(str(event.content), end="", flush=True)
            
            print("\n")

        except Exception as e:
            print(f"\n Error details: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()