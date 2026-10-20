import sys
from agent import create_agent


def main():
    agent = create_agent()
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        response = agent.invoke({"messages": [{"role": "user", "content": query}]})
        messages = response.get("messages", [])
        if messages:
            content = messages[-1].content
            if isinstance(content, list) and content:
                print(content[0].get("text", content[0]))
            else:
                print(content)
        return

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                break
            response = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
            messages = response.get("messages", [])
            if messages:
                content = messages[-1].content
                if isinstance(content, list) and content:
                    print(f"Agent: {content[0].get('text', content[0])}\n")
                else:
                    print(f"Agent: {content}\n")
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    main()

