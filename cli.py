#!/usr/bin/python

import boto3
import json
from typing import Optional

def get_bedrock_claude_response(prompt: str,
                              temperature: float = 0.7,
                              max_tokens: Optional[int] = None) -> str:
    """
    Call Claude 3 Sonnet on AWS Bedrock and get a response.
    
    Args:
        prompt (str): The input prompt to send to the API
        temperature (float): Controls randomness (0-1, default: 0.7)
        max_tokens (int, optional): Maximum tokens in response
        
    Returns:
        str: The API response text
    """
    try:
        # Initialize Bedrock client
        bedrock = boto3.client('bedrock-runtime')
        
        # Prepare the request body
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens if max_tokens else 4096,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature
        }
        
        # Call Bedrock
        response = bedrock.invoke_model(
            modelId="us.anthropic.claude-3-5-sonnet-20240620-v1:0",
            body=json.dumps(request_body)
        )
        
        # Parse the response
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
    
    except Exception as e:
        print(f"Error calling Bedrock API: {str(e)}")
        return ""

def get_openai_response(prompt: str, 
                       model: str = "gpt-3.5-turbo",
                       temperature: float = 0.7,
                       max_tokens: Optional[int] = None) -> str:
    """
    Call OpenAI API and get a response.
    
    Args:
        prompt (str): The input prompt to send to the API
        model (str): The model to use (default: gpt-3.5-turbo)
        temperature (float): Controls randomness (0-1, default: 0.7)
        max_tokens (int, optional): Maximum tokens in response
        
    Returns:
        str: The API response text
    """
    try:
        # Initialize the client
        client = OpenAI()
        
        # Create the chat completion with the new client
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return ""


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Get responses from OpenAI or Bedrock')
    parser.add_argument('--provider', type=str, choices=['openai', 'bedrock'],
                      default='bedrock', help='The API provider to use')
    parser.add_argument('prompt', type=str, help='The input prompt to send to the API')
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo',
                      help='The model to use (default: gpt-3.5-turbo)')
    parser.add_argument('--temperature', type=float, default=0.7,
                      help='Controls randomness (0-1, default: 0.7)') 
    parser.add_argument('--max-tokens', type=int,
                      help='Maximum tokens in response')

    args = parser.parse_args()
    
    if args.provider == 'openai':
        response = get_openai_response(
            prompt=args.prompt,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
    else:
        response = get_bedrock_claude_response(
            prompt=args.prompt,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
    
    print(response)

if __name__ == '__main__':
    main()

