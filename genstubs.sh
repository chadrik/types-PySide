#!/bin/bash
set -e
# pip install PySide2
# pip install -e ../mypy
# python -c "import PySide2.QtWidgets as qtw;print(type(qtw.QAbstractButton.pressed).__mro__)"

# shiboken generator:
#python -m PySide2.support.generate_pyi all --outpath stubs/generate_pyi/PySide2

# standard stubgen
#python -c "import mypy.stubgen;print(mypy.stubgen.__file__)"
#python -m mypy.stubgen -p PySide2.QtCore -p PySide2.QtWidgets -o stubs/stubgen/

# custom:
python -m pyside_stubgen -p shiboken2 -p PySide2 -o stubs/

echo -e "\nclass Object:\n    pass" >> stubs/shiboken2/shiboken2.pyi

function fixqtstub() {
    BASE_NAME=$(basename "$1" ".pyi")
    if [[ $BASE_NAME != "QtCompat" ]]; then
        echo "from PySide2.${BASE_NAME} import *" > $1
    fi
}
export -f fixqtstub
find ../pipe/qt/python/luma_qt/Qt -name "Qt[A-Z]*.pyi" -exec bash -c "fixqtstub \"{}\"" \;

cp -R stubs/PySide2 ../pipe/qt/python/
cp -R stubs/shiboken2 ../pipe/qt/python/
