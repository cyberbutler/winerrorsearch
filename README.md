# winerrorsearch
A small utility script for resolving and searching Win32 Error Messages, by title, error code, or description

## Requirements
- [Rich](https://github.com/Textualize/rich)
- requests
```bash
pip3 install rich requests
```

## Installation
```bash
git clone https://github.com/cyberbutler/winerrorsearch
cd winerrorsearch/
chmod+x winerrorsearch.py

# Add to your .bashrc for easy usage:
alias wes="/path/to/winerrorsearch.py"
```

## Usage
```
usage: winerrorsearch.py [-h] [-t {message,code,description,auto}] [-s] search_term

Search for a Win32 Error Code

positional arguments:
  search_term           The term to search for, partial matches apply

options:
  -h, --help            show this help message and exit
  -t {message,code,description,auto}, --type {message,code,description,auto}
                        The type of input you are searching for. Default: auto
  -s, --save            Save the results to ~/.winerrorcodes.json and skip future requests to microsoft to retrieve the
                        codes. Re-execute with this flag to redownload the results.
```

## Examples
![image](https://user-images.githubusercontent.com/46307021/191973691-7b8c8275-a6fd-4326-9fb8-ad20a2be1d9b.png)
![image](https://user-images.githubusercontent.com/46307021/191973803-7d2466b7-b8ed-420c-b944-5221f82eb54a.png)

