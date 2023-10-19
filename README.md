# Recipe-Service


## Development

Make a `.env` file in the root directory and create a variable write the following:
```python
DB_CONN="<YOUR_SQLALCHEMY_STRING>"
```

Then do the following in powershell:

```sh
python -m .venv venv
.venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
```

on macOS/Linux you might need to do `source .venv\Scripts\activate` and `.venv/Scripts/activate.bat` in windows CMD

## Start Micro Service
```sh
uvicorn app.server:app --reload
```

## Test
```sh
pytest tests
```
