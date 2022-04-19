import json
import os
import shutil
import subprocess

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
    # TODO translation seems to make more sense as a separate step
    translator = options.get('translator')
    if translator is not None:
        mode = os.stat(translator).st_mode | 0o111
        os.chmod(translator, mode)
        lines = subprocess.check_output([translator, f'in/root/{filename}'],
                                        universal_newlines=True).splitlines()
        index = 0
        for index, line in enumerate(lines):
            if not line:
                break
            key, value = line.split('=', 1)
            params[key] = value
        if index + 1 < len(lines):
            with open(f'out/files/translated/{name}', 'w') as translated_fh:
                for line in lines[index + 1:]:
                    print(line, file=translated_fh)
    for key, value in params.items():
        if value == 'original:':
            shutil.copy(f'in/root/{filename}', f'out/files/original/{name}')
            params[key] = f'file:original/{name}'
        elif value == 'translated:':
            if translator is None:
                # TODO better experience to emit a failing step?
                raise Exception('missing translated param')
            params[key] = f'file:translated/{name}'
        elif value.startswith('file:'):
            _, path = value.split(':', 1)
            shutil.copy(f'in/root/{path}', f'out/files/original/{path}')
            params[key] = f'file:original/{path}'
    emit_action_step(name, options['action'], params, plan_fh)

with open('in/root/config.json') as fh:
    config = json.load(fh)

os.mkdir('out/files')
os.mkdir('out/files/translated')
os.mkdir('out/files/original')
with open('out/plan', 'w') as plan_fh:
    for name, step in config['static-steps'].items():
        emit_action_step(name, step['action'], step['params'], plan_fh)
    for filename in os.listdir('in/root'):
        root, ext = os.path.splitext(filename)
        if ext in config['extensions']:
            emit_step(root, filename, config['extensions'][ext], plan_fh)
    # TODO final step (terminal disambiguation)
