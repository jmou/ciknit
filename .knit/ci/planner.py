import os
import shutil

# TODO preview as a separate configured step?

os.mkdir('out/files')
os.mkdir('out/files/pre')
with open('out/plan', 'w') as plan_fh:
    for name in os.listdir('in/pre'):
        if os.path.exists(f'in/pre/{name}/module/plan'):
            print(f'_pos={name}', file=plan_fh)
            print('uncacheable=1', file=plan_fh)
            print('process=dynamic', file=plan_fh)
            shutil.copytree(f'in/pre/{name}', f'out/files/pre/{name}')
            print(f'in/=file:pre/{name}/module/', file=plan_fh)
            if os.path.exists(f'in/pre/{name}/params'):
                with open(f'in/pre/{name}/params') as fh:
                    for line in fh:
                        print(line.rstrip(), file=plan_fh)
            print(file=plan_fh)
    # TODO final step (terminal disambiguation)
