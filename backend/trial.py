from abstract_ai import AIWrapper

def main():
    ai = AIWrapper()
    user_input = input("Enter your message: ")
    messages = [{"role": "user", "content": user_input}]
    response = ai.get_response(messages)
    print("AI Response:", response)

if __name__ == "__main__":
    main()