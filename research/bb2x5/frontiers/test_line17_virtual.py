"""Compare fused physical endpoints, pending flags and counts with the packed worker."""
import hashlib
import json
import struct
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from line17 import DATA, load, native_counts, record, replay

TILES = Path(os.environ.get('BB25_TILE17', '/tmp/bb25-tiles17')).resolve()
PACKED = Path(os.environ.get('BB25_PACK17', '/tmp/bb25-packed17')).resolve()
DRIVER = Path(__file__).with_name('line17_virtual.py')


class FusedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.directory.cleanup)
        cls.root = Path(cls.directory.name)
        cls.period = cls.root / 'cut59.code'
        cls.worker('build', '--cut', 59, '--word-bits', 10_000_000)
        cls.meta = json.loads((cls.root/'cut59.code.json').read_text())

    @classmethod
    def worker(cls, mode, *args, check=True):
        return subprocess.run([sys.executable, str(DRIVER), mode, '--engine', str(TILES),
                               '--period', str(cls.period), '--threads', '2', *map(str,args)],
                              check=check, capture_output=True, text=True)

    def packed(self, epochs):
        return subprocess.run([str(PACKED), str(epochs), str(2**28), str(2**34)],
                              input=DATA+'\n', check=True, capture_output=True, text=True).stdout.splitlines()

    def compare(self, copies, digits, batch, prefix, *args):
        epochs = self.meta['origin'] + copies*self.meta['root_period']
        chk = self.root/(prefix+'.json')
        counts = self.root/(prefix+'.counts')
        self.worker('advance', '--epochs', epochs, '--digits', digits, '--phase-batch', batch,
                    '--checkpoint', chk, '--counts', counts, *args)
        header, *rows = counts.read_text().splitlines()
        self.assertEqual(header, f'epochs {epochs}')
        reference = self.packed(epochs)
        self.assertEqual(rows, reference)
        self.assertEqual(load(chk), record(epochs, native_counts(reference, 4*epochs, 424)))
        return chk, counts

    def test_batch_with_pending_seam_and_resume(self):
        origin = replay(self.meta['origin'], 6)
        index = self.root/'seven.index'
        seed, counts = self.compare(5, 7, 3, 'seed', '--index', index)
        self.assertTrue(index.is_file())
        self.assertNotEqual(load(seed)['register'], origin['register'])
        self.compare(17, 7, 4, 'continued', '--seed', seed, '--seed-counts', counts, '--index', index)
        self.compare(17, 5, 1, 'five')
        with index.open('r+b') as stream:
            stream.seek(-1, 2)
            value = stream.read(1)[0]
            stream.seek(-1, 2)
            stream.write(bytes([value ^ 1]))
        bad = self.worker('advance','--epochs',10**18,'--digits',7,'--index',index,
                          '--checkpoint',self.root/'bad-index.json',check=False)
        self.assertNotEqual(bad.returncode,0)
        self.assertIn('index checksum',bad.stderr)

    def test_observed_phases_replay_the_ordered_output(self):
        from checkpoints import checksum
        path = self.root/'observed.json'
        self.compare(31,3,4,'learned','--phase-counts',path)
        saved = json.loads(path.read_text())
        self.assertGreater(len(saved['payload']['rows']),0)
        self.compare(31,3,3,'reused','--phase-counts',path)
        self.assertEqual(json.loads(path.read_text()),saved)
        # Even a rechecksummed incorrect last-cut tally must disagree with the
        # physical bytes entering the remainder of the actual tape.
        for row in saved['payload']['rows']:
            row[-1] += 1
        saved['sha256'] = checksum(saved['payload'])
        path.write_text(json.dumps(saved))
        target = self.meta['origin'] + 2*self.meta['root_period']
        bad = self.worker('advance','--epochs',target,'--digits',3,'--phase-counts',path,
                          '--checkpoint',self.root/'incorrect.json',check=False)
        self.assertNotEqual(bad.returncode,0)
        self.assertIn('emitted physical output',bad.stdout+bad.stderr)

    def test_lifted_period_matches_blank_export(self):
        lifted, direct = self.root/'lifted60.code', self.root/'direct60.code'
        self.worker('lift', '--output', lifted)
        self.worker('build', '--period', direct, '--cut', 60, '--word-bits', 10_000_000)
        metadata = [json.loads(p.with_suffix('.code.json').read_text()) for p in (lifted,direct)]
        for meta in metadata:
            del meta['sha256']
        self.assertEqual(*metadata)
        masks = [w for w in range(65536) if not w & ((w>>1)|(w>>2)|(w>>3))]

        def word_hash(path):
            acc = width = 0
            digest = hashlib.sha256()
            with path.open('rb') as stream:
                while header := stream.read(4):
                    n, = struct.unpack('<I',header)
                    data = bytearray()
                    for code in stream.read((n+15)//16):
                        used = min(n,16)
                        acc |= (masks[code] & ((1<<used)-1)) << width
                        width += used
                        n -= used
                        while width >= 8:
                            data.append(acc & 255)
                            acc >>= 8
                            width -= 8
                    digest.update(data)
            if width:
                digest.update(bytes([acc]))
            return digest.digest()

        self.assertEqual(word_hash(lifted), word_hash(direct))

    def test_physical_periods(self):
        result = subprocess.run([str(TILES),'probe',str(self.period),'59','7','2'],
                                check=True,capture_output=True,text=True)
        orders = [int(line.split()[2]) for line in result.stdout.splitlines() if 'source-copies' in line]
        self.assertEqual(orders[:4], [3, 9, 9, 9])
        self.assertEqual(len(orders), 7)

    def test_checksum_and_truncated_frame(self):
        source = self.period.read_bytes()
        path = self.root/'damaged.code'
        path.write_bytes(source[:-1])
        path.with_suffix('.code.json').write_text(json.dumps(self.meta))
        result = self.worker('advance','--period',path,'--epochs',100,'--checkpoint',self.root/'bad.json',check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('checksum mismatch',result.stderr)
        result = subprocess.run([str(TILES),'probe',str(path),'59','2','1'],capture_output=True,text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('truncated frame',result.stderr.lower())


if __name__ == '__main__':
    unittest.main()
