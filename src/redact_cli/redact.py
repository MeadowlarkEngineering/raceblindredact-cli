"""
Command Line Interface for redact-cli
"""

import argparse
import os
from mimetypes import guess_type
from pathlib import Path
from requests import post
from redact_cli._version import __version__

token_path = Path.home() / ".redact_api_token"
REDACT_API_TOKEN = "REDACT_API_TOKEN"


def prompt_for_token() -> str:
    """
    Prompts user for the API Token
    """
    print(
        f"""
A token is required to use the RaceBlindRedact.com API.
There are three options for providing the token:
  1. You can set the {REDACT_API_TOKEN} environment variable
  2. You can provide a token on the command line using the --token option,
  3. You can save the token to the file {token_path}
                   
"""
    )
    response = input(
        "Do you want to enter the token and save it to $HOME/.redact_api_token (y/n)? "
    )
    if response.lower() == "y":
        token = input("Enter your API Token: ")
        with token_path.open("w") as f:
            f.write(token)
        return token


def find_token() -> str:
    """
    Find the API Token
    """
    token = None
    if REDACT_API_TOKEN in os.environ:
        token = os.environ[REDACT_API_TOKEN]
    elif token_path.exists():
        with token_path.open() as f:
            token = f.read().strip()
    if not token:
        token = prompt_for_token()
    return token


def redact(input_file: Path, output_file: Path, mode, token, api_url, remove=None, keep=None):
    """
    Redact the input file and write the redacted text to the output file
    """
    
    if not input_file.exists():
        print(f"Error: {input_file} does not exist")
        return
    
    try:
        files = {
            "file": (input_file.name, open(input_file, "rb"), guess_type(input_file.name)[0])
        }
        data = [
            ("mode", mode)
        ]
 
        if remove:
            for r in remove:
                data.append(("blacklist", r))

        if keep:
            for k in keep:
                data.append(("whitelist", k))

        response = post(f"{api_url}/redact", 
                        headers = {
                            "Authorization": f"Bearer {token}",
                            "Accept": "application/pdf"},
                        files=files,
                        data=data
        )
        response.raise_for_status()

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "wb") as f:
            f.write(response.content)

    except Exception as e:
        print(f"Error: {e}")
        
def main():
    parser = argparse.ArgumentParser(
        description="Redact case materials using RaceBlindRedact.com"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["text", "image"],
        help="Redaction Mode",
        default="image",
    )
    parser.add_argument("--token", "-t", help="API Token for RaceBlindRedact.com")
    parser.add_argument(
        "--api-url",
        "-u",
        help="API URL for RaceBlindRedact.com. default: https://api.raceblindredact.com",
        default="https://api.raceblindredact.com",
    )
    parser.add_argument("input", type=Path, help="Input file to redact")
    parser.add_argument("output", type=Path, help="Output file to write redacted text")
    parser.add_argument("--remove", "-r", type=str, nargs="*", help="Terms to remove")
    parser.add_argument("--keep", "-k", type=str, nargs="*", help="Terms to keep")

    args = parser.parse_args()

    token = args.token or find_token()
    if not token:
        print("API Token not found")
        return

    redact(args.input, args.output, args.mode, token, args.api_url, remove=args.remove, keep=args.keep)

if __name__ == "__main__":
    main()