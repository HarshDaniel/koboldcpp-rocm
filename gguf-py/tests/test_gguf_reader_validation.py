import struct
import numpy as np
import pytest

from gguf.gguf_reader import GGUFReader


def _write_gguf(path, n_dims_field, dims):
    buf = b'GGUF' + struct.pack('<IQQ', 3, 1, 0)
    name = b'bad_tensor'
    buf += struct.pack('<Q', len(name)) + name
    buf += struct.pack('<I', n_dims_field)
    for dim in dims:
        buf += struct.pack('<Q', dim)
    buf += struct.pack('<I', 0)
    buf += struct.pack('<Q', 0)
    buf += b'\x00' * 64
    path.write_bytes(buf)


def test_n_dims_upper_bound(tmp_path):
    test_file = tmp_path / 'evil_ndims.gguf'
    _write_gguf(test_file, 1_000_000, [1] * 8)
    with pytest.raises(ValueError, match='exceeds GGML_MAX_DIMS'):
        GGUFReader(test_file)


def test_dims_product_no_uint64_wraparound(tmp_path):
    dims = [4194305, 4194305, 211106198978564]
    assert int(np.prod(np.array(dims, dtype=np.uint64))) == 4
    test_file = tmp_path / 'evil_overflow.gguf'
    _write_gguf(test_file, len(dims), dims)
    with pytest.raises(ValueError):
        GGUFReader(test_file)
