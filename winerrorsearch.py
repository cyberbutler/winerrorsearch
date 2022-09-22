#!/usr/bin/env python3
import os
import re
import json
import requests
import argparse

from rich.progress import Progress
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

REGEX_ERROR_CODE = re.compile(r'<p>(\d+)\s\((0x[A-F0-9]+)\)</p>')
REGEX_ERROR_MSG = re.compile(r'\<span id="([A-Z_]+)"\>')
REGEX_ERROR_DESC = re.compile(r'<p>([\w\s]+\.)</p>')


def convertErrorCodesTupleToDict(errorcodetuple):
    return [{
            "message": e[0],
            "code": list(e[1]),
            "description": e[2]
        } for e in errorcodetuple]


def parseMSErrorCodeResponse(resp: requests.Response):
    messages = REGEX_ERROR_MSG.findall(resp.text)
    codes = REGEX_ERROR_CODE.findall(resp.text)
    descriptions = REGEX_ERROR_DESC.findall(resp.text)
    zipped = zip(messages, codes, descriptions)
    return zipped

def findErrorCode(searchinput:str, searchtype: str, errorCodes: list=[]) -> list:
    return list(filter(lambda e: searchinput in e[searchtype], errorCodes))
    

microsoft_error_code_urls = [
    "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-",
    "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--500-999-",
    "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--1000-1299-",
    "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--1300-1699-",
    "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--1700-3999-",
    "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--4000-5999-",
    "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--6000-8199-",
    "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--8200-8999-",
    "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--9000-11999-",
    "https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--12000-15999-"
]



if __name__ == "__main__":
    console = Console()

    parser = argparse.ArgumentParser(description="Search for a Win32 Error Code")
    parser.add_argument('-t', '--type', help="The type of input you are searching for. Default: auto", choices=["message", "code", "description", "auto"], default="auto")
    parser.add_argument('-s', '--save', help="Save the results to ~/.winerrorcodes.json and skip future requests to microsoft to retrieve the codes. Re-execute with this flag to redownload the results.", action="store_true", default=False)
    parser.add_argument('search_term', help="The term to search for, partial matches apply")

    args = parser.parse_args()
    arg_type = args.type

    if not os.path.exists(f"{os.path.expanduser('~')}/.winerrorcodes.json") or args.save:
        console.print("[[green]+[/green]] Fetching results from microsoft") 
        allErrorsTuple = []
        with Progress() as progress:
            task = progress.add_task("[green]Downloading:", total=len(microsoft_error_code_urls))
            for url in microsoft_error_code_urls:
                resp = requests.get(url)
                allErrorsTuple += parseMSErrorCodeResponse(resp)
                progress.advance(task)
        
        allErrors = convertErrorCodesTupleToDict(allErrorsTuple)

        if args.save:
            console.print("[[green]+[/green]] Saving to results ~/.winerrorcodes.json")
            with open(f"{os.path.expanduser('~')}/.winerrorcodes.json", "w") as f:
                f.write(json.dumps(allErrors))

    else:
        with open(f"{os.path.expanduser('~')}/.winerrorcodes.json", 'r') as f:
            allErrors = json.load(f)

    if args.search_term.split('_')[0].isupper():
        arg_type = "message"
    elif args.search_term.isnumeric() or args.search_term.startswith("0x"):
        arg_type = "code"
    else:
        arg_type = "description"


    for result in findErrorCode(args.search_term, arg_type, allErrors):
        description = Text(result.get("description"))
        description.highlight_words([args.search_term], style="on blue")


        console.print(Panel(
            description, 
            title=f"[bold][red]{result.get('message')}", 
            subtitle=f"[yellow]{result.get('code')[0]} [magenta]({result.get('code')[1]})",
            padding=2,
            highlight=True,
            width=50,
            title_align="left",
            subtitle_align="right"
        ))
