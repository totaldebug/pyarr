FROM python:latest

RUN apt update

RUN apt upgrade  -y

RUN apt install zsh python3-sphinx -y

RUN pip install --user poetry nox
ENV PATH="${PATH}:/root/.local/bin"

RUN wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O - | zsh || true

CMD ["zsh"]
