import os
import sys
import hashlib
import urllib.request
import tarfile
from pathlib import Path

# Suffix to append to the Wheel
# For pre release versions this should be 'aN', e.g. 'a1'
# For release versions this should be ''
# See https://peps.python.org/pep-0427/#file-name-convention for details.
BUILD_SUFFIX = 'a3'

# Main binary for node
# Path of binary inn downloaded distribution to match
NODE_BINS = ('bin/node', 'node.exe')

# Mapping of node platforms to Python platforms
PLATFORMS = {
#     'win-x86':      'win32',
#     'win-x64':      'win_amd64',
#     'darwin-x64':   'macosx_10_9_x86_64',
     'darwin-arm64': 'macosx_11_0_arm64',
#    'linux-x64':    'manylinux_2_12_x86_64.manylinux2010_x86_64',
#     'linux-armv7l': 'manylinux_2_17_armv7l.manylinux2014_armv7l',
#     'linux-arm64':  'manylinux_2_17_aarch64.manylinux2014_aarch64',
#     'linux-x64-musl': 'musllinux_1_1_x86_64'
}

HYPYR_ROOT = Path.home() / ".cache" / f"hypyrpyram"

def main():
    print("Hello from hypyrpyram!")

    # Get root path to use
    root_path = ""

    # Check for node/npx, if not, install it
    if os.system('npx -v') != 0:
        # Check cache
        for file in (HYPYR_ROOT.glob("node-v*")):
            if file.is_dir() and (file / "bin" / "node").exists():
                root_path = file / "bin"
        if not root_path:
            root_path = install_node()

    # Run npx hyperparam, with passed args
    args = sys.argv[1:]
    if root_path:
        os.environ["PATH"] += ":" + str(root_path)
        print("PATH", os.environ["PATH"])
    os.system(f'npx --yes hyperparam {" ".join(args)}')



def install_node(node_version: str = '22.3.0') -> str:
    print('--')
    print('Making Node.js Wheels for version', node_version)

    for node_platform, python_platform in PLATFORMS.items():
        filetype = 'zip' if node_platform.startswith('win-') else 'tar.gz'
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

        compressed_file = HYPYR_ROOT / f"node-v{node_version}-{node_platform}.{filetype}"
        compressed_file.parent.mkdir(exist_ok=True, parents=True)
        # Write the .tar.xz
        with open(compressed_file, "wb") as f:
            f.write(node_archive)

        # Read the .tar.xz file in uncompressed form
        print("Saving to", compressed_file.parent)
        with tarfile.open(compressed_file) as tar:
            tar.extractall(compressed_file.parent)
        tar.close()

        node_path = compressed_file.parent / f"node-v{node_version}-{node_platform}" / "bin"
        return node_path

if __name__ == '__main__':
    main()
