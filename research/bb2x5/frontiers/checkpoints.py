"""Shared checkpoint integrity and atomic file replacement."""
import hashlib
import json
import os
from pathlib import Path
import tempfile


def atomic_json(path, data):
    path = Path(path)
    with tempfile.NamedTemporaryFile('w', dir=path.parent, delete=False) as out:
        name = out.name
        try:
            json.dump(data, out, indent=2)
            out.write('\n')
            out.flush()
            os.fsync(out.fileno())
        except BaseException:
            os.unlink(name)
            raise
    try:
        os.replace(name, path)
    except BaseException:
        os.unlink(name)
        raise


def checksum(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


ROOT = Path(__file__).resolve().parents[1]
DATA_SHA256 = '89ea92fd4643166b92fca4ae80e37a699ab8615ac1dd375dae777e6b3e45ecc6'


def holdouts():
    data=(ROOT/'BB2x5_Rocq_holdouts_37.txt').read_bytes()
    if hashlib.sha256(data).hexdigest()!=DATA_SHA256:
        raise ValueError('holdout dataset identity mismatch')
    return data.decode().splitlines()
