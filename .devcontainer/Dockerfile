FROM python:latest

RUN apt update
RUN apt upgrade  -y
RUN apt install lsb-release -y

RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

RUN echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

RUN apt update

RUN apt install zsh python3-sphinx docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

RUN pip install --user poetry nox
ENV PATH="${PATH}:/root/.local/bin"

RUN wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O - | zsh || true

CMD ["zsh"]
