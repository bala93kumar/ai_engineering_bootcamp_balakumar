import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the env/.env file
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "env", ".env")
load_dotenv(env_path)

def select_backend():
    print("=" * 60)
    print("               LLM BACKEND SELECTION")
    print("=" * 60)
    print("1. Local Ollama (runs locally on http://localhost:11434)")
    print("2. NVIDIA NIM API (requires NVIDIA_API_KEY in env/.env)")
    print("-" * 60)
    
    while True:
        choice = input("Select backend (1 or 2): ").strip()
        if choice == "1":
            # Set up Ollama connection
            base_url = "http://localhost:11434/v1"
            api_key = "ollama"  # Ollama doesn't require a key, but client expects a string
            default_model = "llama3"
            provider_name = "Local Ollama"
            break
        elif choice == "2":
            # Set up NVIDIA NIM connection
            base_url = "https://integrate.api.nvidia.com/v1"
            api_key = os.getenv("NVIDIA_API_KEY")
            if not api_key:
                print("\n[ERROR] NVIDIA_API_KEY not found in env/.env file.")
                print("Please configure your API key first or select Local Ollama.\n")
                continue
            default_model = "nvidia/nemotron-3-super-120b-a12b"
            provider_name = "NVIDIA NIM"
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
            
    print(f"\nConnected to {provider_name} successfully.")
    
    # Let the user use the default model or specify a custom one
    use_default = input(f"Use default model '{default_model}'? [Y/n]: ").strip().lower()
    if use_default == "n":
        model = input("Enter custom model name: ").strip()
    else:
        model = default_model
    
    # Initialize the OpenAI-compatible client
    client = OpenAI(base_url=base_url, api_key=api_key)
    return client, model, provider_name

def main():
    try:
        client, model, provider_name = select_backend()
    except Exception as e:
        print(f"\n[ERROR] Failed to initialize LLM client: {e}")
        return

    # Prepare output folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    print("\n" + "=" * 60)
    print(f"  NO-MEMORY INTERACTIVE SESSION ({provider_name} - {model})")
    print("  Note: Context is completely fresh for each query.")
    print("  Type 'exit' or 'quit' to end the session.")
    print("=" * 60 + "\n")

    while True:
        try:
            question = input("\nAsk a question: ").strip()
            if not question:
                continue
            if question.lower() in ["exit", "quit"]:
                print("\nExiting session. Goodbye!")
                break

            print(f"\nSending request to {model}...")
            
            # Since this is a NO-MEMORY call, we only pass the current question
            # No previous chat history is saved or passed to the client
            messages = [
                {"role": "user", "content": question}
            ]

            # NVIDIA NIM Nemotron model supports extra parameters like reasoning
            extra_params = {}
            if "nvidia" in model.lower():
                extra_params = {
                    "extra_body": {
                        "chat_template_kwargs": {"enable_thinking": True}, 
                        "reasoning_budget": 1024
                    }
                }

            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=1,
                top_p=0.95,
                max_tokens=1024,
                stream=True,
                **extra_params
            )

            # Sanitize filename (remove characters invalid in filenames)
            sanitized_question = "".join(c for c in question if c not in '\\/:*?"<>|').strip()
            # Truncate filename if it's too long
            filename = (sanitized_question[:100].replace(' ', '_') or "response") + ".txt"
            file_path = os.path.join(output_dir, filename)

            print("Response: ", end="", flush=True)

            with open(file_path, "w", encoding="utf-8") as f:
                for chunk in completion:
                    if not chunk.choices:
                        continue
                    
                    # Check for reasoning/thinking content (NVIDIA-specific)
                    reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
                    if reasoning:
                        print(reasoning, end="", flush=True)
                        f.write(reasoning)
                    
                    # Print and write standard completion content
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        print(content, end="", flush=True)
                        f.write(content)
            
            print(f"\n\n[SUCCESS] Response saved to: {file_path}")
            print("-" * 60)

        except KeyboardInterrupt:
            print("\nSession interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n[ERROR] An error occurred: {e}")
            print("Please ensure your local Ollama server is running or check your API key/network connection.")
            print("-" * 60)

if __name__ == "__main__":
    main()
