# TODO missing gate means invocation changes when the virtualenv exists or not
# TODO venvcache default param?

import hashlib
import os
import subprocess
import venv

with open('in/venvcache') as fh:
    venvcache = fh.read().strip()
with open('in/requirements.txt', 'rb') as fh:
    requirements = fh.read()

digest = hashlib.sha256(requirements).hexdigest()

env_dir = f'{venvcache}/{digest}'
if not os.path.exists(env_dir):
    venv.create(env_dir, with_pip=True)
    subprocess.check_call([f'{env_dir}/bin/pip', 'install', '-U', 'pip'])
    subprocess.check_call([f'{env_dir}/bin/pip', 'install', '-r', 'in/requirements.txt'])

with open('out/python.sh', 'w') as fh:
    print(f'exec {env_dir}/bin/python "$@"', file=fh)
