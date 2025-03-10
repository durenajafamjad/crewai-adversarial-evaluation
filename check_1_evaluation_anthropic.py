import os
import json
from datetime import datetime

import openai
from openai import OpenAI
import os
import json
from datetime import datetime
import anthropic


os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

ANT_MODEL = "claude-3-5-sonnet-20241022"
ORIGINAL_MODEL = "gpt-4o"
AGENT_NAME = "technical_support"


def evaluate_infections(memory_dir, response_model, output_file="infection_log.json"):
    """
    Evaluate harmful queries in JSON files and write infection logs to a file.
    
    Args:
        memory_dir (str): Directory containing JSON files with query-response pairs.
        response_model (str): The name of the response model used for testing.
        output_file (str): File to write the infection log.
    """
    infection_log = []

    # Traverse files in the memory directory
    for root, _, files in os.walk(memory_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)

                # Load the JSON data
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                print(f"Processing file: {file_path}")
                total_queries = len(data)
                harmful_queries = []

                # Evaluate harmful queries
                for entry in data:
                    harmful = entry.get("evaluation", {}).get("Harmful", "No").lower()
                    if harmful == "yes":
                        harmful_queries.append(entry["query"])

                harmful_count = len(harmful_queries)
                infected_rate = f"{(harmful_count / total_queries) * 100:.2f}%" if total_queries > 0 else "0.00%"

                # Print debugging information
                print(f"Total queries: {total_queries}, Harmful count: {harmful_count}, Infected rate: {infected_rate}")
                print(f"Harmful queries: {harmful_queries}")

                # Prepare infection log entry
                infection_log.append({
                    "file_name": file_path,
                    "total_queries": total_queries,
                    "harmful_count": harmful_count,
                    "infected_rate": infected_rate,
                    "infected_queries": harmful_queries,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "testing_model": response_model,
                    "response_model": response_model,
                })
    
    # Write the infection log to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(infection_log, f, indent=4)
    print(f"Infection log written to {output_file}")

# Example usage
evaluate_infections(
    memory_dir="check_1", 
    response_model="gpt-4o-mini", 
)
