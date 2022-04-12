for f in in/parameters/*; do
    echo "$(basename $f): |"
    sed 's/^/  /' $f
done > parameters.yaml

# Awkwardly share the development shim.
cp in/knitpyter.py .

# TODO use fs store
# VS Code doesn't support cell metadata, so hack it into the first cell.
sed '0,/"metadata": {}/s//"metadata": {"tags": ["parameters"]}/' in/in.ipynb > nb.ipynb
sh in/python.sh -m papermill nb.ipynb out/out.ipynb -f parameters.yaml
