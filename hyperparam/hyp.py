import os
import platform
import sys
import hashlib
import urllib.request
import tarfile
from pathlib import Path

NODE_VERSION = '22.3.0'

# Main binary for node
# Path of binary in downloaded distribution to match
NODE_BINS = ('bin/node', 'node.exe')

HYPYR_CACHE = Path.home() / ".cache" / f"hypyrpyram"

ARCH = platform.system().lower() + "-" + os.uname().machine

def main():
    print("Hello from hyperparam!")

    # Get root path to use
    root_path = ""

    # Check for node/npx, if not, install it
    # TODO: use popen instead of system
    if os.system('npx -v') != 0:
        # Check cache
        file = HYPYR_CACHE / f"node-v{NODE_VERSION}-{ARCH}"
        if file.is_dir() and (file / "bin" / "node").exists():
            root_path = file / "bin"
        if not root_path:
            root_path = install_node(NODE_VERSION)

    # Run npx hyperparam, with passed args
    args = sys.argv[1:]
    if root_path:
        os.environ["PATH"] += ":" + str(root_path)
        print("PATH", os.environ["PATH"])
    os.system(f'npx --yes hyperparam {" ".join(args)}')


def install_node(node_version: str) -> str:
    print('--')
    print('Making Node.js Wheels for version', node_version)

    filetype = 'zip' if ARCH.startswith('win-') else 'tar.gz'
    node_url = f'https://nodejs.org/dist/v{node_version}/node-v{node_version}-{ARCH}.{filetype}'

    print(f'- Making Wheel for {ARCH} from {node_url}')
    try:
        with urllib.request.urlopen(node_url) as request:
            node_archive = request.read()
            print(f'  {node_url}')
            print(f'    {hashlib.sha256(node_archive).hexdigest()}')
    except urllib.error.HTTPError as e:
        print(f'  {e.code} {e.reason}')
        print(f'  Skipping {ARCH}')
        return

    compressed_file = HYPYR_CACHE / f"node-v{node_version}-{ARCH}.{filetype}"
    compressed_file.parent.mkdir(exist_ok=True, parents=True)
    # Write the .tar.xz
    with open(compressed_file, "wb") as f:
        f.write(node_archive)

    # Read the .tar.xz file in uncompressed form
    print("Saving to", compressed_file.parent)
    with tarfile.open(compressed_file) as tar:
        tar.extractall(compressed_file.parent)
    tar.close()

    node_path = compressed_file.parent / f"node-v{node_version}-{ARCH}" / "bin"
    return node_path

if __name__ == '__main__':
    main()
