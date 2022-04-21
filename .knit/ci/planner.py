import json
import os
import shutil

# TODO preview as a separate configured step?

def emit_action_step(name, action, params, plan_fh):
    print(f'_pos={name}', file=plan_fh)
    print('uncacheable=1', file=plan_fh)
    print('process=dynamic', file=plan_fh)
    if not os.path.exists(f'out/files/actions/{action}'):
        shutil.copytree(f'in/actions/{action}', f'out/files/actions/{action}')
    print(f'in/=file:actions/{action}/', file=plan_fh)
    for key, value in params.items():
        print(f'{key}={value}', file=plan_fh)
    print(file=plan_fh)

def emit_step(name, filename, options, plan_fh):
    params = options.get('params', {}).copy()
    for key, value in params.items():
        if value == 'original:':
            shutil.copy(f'in/root/{filename}', f'out/files/original/{name}')
            params[key] = f'file:original/{name}'
        elif value.startswith('file:'):
            _, path = value.split(':', 1)
            shutil.copy(f'in/root/{path}', f'out/files/original/{path}')
            params[key] = f'file:original/{path}'
        elif value.startswith('pre:'):
            _, path = value.split(':', 1)
            dest = f'out/files/pre/{name}/{path}'
            os.makedirs(os.path.dirname(dest))
            shutil.copy(f'in/pre/{name}/{path}', dest)
            params[key] = f'file:pre/{name}/{path}'
    if os.path.exists(f'in/pre/{name}/params'):
        with open(f'in/pre/{name}/params') as fh:
            for line in fh:
                key, value = line.rstrip().split('=', 1)
                params[key] = value
    emit_action_step(name, options['action'], params, plan_fh)

with open('in/root/config.json') as fh:
    config = json.load(fh)

os.mkdir('out/files')
os.mkdir('out/files/original')
with open('out/plan', 'w') as plan_fh:
    for name, step in config['static-steps'].items():
        emit_action_step(name, step['action'], step['params'], plan_fh)
    for filename in os.listdir('in/root'):
        root, ext = os.path.splitext(filename)
        if ext in config['extensions']:
            emit_step(root, filename, config['extensions'][ext], plan_fh)
    # TODO final step (terminal disambiguation)
