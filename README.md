# MySQL-Python Connector

## Conda

### Install Conda

### Installing this connector with Conda

Create environment <name> = project-env

`conda create --name <name>`

Activate environment

`conda activate project-env`

`conda list --explicit > spec-file.txt`

`conda create --name <env> --file spec-file.txt`


## PIP

### Install PIP

### Installing this connector with PIP

Defining the virtual environment folder
```
python3 -m venv .venv
```

Windows (Command Prompt).
```
.venv\Scripts\activate
```

Windows (PowerShell).
```
.venv\Scripts\Activate.ps1
```

macOS/Linux.
```
source .venv/bin/activate
```

Deactivate.
```
deactivate
```

## UV

### Install UV

## Examples

```
python3 connector.py -h 145.128.456.789 -u user -p 'ThePassword%' -d database -r 3306 -q "SELECT * FROM table"
```

```
echo "SELECT * FROM users WHERE created_at > '2024-01-01'" | python3 connector.py -h localhost -u root -p password -d mydb
```

```
cat complex_query.sql | python3 connector.py -h db.server.com -u admin -p secret -d production
```
