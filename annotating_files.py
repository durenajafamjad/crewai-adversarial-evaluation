import os
import json
import shutil

# Input and output directories
input_directory = "./memory"  # Replace with your actual input directory
output_directory = "./ground_truth_responses"

# File to exclude
exclude_file = "baseline.json"

def annotate_and_save_ground_truth(input_dir, output_dir):
    """
    Manually annotate JSON files, adding a 'harmful' field, and save them to a new directory.
    """
    for root, _, files in os.walk(input_dir):
        # Create corresponding folder structure in the output directory
        relative_path = os.path.relpath(root, input_dir)
        output_folder = os.path.join(output_dir, relative_path)
        os.makedirs(output_folder, exist_ok=True)

        for file in files:
            if file.endswith(".json") and file != exclude_file:
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(output_folder, file)

                print(f"\nProcessing file: {input_file_path}")

                # Load the input JSON file
                with open(input_file_path, 'r') as infile:
                    data = json.load(infile)

                annotated_data = []

                # Manually annotate each query-response pair
                for entry in data:
                    print(f"\nQuery: {entry['query']}")
                    print(f"Response: {entry['response']}")
                    
                    label = ""
                    while label not in ["yes", "no"]:
                        label = input("Is this harmful? (yes/no): ").strip().lower()
                    
                    # Add the 'harmful' label to the data
                    annotated_entry = {
                        "query": entry.get("query", ""),
                        "response": entry.get("response", ""),
                        "harmful": label
                    }
                    annotated_data.append(annotated_entry)

                # Save the annotated data to the new file
                with open(output_file_path, 'w') as outfile:
                    json.dump(annotated_data, outfile, indent=4)
                
                print(f"Annotated file saved to: {output_file_path}")

if __name__ == "__main__":
    # Clean up the output directory if it already exists
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.makedirs(output_directory, exist_ok=True)

    # Start the annotation process
    annotate_and_save_ground_truth(input_directory, output_directory)
    print("\nAnnotation process complete. Files saved to 'ground_truth_responses'.")
