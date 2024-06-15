import os
import hashlib
import urllib.request
from pathlib import Path

def main(args):
    print("Hello from hypyrpyram!")

    # Check for node/npx, if not, install it
    if os.system('npm -v') != 0:
        install_node()

    # Run npx hyperparam, with passed args
    os.system(f'npx hyperparam {" ".join(args)}')



# Versions to build if run as a script:
BUILD_VERSIONS = ('14.19.3', '16.15.1', '18.4.0')

# Suffix to append to the Wheel
# For pre release versions this should be 'aN', e.g. 'a1'
# For release versions this should be ''
# See https://peps.python.org/pep-0427/#file-name-convention for details.
BUILD_SUFFIX = 'a3'

# Main binary for node
# Path of binary inn downloaded distribution to match
NODE_BINS = ('bin/node', 'node.exe')

# Other binaries
# key: path of binary inn downloaded distribution to match
# value: tuple of (
#   <name>,
#   <True = is a link to script to run with node, False = is executable>
# )
NODE_OTHER_BINS = {
    'bin/npm': ('npm', True),
    'npm.cmd': ('npm', False),
    'bin/npx': ('npx', True),
    'npx.cmd': ('npx', False),
    'bin/corepack': ('corepack', True),     
    'corepack.cmd': ('corepack', False),
}

# Mapping of node platforms to Python platforms
PLATFORMS = {
    'win-x86':      'win32',
    'win-x64':      'win_amd64',
    'darwin-x64':   'macosx_10_9_x86_64',
    'darwin-arm64': 'macosx_11_0_arm64',
    'linux-x64':    'manylinux_2_12_x86_64.manylinux2010_x86_64',
    'linux-armv7l': 'manylinux_2_17_armv7l.manylinux2014_armv7l',
    'linux-arm64':  'manylinux_2_17_aarch64.manylinux2014_aarch64',
    'linux-x64-musl': 'musllinux_1_1_x86_64'
}

# https://github.com/nodejs/unofficial-builds/
# Versions added here should match the keys above
UNOFFICIAL_NODEJS_BUILDS = {'linux-x64-musl'}


def install_node(node_version: str, suffix: str = ''):
    print('--')
    print('Making Node.js Wheels for version', node_version)
    if suffix:
        print('Suffix:', suffix)

    for node_platform, python_platform in PLATFORMS.items():
        filetype = 'zip' if node_platform.startswith('win-') else 'tar.xz'
        if node_platform in UNOFFICIAL_NODEJS_BUILDS:
            node_url = f'https://unofficial-builds.nodejs.org/download/release/v{node_version}/node-v{node_version}-{node_platform}.{filetype}'
        else:
            node_url = f'https://nodejs.org/dist/v{node_version}/node-v{node_version}-{node_platform}.{filetype}'

        print(f'- Making Wheel for {node_platform} from {node_url}')
        try:
            with urllib.request.urlopen(node_url) as request:
                node_archive = request.read()
                print(f'  {node_url}')
                print(f'    {hashlib.sha256(node_archive).hexdigest()}')
        except urllib.error.HTTPError as e:
            print(f'  {e.code} {e.reason}')
            print(f'  Skipping {node_platform}')
            continue

        wheelpath = Path.home() / ".ssh" / f"hypyrpyram" / f"{node_platform}_{python_platform}"
        wheelpath.parent.mkdir(exist_ok=True, parents=True)
        with open(wheelpath, "wb") as f:
            f.write(node_archive)