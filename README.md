# hotmodern-python

My Python learning project by article series '[Hypermodern Python](https://cjolowicz.github.io/posts/)' (by [Claudio Jolowicz](https://github.com/cjolowicz))

This repo 98% repeats code from these articles
with little improvements for Windows environment
and except several components
(pre-commit, typeguard)

## Notes for Windows host

### Functions with temp file on Windows

Windows has security limitation for temp files:
OS does not allow processes other than the one used to create the NamedTemporaryFile to access the file
([from here](https://github.com/bravoserver/bravo/issues/111#issuecomment-826990))

That's why I modified code like this:

```python
# noxfile.py
import pathlib

def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file."""
    with tempfile.NamedTemporaryFile(delete=False) as requirements:
        session.run(
            "poetry",
            "export",
            ...
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)
    pathlib.Path(requirements.name).unlink()
```

### Run Nox sessions with pyenv's Python versions

#### Option A

Use Nox CLI argument `--extra-pythons` and full paths to desired version of Python interpreter

Example:

```powershell
nox --extra-pythons "C:\users\winfan\.pyenv\pyenv-win\versions\3.8.2\python.exe" "C:\users\winfan\.pyenv\pyenv-win\versions\3.9.2\python.exe"
```

will run all sessions with Python specified in noxfile.py _(or skip if not found)_
and with all Pythons passed in this command.
See [detailed explanation](https://github.com/theacodes/nox/issues/412#issuecomment-810425155) how `--extra-pythons` and `--extra-python` works from Claudio Jolowicz himself

#### Option B

Create separate noxfile for local execution.
Duplicate all sessions and change python versions like this:

```python
# noxfile.local.py

@nox.session(
    python=[
        r"C:\users\winfan\.pyenv\pyenv-win\versions\3.8.2\python.exe",
        r"C:\users\winfan\.pyenv\pyenv-win\versions\3.9.2\python.exe",
    ],
    reuse_venv=True,
)
```

Then run command in your Terminal `nox -f noxfile.local.py`  
Don't forget to add this file to `.gitignore`
