import toml

parsed_toml = toml.load("Pipfile")
modules = parsed_toml["modules"]
MODULES_AS_ARGS = " ".join(modules)
