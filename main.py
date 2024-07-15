import os
import openai
from dotenv import load_dotenv
import json


def convert_tf_to_arm(input_dir, output_dir):
    # Traverse the directory tree
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".tf"):
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                target_dir = os.path.join(output_dir, relative_path.replace("aws", "azm"))
                os.makedirs(target_dir, exist_ok=True)
                # Change the file extension from .tf to .json
                target_file = os.path.splitext(file)[0] + ".json"
                # Construct the full path to the target file
                target_path = os.path.join(target_dir, target_file)
                # Read the content of the source file
                with open(source_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                # Get the conversion result
                result = create_chat_response(file_content).replace("\n","").rstrip()
                # out = clean_json(result)
                print(is_json(result))
                # print(result)
                json_object = json.loads(result)
                # Write the result to the target file in JSON format
                with open(target_path, 'w', encoding='utf-8') as f:
                    json.dump(json_object, f, indent=4, sort_keys=True)

                print(f"Converted {source_path} to {target_path}")
                print("Converted...")
                
                
def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


# Function to convert Terraform to Azure ARM
def create_chat_response(message):
    messages = [
        {"role": "system", "content": "Convert the following Terraform code to an Azure Resource Manager (ARM) template and \
         give the completed json format dont inlcude apiVersion this is gpt generated code of arm file could you explain me remove this from gpt response need code to \
         remove this line dont give complete summary code show remove response code "},
        {"role": "user", "content": message},
        {"role": "assistant", "content": message}
    ]
    
    response = openai.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            temperature=0.5,
            max_tokens=1200,
            top_p=1,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0
        )
    
    return response.choices[0].message.content

def main():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = openai_api_key
    input_dir = "terraform_file"#input("Enter or paste Input directory: ")
    output_dir = "output"#input("Enter or paste output directory: ")
    print("Processing......")
    convert_tf_to_arm(input_dir, output_dir)
    print("Processing Completed... ")

if __name__ == "__main__":
    main()
    

