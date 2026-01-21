from root_agent.agent import RootAgent

def load_system_prompt():
    with open("prompts/system_prompt.txt", "r") as f:
        return f.read()

def main():
    agent = RootAgent(load_system_prompt())

    print("OmniTool CLI (type 'exit' to quit)")
    while True:
        user_input = input("> ")
        if user_input.lower() in ("exit", "quit"):
            break

        response = agent.run(user_input)
        print("\n" + response + "\n")

if __name__ == "__main__":
    main()