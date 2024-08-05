[![PyPI](https://img.shields.io/pypi/v/hotmodern-python.svg)](https://pypi.org/project/hotmodern-python/)
[![Tests](https://github.com/hotenov/hotmodern-python/actions/workflows/tests.yml/badge.svg)](https://github.com/hotenov/hotmodern-python/actions/workflows/tests.yml)
[![codecov.io](https://codecov.io/github/hotenov/hotmodern-python/coverage.svg?branch=main)](https://codecov.io/github/hotenov/hotmodern-python/coverage.svg?branch=main)
[![Docs](https://readthedocs.org/projects/hotmodern-python/badge/?version=latest)](https://hotmodern-python.readthedocs.io/en/latest/?badge=latest)
[![Nox](https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg)](https://github.com/wntrblm/nox)

# hotmodern-python

My Python learning project by article series '[Hypermodern Python](https://cjolowicz.github.io/posts/)' (by [Claudio Jolowicz](https://github.com/cjolowicz))

This repo 98% repeats code from these articles
with little improvements for Windows environment *(see below)*
and except several components
(pre-commit, pytype, typeguard, Release Drafter)

## Notes for Windows host

**Updated:** 2024-08-05

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
        session.install("-r", f"{requirements.name}", *args, **kwargs)
    pathlib.Path(requirements.name).unlink()
```

### Run Nox sessions with pyenv's Python versions

On Windows I use [pyenv-win](https://github.com/pyenv-win/pyenv-win)
for managing Python interpreter versions.

If you set up `pyenv-win` correctly,
it lets you run your session against multiple interpreters by specifying
`python` to `@nox.session`
(and run sessions the same way as on Linux machines).

```python
@nox.session(python=["3.11", "3.12"], reuse_venv=True)
def tests(session: Session) -> None:
...
```

**The main thing** you should do is setting paths to Python interpreters
in the right order in your `PATH` environment variable on Windows.  
I wrote a detailed tutorial on their wiki page
[Configure the order in PATH variable](https://github.com/pyenv-win/pyenv-win/wiki#configure-the-order-in-path-variable)  
But to avoid many problems related to discover a Python interpreter version,
**you also have to add paths for all installed versions of Python**
"below" *(after)* path to `...\pyenv-win\shims`
For example your PATH might look as:

```plain
D:\python_tools\.pyenv\pyenv-win\bin
D:\python_tools\.pyenv\pyenv-win\shims\
D:\python_tools\.pyenv\pyenv-win\versions\3.8.10
D:\python_tools\.pyenv\pyenv-win\versions\3.9.13
D:\python_tools\.pyenv\pyenv-win\versions\3.10.8
D:\python_tools\.pyenv\pyenv-win\versions\3.11.2
D:\python_tools\.pyenv\pyenv-win\versions\3.12.4
```

> [!IMPORTANT]  
> If you encountered with Nox error:
>
> ```plain
> ... failed with exit code 1:  
> PEP-514 violation in Windows Registry at HKEY_CURRENT_USER/PythonCore/...
> ```
>
> for modern Python 3.12+ you must reinstall this version with `--register` CLI option
>
> ```plain
> pyenv uninstall 3.12.4
> pyenv install 3.12.4 --register
> ```
>
> Don't forget to restart your Terminal window (or IDE) to apply these changes.
