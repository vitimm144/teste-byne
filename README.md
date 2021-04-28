[![CI](https://github.com/vitimm144/teste-byne/actions/workflows/main.yml/badge.svg)](https://github.com/vitimm144/teste-byne/actions/workflows/main.yml)
[![Build Status](https://travis-ci.org/vitimm144/teste-byne.svg?branch=main)](https://travis-ci.org/vitimm144/teste-byne)
# teste-byne
Teste com microserviços em python
- Even Generator: Gera números pares aleatórios entre 0 e 1000;
- Odd Generator: Gera números ímpares aleatórios entre 0 e 1000;
- Multiply Publisher: A cada 500ms, requisita números do serviço Even e Odd e faz a multiplicação entre os dois números recebidos. Caso o número multiplicado seja maior que 100000, publica esse número para o RabbitMQ
- Multiply api: Busca os numeros publicados na fila do RabbitMQ, armazena no mongodb tem uma chamada rpc para servir os últimos 1000 números publicados;
- Client: Frontend que conecta na api e faz uma chamada rpc para exibir os últimos 100 numeros. 

# Run project

docker-compose up -d

O serviço do rabbitmq pode demorar a subir, esperar por algum tempo e acessar:

http://localhost:8080

clique no botão pra buscar os resgistros ou atualizar os registros gerados pelo serviços

