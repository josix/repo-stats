from invoke import task

from tasks.common import MODULES_AS_ARGS


@task
def black(ctx):
    """Reformat Python scripts through black"""
    ctx.run(f"black {MODULES_AS_ARGS}")


@task
def isort(ctx):
    """Reformat Python scripts through isort"""
    ctx.run(f"isort --atomic {MODULES_AS_ARGS}")


@task(pre=[isort, black], default=True)
def reformat(ctx):
    """Reformat Python scripts through black and isort"""
    pass
