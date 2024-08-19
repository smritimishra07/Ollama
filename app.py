import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json'
}

history = []

def generate_response(prompt):
    history.append(prompt)
    final_prompt = "\n".join(history)
    
    print(f"Sending prompt: {final_prompt}")  # Debug: Check the prompt being sent

    data = {
        "model": "codeguru",  # Replace with the smaller model's name
        "prompt": final_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_text = response.text
            print(f"Raw response: {response_text}")  # Debug: Check the raw response

            data = json.loads(response_text)
            if 'response' in data:
                actual_response = data['response']
                print(f"Processed response: {actual_response}")  # Debug: Check the processed response
                return actual_response
            else:
                print("Error: 'response' key not found in the API response.")
                return "Error: Unexpected API response format."
        else:
            print(f"Error {response.status_code}: {response.text}")
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        print("Exception occurred:", str(e))
        return f"Exception: {str(e)}"

interface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=4, placeholder="Enter your Prompt"),
    outputs="text"
)

interface.launch()
