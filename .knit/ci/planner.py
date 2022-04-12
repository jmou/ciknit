import os
import shutil
import subprocess

# Consider translating directory at a time. Can simplify "global" dependencies.

def build_actions():
    actions = {}
    with open('in/root/.actions') as fh:
        for line in fh:
            line = line.strip()
            if line.startswith('#'):
                continue
            ext, command = line.split(None, 1)
            if not ext.startswith('.'):
                # TODO better experience to emit a failing step?
                raise Exception('extension should start with .')
            actions[ext] = command
    return actions

def emit_step(name, filename, action, plan_fh):
    print(f'_pos={name}', file=plan_fh)
    print('uncacheable=1', file=plan_fh)
    print('process=dynamic', file=plan_fh)
    if not os.path.exists(f'out/files/actions/{action}'):
        shutil.copytree(f'in/actions/{action}', f'out/files/actions/{action}')
    print(f'in/=file:actions/{action}/', file=plan_fh)
    # TODO translation seems to make more sense as a separate step
    translator = f'in/actions/{action}/translate'
    mode = os.stat(translator).st_mode | 0o111
    os.chmod(translator, mode)
    lines = subprocess.check_output([translator, f'in/root/{filename}'],
                                    universal_newlines=True).splitlines()
    index = 0
    for index, line in enumerate(lines):
        if not line:
            break
        print(line, file=plan_fh)
    if index + 1 < len(lines):
        param = lines[index + 1]
        with open(f'out/files/{name}', 'w') as translated_fh:
            for line in lines[index + 2:]:
                print(line, file=translated_fh)
        print(f'in/param/{param}=file:{name}', file=plan_fh)
    print(file=plan_fh)

actions = build_actions()
os.mkdir('out/files')
with open('out/plan', 'w') as plan_fh:
    for filename in os.listdir('in/root'):
        root, ext = os.path.splitext(filename)
        if ext in actions:
            emit_step(root, filename, actions[ext], plan_fh)
    # TODO final step (terminal disambiguation)
