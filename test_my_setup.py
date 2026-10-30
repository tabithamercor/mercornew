#!/usr/bin/env python3
"""Is this computer ready for a sprint?  Run in an empty folder:  python3 test_my_setup.py

Fetches init.py if needed and runs `init.py --test`: a full setup rehearsal on a
dummy task, with no Studio task and no model call. Prints PASS or FAIL.
"""
import os
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

INIT_URL = "https://sdippjgffrptdvlmlurv.supabase.co/storage/v1/object/code-preferences-setup-files-v2/init.py"
ANON_KEY = "sb_publishable_ReTMY8aH1JgV3pPiOnXKAA_ZVcYIimL"


def fetch_init(dest=Path("init.py"), url=INIT_URL):
    if dest.is_file():
        return True
    try:
        req = urllib.request.Request(url, headers={"apikey": ANON_KEY})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except Exception as e:
        print(f"Could not download init.py ({e}). Check your network and try again.", file=sys.stderr)
        return False
    try:
        dest.write_bytes(data)
    except OSError as e:
        print(f"Cannot write init.py in {Path.cwd()} ({e.strerror or e}). Move test_my_setup.py "
              "into an empty folder you own and run it from there.", file=sys.stderr)
        return False
    return True


def writable(folder):
    try:
        with tempfile.TemporaryFile(dir=folder):
            return True
    except OSError:
        return False


def main(argv=None):
    # Windows "Open with" can start Python in read-only C:\Program Files\WindowsApps.
    if not writable(Path.cwd()):
        os.chdir(Path(__file__).resolve().parent)
    if not fetch_init():
        return 1
    return subprocess.run([sys.executable, "init.py", "--test"] + list(argv or [])).returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
