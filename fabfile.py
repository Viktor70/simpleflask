from fabric import Connection, task
#c = Connection('aws')


@task
def test(c):
    print('Начала отправку на сервер aws')
    with Connection('aws') as c:
        c.run('sudo systemctl restart telbot')