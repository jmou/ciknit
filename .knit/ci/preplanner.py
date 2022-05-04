import json
import os
import shutil

with open('in/root/config.json') as fh:
    config = json.load(fh)

os.mkdir('out/files')

steps = []

with open('out/plan', 'w') as plan_fh:
    shutil.copytree('in/modules', 'out/files/modules')

    for name, step in config['presteps'].items():
        print(f'_pos={name}', file=plan_fh)
        print('uncacheable=1', file=plan_fh)
        print('process=dynamic', file=plan_fh)
        print(f'in/=file:modules/{step["module"]}/', file=plan_fh)
        for key, value in step['params'].items():
            if value.startswith('file:'):
                _, path = value.split(':', 1)
                value = f'_pos:originals:out/{path}'
            print(f'{key}={value}', file=plan_fh)
        print(file=plan_fh)

    for filename in os.listdir('in/root'):
        name, ext = os.path.splitext(filename)
        options = config['extensions'].get(ext)
        if options is None:
            continue
        action = options['action']
        steps.append(name)
        print(f'_pos=pre@{name}', file=plan_fh)
        print('process=dynamic', file=plan_fh)
        print(f'in/=file:modules/actions/{action}/', file=plan_fh)
        for key, value in options['params'].items():
            if value == 'original:':
                value = f'_pos:originals:out/{filename}'
            elif value.startswith('file:'):
                _, path = value.split(':', 1)
                value = f'_pos:originals:out/{path}'
            print(f'{key}={value}', file=plan_fh)
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
    for name in steps:
        print(f'in/pre/{name}/=_pos:pre@{name}:out/', file=plan_fh)
    print(file=plan_fh)

    print('_pos=main', file=plan_fh)
    print('_source=fabric:main:unwrap', file=plan_fh)
    print('uncacheable=1', file=plan_fh)
    print('process=dynamic', file=plan_fh)
    print('in/=_pos:plan:out/', file=plan_fh)
    print(file=plan_fh)
