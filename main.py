import asyncio
import os
import getpass
from google.adk.runners import InMemoryRunner
from google.adk.runners import Session
from google.genai.types import Content, Part
from root_agent.agent import agent

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

def main():
    console = Console()
    
    # --- 0. API KEY CHECK ---
    if not os.environ.get("GOOGLE_API_KEY"):
        console.print("\n[bold yellow]WARNING: GOOGLE_API_KEY not found in environment variables.[/bold yellow]")
        key = getpass.getpass("Please paste your Google API Key here (input will be hidden): ")
        if key.strip():
            os.environ["GOOGLE_API_KEY"] = key.strip()
            console.print("[bold green]SUCCESS: API Key set for this session.[/bold green]\n")
        else:
            console.print("[bold red]ERROR: No key provided. Exiting...[/bold red]")
            return

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
    console.print(f"[dim]Initializing {APP_NAME}...[/dim]")
    try:
        asyncio.run(
            runner.session_service.create_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=SESSION_ID
            )
        )
    except Exception as e:
        console.print(f"[bold red]Session Error:[/bold red] {e}")
        
    console.print("[bold cyan]SYSTEM: OmniTool is online. Type 'exit' to quit.[/bold cyan]")

    # --- 5. CHAT LOOP ---
    while True:
        try:
            user_input = console.input("\n[bold magenta]User>[/bold magenta] ")
            
            if user_input.lower().strip() in ("exit", "quit", "q", "bye", "goodbye", "stop"):
                console.print("[bold cyan]OmniTool: Shutting down.[/bold cyan]")
                break

            user_message = Content(
                role="user",
                parts=[Part(text=user_input)]
            )

            try:
                events = runner.run(
                    session_id=SESSION_ID, 
                    user_id=USER_ID, 
                    new_message=user_message
                )

                full_response = ""
                console.print("[bold green]OmniTool:[/bold green]")
                
                with Live(Markdown(""), console=console, refresh_per_second=15, vertical_overflow="visible") as live:
                    for event in events:
                        chunk = ""
                        if hasattr(event, "text") and event.text:
                            chunk = event.text
                        elif hasattr(event, "content") and event.content:
                            if hasattr(event.content, "parts") and event.content.parts:
                                chunk = event.content.parts[0].text
                            else:
                                chunk = str(event.content)
                        
                        if chunk:
                            full_response += chunk
                            live.update(Markdown(full_response))
                
            except Exception as api_err:
                console.print(f"\n[bold red]OmniTool Error:[/bold red] {str(api_err)}")

        except KeyboardInterrupt:
            console.print("\n[bold cyan]OmniTool: Interrupted. Shutting down.[/bold cyan]")
            break
        except EOFError:
            console.print("\n[bold cyan]OmniTool: Shutting down.[/bold cyan]")
            break
        except Exception as fatal_err:
            console.print(f"\n[bold red]Fatal System Error:[/bold red] {fatal_err}")
            break

if __name__ == "__main__":
    main()