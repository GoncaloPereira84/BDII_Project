# Dependencies
```bash
pip install django
```
```bash
pip install psycopg2
```
# Setup Project

1. Dar clone do repositório
2. entrar dentro do mesmo
3. executar o seguinte comando para criar (venv)

```bash
python -m venv env;
```
4. Entrar na venv
```bash
env/scripts/activate
```
5. Por último dar start ao projeto

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```