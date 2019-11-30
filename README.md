# To start up (using powershell)
```
python -m venv venv
.\venv\Scripts\Activate.ps1      # Initialize virtualenv
pip install -r requirements.txt  # Install python libraries 
$env:FLASK_APP = "app.py"
flask run
```

## Tips
To save pip depedencies in requirements.txt:
`pip freeze > requirements.txt`