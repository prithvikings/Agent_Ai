from dotenv import load_dotenv
import os
import pandas as pd
import google.generativeai as genai
from llama_index.core.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context
from note_engine import note_engine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from pdf import india_engine

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Load population data
population_path = os.path.join("data", "population.csv")
population_df = pd.read_csv(population_path)

population_query_engine = PandasQueryEngine(
    df=population_df, verbose=True, instruction_str=instruction_str
)
population_query_engine.update_prompts({"pandas_prompt": new_prompt})

# Define tools
tools = [
    note_engine,
    QueryEngineTool(
        query_engine=population_query_engine,
        metadata=ToolMetadata(
            name="population_data",
            description="This gives information about world population and demographics.",
        ),
    ),
    QueryEngineTool(
        query_engine=india_engine,
        metadata=ToolMetadata(
            name="india_data",
            description="This gives detailed information about india.",
        ),
    ),
]

# Define Gemini-based Agent
class GeminiAgent:
    def __init__(self, tools, context):
        self.tools = tools
        self.context = context

    def query(self, prompt):
        response = genai.generate_text(model="Gemini 2.0", prompt=prompt)
        return response.text

# Initialize Agent
agent = GeminiAgent(tools=tools, context=context)

# Main Loop
while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    result = agent.query(prompt)
    print(result)
