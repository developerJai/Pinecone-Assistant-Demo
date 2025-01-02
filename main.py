from flask import Flask, request, jsonify
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
import os
import sys

app = Flask(__name__)


# Check environment variables
api_key = os.environ.get('PINECONE_API_KEY')
assistant_name = os.environ.get('ASSISTANT_NAME')

if not api_key:
    print("ERROR: PINECONE_API_KEY environment variable is not set!", file=sys.stderr)
    raise ValueError("PINECONE_API_KEY environment variable is required")

if not assistant_name:
    print("ERROR: ASSISTANT_NAME environment variable is not set!", file=sys.stderr)
    raise ValueError("ASSISTANT_NAME environment variable is required")

try:
    # Initialize Pinecone client
    pc = Pinecone(api_key=api_key)

    # Create Assistant object
    assistant = pc.assistant.Assistant(assistant_name=assistant_name)
except Exception as e:
    print(f"ERROR initializing Pinecone: {str(e)}", file=sys.stderr)
    raise

def chat_with_assistant(question):
    chat_context = [Message(content=question)]
    response = assistant.chat_completions(messages=chat_context)
    return response.choices[0].message.content


# def chat_with_assistant(question):
#     # Create message dictionary directly
#     chat_context = [{"role": "user", "content": question}]
#     response = assistant.chat_completions(messages=chat_context)
#     return response.choices[0].message.content

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    if not data or 'question' not in data:
        return jsonify({"error": "No question provided"}), 400

    question = data['question']
    answer = chat_with_assistant(question)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
