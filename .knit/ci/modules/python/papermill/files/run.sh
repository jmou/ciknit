# TODO use fs store
# VS Code doesn't support cell metadata, so hack it into the first cell.
sed '0,/"metadata": {}/s//"metadata": {"tags": ["parameters"]}/' in/in.ipynb > nb.ipynb
cd in/root
exec sh ../python.sh -m papermill ../../nb.ipynb ../../out/out.ipynb -p knit_active True
