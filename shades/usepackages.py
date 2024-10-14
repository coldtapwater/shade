# look throught this file to retreive the packages.json file and use that to use the scripts

import json
import os
import sys
from pathlib import Path
import subprocess

packages = json.loads(Path("packages.json").read_text())

def usepackages():
    for package in packages:
        path = Path(package["path"])
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", path])
        script = package["script"]
        inputs = package.get("inputs", {})
        outputs = package.get("outputs", {})
        if "prompt" in inputs:
            prompt = inputs["prompt"].get("default", "")
            subprocess.run([sys.executable, script, prompt])
