#!/usr/bin/env python3
"""Regenerate gRPC stubs and fix sibling imports to be package-relative."""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
PROTO_DIR = HERE.parent.parent / "user-service-proto"

subprocess.run([
    sys.executable, "-m", "grpc_tools.protoc",
    f"-I{PROTO_DIR}",
    "--python_out=.",
    "--pyi_out=.",
    "--grpc_python_out=.",
    *PROTO_DIR.glob("*.proto"),
], cwd=HERE, check=True)

pattern = re.compile(r"^import (\w+_pb2)\b", re.MULTILINE)
for path in sorted(HERE.glob("*_pb2*.py*")):
    text = path.read_text()
    fixed = pattern.sub(r"from . import \1", text)
    if fixed != text:
        path.write_text(fixed)
        print(f"Fixed imports in {path.name}")