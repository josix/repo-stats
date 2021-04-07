from invoke import task

from tasks.common import MODULES_AS_ARGS


@task(optional=["config_file"])
def flake8(ctx, config_file="setup.cfg"):
    """Check style through flake8"""
    ctx.run(f"flake8 --config={config_file}")


@task
def mypy(ctx):
    """Check style through mypy"""
    ctx.run("mypy")


@task
def black_check(ctx):
    """Check style through black"""
    ctx.run(f"black --check {MODULES_AS_ARGS}")


@task
def isort_check(ctx):
    """Check style through isort"""
    ctx.run(f"isort --atomic --check-only ${MODULES_AS_ARGS}")


@task
def pylint(ctx):
    """Check style through pylint"""
    ctx.run(f"pylint {MODULES_AS_ARGS}")


@task(pre=[mypy, flake8, black_check, isort_check, pylint], default=True)
def lint(ctx):
    """Check style through pylint, isort, black, flake8 and mypy"""
    pass
