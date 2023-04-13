FROM mcr.microsoft.com/devcontainers/python:latest

RUN apt update && apt upgrade -y

RUN apt install -y zsh python3-sphinx

# Poetry
ARG POETRY_VERSION="latest"
RUN if [ "$POETRY_VERSION" = "latest" ]; then su vscode -c "umask 0002 && sudo pip3 install poetry"; fi
RUN if [ "$POETRY_VERSION" != "none" && "$POETRY_VERSION" != "latest" ]; then su vscode -c "umask 0002 && sudo pip3 install poetry==$POETRY_VERSION"; fi

# Nox
ARG NOX_VERSION="latest"
RUN if [ "$NOX_VERSION" = "latest" ]; then su vscode -c "umask 0002 && sudo pip3 install nox-poetry nox"; fi
RUN if [ "$NOX_VERSION" != "none" && "$POETRY_VERSION" != "latest" ]; then su vscode -c "umask 0002 && sudo pip3 install nox-poetry nox==$NOX_VERSION"; fi

RUN wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O - | zsh || true

CMD ["zsh"]
