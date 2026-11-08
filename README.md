# SGCE

## Executando a aplicação


### Execução com Docker

Primeiramente, crie um arquivo `config.env` de acordo com o arquivo `config.env.example` na raiz da aplicação:
```
cp config.env.example config.env
```

Esta aplicação possui um ambiente de desenvolvimento em Docker, onde é possível executar fazer alterações e executar o código dentro de um container com hot reload. Para isso você necessitará do `docker-compose` instalado em sua máquina.

Para executar a aplicação, use o seguinte comando:
```
docker-compose up
```

___

### Execução local

Como as bibliotecas necessárias estão numa versão bem legada é necessário a criação de um ambiente virtual utilizando o [`pyenv`](https://github.com/pyenv/pyenv).

Após instalar o `pyenv`:

Instale a versão 3.6.2 do Python:
```
pyenv install 3.6.2
```


Depois disso crie um ambiente virtual com o seguinte comando:
```
pyenv virtualenv 3.6.2 env
```

Ative o virtual env:
```
pyenv activate env
```

Instale as dependências:
```
pip install -r requirements.txt
```

Execute as migrações:
```
python manage.py migrate
```

Execute a aplicação:
```
DEBUG=True && python manage.py runserver
```