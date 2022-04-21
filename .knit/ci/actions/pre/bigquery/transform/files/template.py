import re

tables = {}

def replace_ref(match):
    return tables.setdefault(match[1], f't{len(tables)}')

lines = []
with open('in/original') as fh:
    for line in fh:
        if line.strip().startswith('--'):
            continue
        lines.append(re.sub(r'@ref\(([^)]*)\)', replace_ref, line))

with open('out/params', 'w') as fh:
    for ref, table in tables.items():
        print(f'in/param/tables/{table}=_pos:{ref}:out/table', file=fh)

with open('out/sql', 'w') as fh:
    fh.writelines(lines)
