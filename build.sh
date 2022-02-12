
# seems to run much faster with -F and built not as one
pyinstaller navi.py \
--name "navi-mac" \
--hidden-import click \
--clean