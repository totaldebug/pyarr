from __future__ import annotations

import nox
from nox.sessions import Session


@nox.session(reuse_venv=True)
def format(session: Session) -> None:
    """Run automatic code formatters"""
    session.run("poetry", "install", external=True)
    session.run("black", ".")
    session.run("isort", ".")
    session.run("autoflake", "--in-place", ".")


@nox.session(reuse_venv=True)
def coverage(session: Session) -> None:
    """Check tests cover all code"""
    session.run("poetry", "install", external=True)
    session.run("pytest", "tests", "--cov=pyarr", "--cov-report", "term-missing", "-vv")


@nox.session(reuse_venv=True)
def test(session: Session) -> None:
    """Run the complete test suite"""
    session.run("poetry", "install", external=True)
    session.notify("test_types")
    session.notify("test_style")
    session.notify("test_suite")


@nox.session(reuse_venv=True)
def docker_test(session: Session) -> None:
    """Run the complete test suite"""
    session.notify("test_docker_start")
    session.notify("test_types")
    session.notify("test_style")
    session.notify("test_suite")
    session.notify("test_docker_stop")


@nox.session(reuse_venv=True)
def test_docker_start(session: Session) -> None:
    session.run(
        "docker",
        "compose",
        "-f",
        ".devcontainer/docker-compose.yml",
        "pull",
        external=True,
    )
    session.run(
        "docker",
        "compose",
        "--project-name",
        "pyarr_devcontainer",
        "-f",
        ".devcontainer/docker-compose.yml",
        "up",
        "-d",
        external=True,
    )


@nox.session(reuse_venv=True)
def test_docker_stop(session: Session) -> None:
    session.run(
        "docker",
        "compose",
        "--project-name",
        "pyarr_devcontainer",
        "-f",
        ".devcontainer/docker-compose.yml",
        "down",
        external=True,
    )


@nox.session(reuse_venv=True)
def test_suite(session: Session) -> None:
    """Run the Python-based test suite"""
    session.run("poetry", "install", external=True)
    session.run("pytest", "tests")


@nox.session(reuse_venv=True)
def test_types(session: Session) -> None:
    """Check that typing is working as expected"""
    session.run("poetry", "install", external=True)
    session.run("mypy", "--show-error-codes", "pyarr")


@nox.session(reuse_venv=True)
def test_style(session: Session) -> None:
    """Check that style guidelines are being followed"""
    session.run("poetry", "install", external=True)
    session.run("flake8", "pyarr", "tests")
    session.run(
        "black",
        ".",
        "--check",
    )
    session.run("isort", ".", "--check-only")
    session.run("autoflake", ".")
    session.run("interrogate", "pyarr")


@nox.session(reuse_venv=True)
def docs(session: Session) -> None:
    """Create local copy of docs for testing"""
    session.run("poetry", "install", external=True)
    session.run("sphinx-build", "sphinx-docs", "build")
