#!/usr/bin/env python3
import re
import requests
import argparse

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

REGEX_ERROR_CODE = re.compile(r'<p>(\d+)\s\((0x[A-F0-9]+)\)</p>')
REGEX_ERROR_MSG = re.compile(r'\<span id="([A-Z_]+)"\>')
REGEX_ERROR_DESC = re.compile(r'<p>([\w\s]+\.)</p>')


def parseMSErrorCodeResponse(resp: requests.Response):
    messages = REGEX_ERROR_MSG.findall(resp.text)
    codes = REGEX_ERROR_CODE.findall(resp.text)
    descriptions = REGEX_ERROR_DESC.findall(resp.text)
    zipped = zip(messages, codes, descriptions)
    return zipped

def findErrorCode(searchinput:str, searchtype: str, errorCodes: list=[]) -> list:
    searchtypes = [
        "message",
        "code",
        "description"
    ]
    idx = searchtypes.index(searchtype)
    return list(filter(lambda e: searchinput in e[idx], errorCodes))
    

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
    parser.add_argument('-t', '--type', help="The type of input you are searching for. Default: message", choices=["message", "code", "description", "auto"], default="auto")
    parser.add_argument('search_term', help="The term to search for, partial matches apply")

    args = parser.parse_args()
    arg_type = args.type

    allErrors = []

    for url in microsoft_error_code_urls:
        resp = requests.get(url)
        allErrors += parseMSErrorCodeResponse(resp)

    if args.search_term.split('_')[0].isupper():
        arg_type = "message"
    elif args.search_term.isnumeric() or args.search_term.startswith("0x"):
        arg_type = "code"
    else:
        arg_type = "description"


    for result in findErrorCode(args.search_term, arg_type, allErrors):
        description = Text(result[2])
        description.highlight_words([args.search_term], style="on blue")


        console.print(Panel(
            description, 
            title=f"[bold][red]{result[0]}", 
            subtitle=f"[yellow]{result[1][0]} [magenta]({result[1][1]})",
            padding=2,
            highlight=True,
            width=50,
            title_align="left",
            subtitle_align="right"
        ))
