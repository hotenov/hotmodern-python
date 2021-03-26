import nox


locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.9.2"], reuse_venv=True)
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=["3.9.2"], reuse_venv=True)
def lint(session):
    args = session.posargs or locations
    session.install("flake8")
    session.run("flake8", *args)
