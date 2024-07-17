import os
import openai
from dotenv import load_dotenv


def convert_aws_tf_to_azm_tf(input_dir, output_dir):
    # Traverse the directory tree
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".tf"):
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                target_dir = os.path.join(output_dir, relative_path.replace("aws", "azm"))
                os.makedirs(target_dir, exist_ok=True)
                # Change the file extension from .tf to .json
                # target_file = os.path.splitext(file)[0] + ".tf"
                # Construct the full path to the target file
                target_path = os.path.join(target_dir, file)
                # Read the content of the source file
                with open(source_path, 'r') as f:
                    file_content = f.read()
                # Get the conversion result
                result = convert_aws_to_azure_terraform(file_content)
                with open(target_path, 'w') as tf:
                        tf.write(result)
                print(f"Converted {source_path} to {target_path}")
                print("Converted...")
                
                
def convert_aws_to_azure_terraform(aws_terraform_code):
    # Create a prompt for ChatGPT
#     prompt = f"Convert the following AWS Terraform IaC to an Azure Terraform IaC template, Provide the complete Azure Terraform template."
    messages=[
        {"role": "system", "content": "Convert the following AWS Terraform IaC to an Azure Terraform IaC template, Provide the complete Azure Terraform template "},
            {"role": "system", "content": "You are a helpful assistant that converts AWS Terraform IaC to Azure Terraform IaC."},
            {"role": "user", "content": aws_terraform_code}
        ]
    # Use OpenAI's Chat Completion
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

    azure_terraform_code = response.choices[0].message.content
    return azure_terraform_code


def main():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = openai_api_key
    input_dir = "terraform_file"#input("Enter or paste Input directory: ")
    output_dir = "output"#input("Enter or paste output directory: ")
    print("Processing......")
    convert_aws_tf_to_azm_tf(input_dir, output_dir)
    print("Processing Completed... ")

if __name__ == "__main__":
    main()
    
