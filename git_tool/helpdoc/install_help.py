#!/usr/bin/env python3

import os
import platform
import shutil
import sys
from pathlib import Path



'''
    I could not find a reliable way to install the helpdoc during package installation.
    So, the user has to copy the helpdoc in the respective location manually.
    This script is added as an executable script to the pyproject.toml file.
    The user can run this script via "feature-install-help".
'''



def install_man_page():
    man_page = Path("git_tool/helpdoc/git-feature.1")
    if not man_page.exists():
        print("Man page not found.")
        sys.exit(1)

    if platform.system() == "Linux":
        target_dir = Path("/usr/share/man/man1")
    elif platform.system() == "Darwin":  # macOS
        target_dir = Path("/usr/local/share/man/man1")
    else:
        print("Manual pages not supported on this OS.")
        sys.exit(0)

    try:
        print(f"Copying {man_page} to {target_dir}")
        shutil.copy(man_page, target_dir)
    except PermissionError:
        print("Permission denied. Try running with sudo.")
        sys.exit(1)



def install_html_doc():
    SCRIPT_DIR = Path(__file__).resolve().parent
    html_doc = SCRIPT_DIR / "git-feature.html"
    if not html_doc.exists():
        print("HTML doc not found.")
        sys.exit(1)

    target_dir = Path("C:/Program Files/Git/mingw64/share/doc/git-doc")

    if not target_dir.exists():
        print(f"Target doc directory not found: {target_dir}")
        sys.exit(1)

    try:
        print(f"Copying {html_doc} to {target_dir}")
        shutil.copy(html_doc, target_dir)
    except PermissionError:
        print("Permission denied. Run this script as Administrator.")
        sys.exit(1)



def main():
    os_type = platform.system()

    if os_type in ["Linux", "Darwin"]:
        install_man_page()
    elif os_type == "Windows":
        install_html_doc()
    else:
        print(f"Unsupported OS: {os_type}")
        sys.exit(1)



if __name__ == "__main__":
    main()
