lint: flake8 black-chk pylint mypy

pylint:
  python -mpylint stormlock

mypy:
  mypy .

flake8:
  flake8

black-chk:
  black --check .

fmt:
  black .
