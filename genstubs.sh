#!/bin/bash
set -e

POINT_RELEASE=1

pip install -U git+https://github.com/chadrik/mypy@stubgenc-all-fixes#mypy

python -m pyside_stubgen -p shiboken2 -p PySide2 -o ./.build

echo -e "\nclass Object:\n    pass" >> ./.build/shiboken2/shiboken2.pyi
echo -e "__version__: str" >> ./.build/PySide2/__init__.pyi
echo -e "__version_info__: tuple[int, int, float, str, str]" >> ./.build/PySide2/__init__.pyi

rm -rf ./PySide2-stubs
mv ./.build/PySide2 ./PySide2-stubs
rm -rf ./shiboken2-stubs
mv ./.build/shiboken2 ./shiboken2-stubs

VERSION=$(python -c "import PySide2;print(PySide2.__version__)")
echo "$VERSION.$POINT_RELEASE" > ./VERSION
