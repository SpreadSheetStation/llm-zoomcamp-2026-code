import json
from dotenv import load_dotenv
from openai import OpenAI
from fp_ingest import load_qa_kb, build_index

load_dotenv()
client = OpenAI()

class AgenticRAG:
    def __init__(self, index):
        self.index = index
        self.search_tool = {
            "type": "function",
            "name": "search",
            "description": "Search the knowledge base for entries matching the given query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query text to look up in the knowledge base."
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
        self.instructions = """
You are a history study tutor. Answer questions about the Dancing Plague of 1518.

If you need information to answer the question, use the search function.
Use as many keywords from the user question as possible when making first requests.

Make multiple searches if needed. Try to expand your search by using new keywords based on the results you get.

At the end, ask if there are other areas the user wants to explore.
""".strip()

    def search(self, query):
        boost_dict = {"question": 3.0, "answer": 0.5}
        return self.index.search(query, num_results=5, boost_dict=boost_dict)

    def ask(self, question):
        messages = [
            {"role": "developer", "content": self.instructions},
            {"role": "user", "content": question}
        ]
        while True:
            response = client.responses.create(
                model="gpt-5.4-mini",
                input=messages,
                tools=[self.search_tool]
            )
            messages.extend(response.output)
            has_function_calls = False
            for item in response.output:
                if item.type == "function_call":
                    args = json.loads(item.arguments)
                    result = self.search(**args)
                    result_json = json.dumps(result, indent=2)
                    messages.append({
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": result_json,
                    })
                    has_function_calls = True
                elif item.type == "message":
                    last_answer = item.content[0].text
            if not has_function_calls:
                return last_answer

if __name__ == "__main__":
    documents = load_qa_kb()
    index = build_index(documents)
    agent = AgenticRAG(index)
    # print(agent.ask("What caused the dancing plague of 1518?"))

### v Make it interactive in Terminal when running python3 agentic_assistant.py v ###    
    print("Welcome! Ask me anything about the Dancing Plague of 1518.")
    print("Type 'quit' or 'exit' to stop.\n")
    
    while True:
        question = input("You: ")
        if question.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break
        answer = agent.ask(question)
        print(f"Agent: {answer}\n")