# Chamada Eletronica

Projeto de Engenharia de Software: Proposta de solução para uma versão eletrônica e colaborativa/descentralizada da chamada de presença.

- Experimente: [chamadaeletronica.oseiasromeiro.repl.co](https://chamadaeletronica.oseiasromeiro.repl.co)
- Template: [oseias-romeiro/flask_template](https://github.com/oseias-romeiro/flask_template)

## Descrição

Neste projeto foi criado 5 entidades (user, turma, turmas, chamada, frequencias), nos quais ligam entre si e permite ao usuário-professor criar turmas, adicionar outros usuários-alunos e criar chamada para o dia. O usuário-aluno, pode responder a frequencia, se o professor já ter criado a chamada para o dia, utilizando o qrcode disponível para o professor.

## Ferramentas

Para o projeto foi utilizado:
  - **Flask**
  - **sqlite3**
  - **SQLAlchemy**
  - **Werkzeug**
  - **GeoDB**

### Dados

O projeto está utilizando sqlite, com os seguintes dados de exemplos:

|Matricula|Professor|
|--- |--- |
|100000000|Sim|
|200000000|Sim|
|111111111|Não|
|222222222|Não|

> Todas as senhas são `1234`

### APIs

Foi utilizado a api GeoDB para obter informações de coordenadas coletadas pela api Geolocation no navegador do usuário. Os dados são salvos e utilizados para registrar a posição do professor quando uma chamada é criada e calculo de distância quando um aluno responde a chamada. A diferença é mostrada para o professor, podendo ele rejeitar a presença do aluno.

> É opcional a utilização da API e não é obrigatório autorizar a geolocalização para o aluno responder a chamada.

### Env

Variaveis de ambiente são declarados em `.env`

- **RAPID_KEY** : deve manter a chave rapid para a utilização da api

## Algumas telas

- Tela de Login

<img src="static/media/login.png" height="400px">

- Painel do professor

<img src="static/media/home.png" height="400px">
<br><br>

## Execução 

```sh
  pip install -r requirements.txt
  python3 app.py
```

Acesse: [localhost:5000](http://localhost:5000)
