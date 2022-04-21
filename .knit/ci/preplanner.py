import json
import os
import shutil

# TODO make all actions two stage?

with open('in/root/config.json') as fh:
    config = json.load(fh)

os.mkdir('out/files')

presteps = []

with open('out/plan', 'w') as plan_fh:
    shutil.copytree('in/actions', 'out/files/actions')
    for filename in os.listdir('in/root'):
        name, ext = os.path.splitext(filename)
        pre = config['extensions'].get(ext, {}).get('pre')
        if pre is not None:
            presteps.append(name)
            print(f'_pos=pre@{name}', file=plan_fh)
            print('process=dynamic', file=plan_fh)
            print(f'in/=file:actions/{pre}/', file=plan_fh)
            print(f'in/param/original=_pos:originals:out/{filename}', file=plan_fh)
            print(file=plan_fh)

    print('_pos=originals', file=plan_fh)
    print('process=identity', file=plan_fh)
    shutil.copytree('in/root/', 'out/files/originals')
    print('in/=file:originals/', file=plan_fh)
    print(file=plan_fh)

    shutil.copy('in/planner.py', 'out/files/planner.py')
    print('_pos=plan', file=plan_fh)
    print('process=command:python3 in/planner.py', file=plan_fh)
    print('in/planner.py=file:planner.py', file=plan_fh)
    print('in/actions/=file:actions/', file=plan_fh)
    print('in/root/=_pos:originals:out/', file=plan_fh)
    for name in presteps:
        print(f'in/pre/{name}/=_pos:pre@{name}:out/', file=plan_fh)
    print(file=plan_fh)

    print('_pos=main', file=plan_fh)
    print('_source=skein:main:unwrap', file=plan_fh)
    print('uncacheable=1', file=plan_fh)
    print('process=dynamic', file=plan_fh)
    print('in/=_pos:plan:out/', file=plan_fh)
    print(file=plan_fh)
