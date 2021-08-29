Mega Sena
=========

Este é um App Backend realizado em Django responsável por gerar jogos randomicos de Mega Sena. Ele possui uma camada de autenticação utilizando tokens JWT, sendo necessária a autenticação para o consumo dos recursos. Para utiliza-lo, primeiramente é necessário a configuração de um banco de dados PostgreSQL, editando os valores de nome do banco, usuário, senha e host em um arquivo .env, no seguinte formato:

```
DBNAME=<<NOME_DO_BANCO>>
USERNAME=<<USUARIO_DE_ACESSO>>
PASSWORD=<<SENHA_DE_ACESSO>>
HOST=<<HOSPEDAGEM_DO_BANCO>>
```

Requisitos
----------

Python3.7+

Execução
--------

Para a instalação das dependências, basta a execução do comando:

```
pip install -r requirements.txt
```

Assim que terminada a instalação das dependências, para a execução do código:

```python
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Os serviços utilizados estão disponíveis na coleção Postman **Django MegaSena.postman_collection.json**, fazendo-se uso do ambiente **django megasena.postman_environment.json**. Caso deseja-se utilizar a interface web disponibilizada pelo Django Framework, necessita-se editar o arquivo *megaSena/urls.py*, descomentando a linha:
 
```python
# path('admin/', admin.site.urls),
```