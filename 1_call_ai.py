import os
import sys  
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the env/.env file
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "env", ".env")
load_dotenv(env_path)

def main(input_question):
    # Initialize OpenAI client (requires API key)
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.getenv("NVIDIA_API_KEY")
    )

    question = input_question
    
    # Prepare output folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Sanitize filename (remove characters invalid in filenames)
    sanitized_question = "".join(c for c in question if c not in '\\/:*?"<>|').strip()
    filename = sanitized_question.replace(' ', '_') + ".txt"
    file_path = os.path.join(output_dir, filename)

    print(f"Fetching response for: '{question}'...")
    
    completion = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b",

        #role model based prompting. 
        # messages=[{"role": "user", "content": question}],
        messages = [
            {"role": "system", "content": "you are a eastern poet"}, 
            {"role": "user", "content": question}
        ],
        temperature=1,
        top_p=0.95,
        max_tokens=1024,
        extra_body={"chat_template_kwargs": {"enable_thinking": True}, "reasoning_budget": 1024},
        stream=True
    )

    print(f"Writing output to: {file_path}")
    
    with open(file_path, "w", encoding="utf-8") as f:
        for chunk in completion:
            if not chunk.choices:
                continue
            reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
            if reasoning:
                f.write(reasoning)
            if chunk.choices[0].delta.content is not None:
                f.write(chunk.choices[0].delta.content)
    
    print("Output saved successfully.")

if __name__ == "__main__":
    
    #role based basic prompting - example:
    input_question = "why is dollar value increasing give response in general terms?"
    main(input_question)

    #role based advanced 
    main("write a short poem about moon in english")
