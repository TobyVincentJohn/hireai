from transformers import pipeline

class AIWrapper:
    def __init__(self, model_name="ibm-granite/granite-3.1-8b-instruct"):
        self.pipe = pipeline("text-generation", model=model_name)

    def get_response(self, messages):
        return self.pipe(messages)