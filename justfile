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

release version:
    git branch --show-current | grep -q '^main$' || { \
        echo "must be on main branch"; false; }
    test -z `git diff-index --cached --shortstat origin/main` || { \
        echo "git index must be clean"; false; }
    sed -i '/version =/s/".*"$/"{{ version }}"/' pyproject.toml
    git commit -m "Bump to version {{ version }}" pyproject.toml
    git tag -a v{{ version }} -m "Version {{ version }}"
    #git push --tags +main
