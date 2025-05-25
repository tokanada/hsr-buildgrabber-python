# HSR Relic Fetch

Fetches builds from your HSR Showcase using Enka API and converts it into JSON format for HSR Private Servers

## Prerequisites

* Python >=3.10
* Git

## How to run

### Windows
```powershell
# Clone this repository
git clone "https://github.com/tokanada/hsr-relic-fetch"

# Go to folder
cd hsr-relic-fetch

# Create new Python Virtualenv
python.exe -m venv venv

# Activate Virtualenv
source .\venv\bin\activate

# Install requirements
python.exe -m pip install -r requirements.txt

# Run Applet
python.exe main.py
```

### Linux/Mac
```bash
# Clone this repository
git clone "https://github.com/tokanada/hsr-relic-fetch"

# Go to folder
cd hsr-relic-fetch

# Create new Python Virtualenv
python -m venv venv

# Activate Virtualenv
source ./venv/bin/activate

# Install requirements
python -m pip install -r requirements.txt

# Run Applet
python main.py
```
## Special Thanks to
* [enka.py](https://github.com/seriaati/enka-py)
* [enka.network](https://enka.network/)
