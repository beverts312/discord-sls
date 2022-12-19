from invoke import task


def black(c, check, all=False):
    if all:
        c.run(
            f"npx prettier --loglevel=warn {'--check' if check is True else '--write'} ."
        )
    c.run("isort .")
    return c.run(
        f"black tasks.py discord_sls/ --line-length=79 {'--check' if check is True else ''} -v"
    )


@task(aliases=["f"])
def format(c):
    return black(c, False)


@task(aliases=["fa"])
def format_all(c):
    return black(c, False, True)


@task(aliases=["cf", "fc"])
def check_format(c):
    return black(c, True, True)


@task(aliases=["c"])
def clean(c):
    return c.run("rm -rf dist discord_sls.egg-info build")


@task(aliases=["b"])
def build(c):
    return c.run("python3 setup.py bdist_wheel")


@task(aliases=["bp"])
def build_and_publish(c):
    clean(c)
    build(c)
    return c.run("python3 -m twine upload dist/*.whl --verbose")
