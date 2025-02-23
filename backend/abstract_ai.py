import requests
from dotenv import load_dotenv
import os

load_dotenv()

class AIWrapper:
    def __init__(self, api_url, model_id, project_id, access_token):
        self.api_url = api_url
        self.model_id = model_id
        self.project_id = project_id
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

    def get_response(self, user_input, decoding_method="greedy", max_new_tokens=900, min_new_tokens=0, repetition_penalty=1):
        input_text = f"""<|start_of_role|>system<|end_of_role|>You are an AI recruiter conducting job interviews.
                        Your role is to ask relevant questions based on the candidate's resume, assess their qualifications, and determine if they are a good fit for the role.
                        Be professional, concise, and stay focused on evaluating skills and experiences related to the position.<|end_of_text|>
<|start_of_role|>assistant<|end_of_role|>{user_input}"""
        
        body = {
            "input": input_text,
            "parameters": {
                "decoding_method": decoding_method,
                "max_new_tokens": max_new_tokens,
                "min_new_tokens": min_new_tokens,
                "repetition_penalty": repetition_penalty
            },
            "model_id": self.model_id,
            "project_id": self.project_id
        }

        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=body
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        return response.json()

# Example usage
if __name__ == "__main__":
    api_url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    model_id = "ibm/granite-3-8b-instruct"
    project_id = "3d9b8852-34e2-4b58-a164-622856e19e5a"
    access_token = "YOUR_ACCESS_TOKEN"

    ai = AIWrapper(api_url, model_id, project_id, access_token)
    user_input = "Your input text here"
    response = ai.get_response(user_input)
    print("AI Response:", response)