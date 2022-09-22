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
usage: winerrorsearch.py [-h] [-t {message,code,description,auto}] search_term

Search for a Win32 Error Code

positional arguments:
  search_term           The term to search for, partial matches apply

optional arguments:
  -h, --help            show this help message and exit
  -t {message,code,description,auto}, --type {message,code,description,auto}
                        The type of input you are searching for. Default: auto
```

## Examples
<img width="612" alt="image" src="https://user-images.githubusercontent.com/46307021/191639222-2885c8cd-54fa-4825-a741-ecb939ed22f7.png">
<img width="605" alt="image" src="https://user-images.githubusercontent.com/46307021/191638792-485ba6ce-215e-416a-af64-bf9044853774.png">
<img width="626" alt="image" src="https://user-images.githubusercontent.com/46307021/191639026-8c388f8d-a8a4-41c2-b798-4eeffdd8bff6.png">
