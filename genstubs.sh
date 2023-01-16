#!/bin/bash
set -e

POINT_RELEASE=0

# pip install -U git+https://github.com/chadrik/mypy@stubgenc-improvements1#mypy

python -m pyside_stubgen -p shiboken2 -p PySide2 -o ./.build

echo -e "\nclass Object:\n    pass" >> ./.build/shiboken2/shiboken2.pyi

rm -rf ./PySide2-stubs
mv ./.build/PySide2 ./PySide2-stubs
rm -rf ./shiboken2-stubs
mv ./.build/shiboken2 ./shiboken2-stubs

VERSION=$(python -c "import PySide2;print(PySide2.__version__)")
echo "$VERSION.$POINT_RELEASE" > ./VERSION
