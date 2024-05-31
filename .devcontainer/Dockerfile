FROM mcr.microsoft.com/devcontainers/python:latest

RUN apt update && apt upgrade -y

RUN apt install -y zsh python3-sphinx

# Poetry
RUN su vscode -c "umask 0002 && sudo pip3 install poetry"

# Nox
RUN su vscode -c "umask 0002 && sudo pip3 install nox-poetry nox"

RUN wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O - | zsh || true

RUN poetry config virtualenvs.in-project true

CMD ["zsh"]
