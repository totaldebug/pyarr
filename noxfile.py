from __future__ import annotations

import os
import subprocess

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
def tests(session: Session) -> None:
    """Run the complete test suite"""
    if os.environ.get("GITHUB_ACTIONS") == "true":
        session.notify("test_types")
        session.notify("test_style")
        session.notify("test_suite")
    else:
        session.notify("docker_test")


@nox.session(reuse_venv=True)
def docker_test(session: Session) -> None:
    """Run the complete test suite"""
    session.notify("test_create_containers")
    session.notify("test_types")
    session.notify("test_style")
    session.notify("test_suite")
    session.notify("test_cleanup_containers")


@nox.session(reuse_venv=True)
def test_create_containers(session: Session) -> None:
    session.run(
        "sudo",
        "docker",
        "compose",
        "-f",
        ".devcontainer/docker-compose.yml",
        "pull",
        external=True,
    )
    hostname = subprocess.check_output(["hostname"]).strip().decode("utf-8")
    inspect_command = [
        "sudo",
        "docker",
        "inspect",
        "--format",
        '{{ index .Config.Labels "com.docker.compose.project" }}',
        hostname,
    ]
    project_name = subprocess.check_output(inspect_command).strip().decode("utf-8")

    session.run(
        "sudo",
        "docker",
        "compose",
        "--project-name",
        project_name,
        "-f",
        ".devcontainer/docker-compose.yml",
        "up",
        "-d",
        external=True,
    )


@nox.session(reuse_venv=True)
def test_cleanup_containers(session: Session) -> None:
    # Get the container IDs using the filter
    hostname = subprocess.check_output(["hostname"]).strip().decode("utf-8")
    project_name_command = [
        "sudo",
        "docker",
        "inspect",
        "--format",
        '{{ index .Config.Labels "com.docker.compose.project" }}',
        hostname,
    ]
    project_name = subprocess.check_output(project_name_command).strip().decode("utf-8")
    container_filter = f"label=com.docker.compose.project={project_name}"

    # Execute the `docker ps` command and filter the output using grep
    cmd1 = ["sudo", "docker", "ps", "-a", "-q", "--filter", container_filter]
    cmd2 = ["grep", "-v", hostname]
    output1 = subprocess.run(cmd1, stdout=subprocess.PIPE)
    output2 = subprocess.run(cmd2, input=output1.stdout, stdout=subprocess.PIPE)

    # Get the container IDs from the output
    container_ids = output2.stdout.decode("utf-8").strip().split()

    # Kill and remove the containers, cant use docker compose down as that kills
    # the workspace container for devcontainer. this works just as well.
    for container_id in container_ids:
        session.run("sudo", "docker", "kill", container_id, silent=True, external=True)
        session.run("sudo", "docker", "rm", container_id, silent=True, external=True)


@nox.session(reuse_venv=True)
def test_suite(session: Session) -> None:
    """Run the Python-based test suite"""
    session.run("poetry", "install", external=True)
    session.run(
        "pytest",
        "--showlocals",
        "--reruns",
        "3",
        "--reruns-delay",
        "5",
        "--cov=pyarr",
        "--cov-report",
        "xml",
        "--cov-report",
        "term-missing",
        "-vv",
    )


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
        "pyarr",
        "--check",
    )
    session.run("isort", "pyarr", "--check-only")
    session.run("autoflake", "-r", "pyarr")
    session.run("interrogate", "pyarr")


@nox.session(reuse_venv=True)
def docs(session: Session) -> None:
    """Create local copy of docs for testing"""
    session.run("poetry", "install", external=True)
    session.run("sphinx-build", "sphinx-docs", "build")
