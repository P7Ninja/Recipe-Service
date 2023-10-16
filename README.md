# Recipe-Service


## Development

Windows Powershell:
```sh
python -m .venv venv
.venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Start Micro Service
```sh
uvicorn app.server:app --reload
```

## Test
```sh
pytest tests
```
