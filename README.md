# MySQL-Python Connector

Note: This module is offered as an example of an ODVF connector using Python and MySQL. It is subject to verification by the technical team that implements it and is used at the installer's own risk.

## Conda

Conda is an open-source, cross-platform, language-agnostic package manager and environment management system. It was originally developed to solve package management challenges faced by Python data scientists, and today is a popular package manager for Python and R.

[Conda (Wikipedia Definition)](https://en.wikipedia.org/wiki/Conda_(package_manager))

### Installing Conda

### Installing this connector with Conda

Create environment <name> = project-env

`conda create --name <name>`

Activate environment

`conda activate project-env`

`conda list --explicit > requirements.conda.txt`

`conda create --name <env> --file requirements.conda.txt`


## PIP

pip (also known by Python 3's alias pip3) is a package manager (package management system) written in Python and is used to install and manage software packages. The Python Software Foundation recommends using pip to install Python applications and its dependencies during deployment. Pip connects to an online software repository of public packages, named the Python Package Index (PyPI). Pip can be configured to connect to other package repositories (local or remote), provided that they comply to Python Enhancement Proposal 503.

[PIP (Wikipedia Definition)](https://en.wikipedia.org/wiki/Pip_(package_manager))

### Installing PIP

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

UV is an extremely fast Python package and project manager, written in Rust.

### Install UV

[UV Installing Docs](https://docs.astral.sh/uv/getting-started/installation/)

## Examples

```
python3 connector.py -t localhost -u user -p 'password' -d mydb -r 3306 -f json --pretty -q "SELECT * FROM user LIMIT 10"
```

```
echo "SELECT * FROM user WHERE created_at > '2024-01-01'" | python3 connector.py -t localhost -u user -p password -d mydb -f table
```

```
cat users.sql | python3 connector.py -t localhost -u user -p password -d mydb -f csv
```
