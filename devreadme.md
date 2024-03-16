to use pytest,

```
pip install -r requirements.txt
pytest-watch --runner="pytest --testmon"
```

if you get any import errors, try setting PYTHONPATH environment variable

macos
```
pwd
export PYTHONPATH = {result of pwd}
```

