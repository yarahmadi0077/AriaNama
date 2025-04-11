@echo off
pyinstaller --onefile ^
--additional-hooks-dir=. ^
--hidden-import "pandas._libs.tslibs.nattype" ^
--hidden-import "altair.utils.data" ^
--hidden-import "pyarrow" ^
--hidden-import "jinja2" ^
--add-data "data.csv;." ^
main.py
pause