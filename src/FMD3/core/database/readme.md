# Install tool (while in venv):

```shell
pip install alembic
```
## Create migration instructions:
```shell
    alembic revision --autogenerate -m "Message"
```
For example Message could be: `alembic revision --autogenerate -m "Add fav table"`




## To apply migrations on client
```shell
    alembic upgrade head
```