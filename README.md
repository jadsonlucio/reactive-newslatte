# Newsletter

A ideia desse projeto é criar um newsletter personalizado utilizando programação reativa. Esse newsletter vai conter uma lista de topicos que vão estar armazenados em diferentes fontes de dados (inicialmente o redis). O newsletter também deve ser enviado para a lista de usuário que estiverem acessando ele.


# Instação 

Executar os seguintes passos:

1. Criar um virtualenv executando o seguinte comando: `virtualenv venv`
2. Instalar os requirements executando o comando: `pip install -r requirements.txt`


# Testes

1. Executar o redis atravez do docker-compose rodando: `docker-compose up -d`
2. Executar o serviço do observable rodando: `python main.py`
