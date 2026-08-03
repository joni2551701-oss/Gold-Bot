"""Unit tests for data_layer/market_memory/persistence/memory_codec.py (module 6)."""

import pytest

from data_layer.market_memory.persistence.memory_codec import MemoryCodec, SCHEMA_VERSION
from _pfakes import memory_with, ts


def test_serialize_roundtrip():
    mem = memory_with(m1=5)
    codec = MemoryCodec(compress=True)
    data, meta = codec.serialize(mem, ts(10), bootstrap_version="b1")
    assert meta.candle_count == 5
    assert meta.timeframe_count == 1
    assert meta.schema_version == SCHEMA_VERSION
    assert meta.bootstrap_version == "b1"
    meta2, timeframes = codec.deserialize(data)
    assert meta2.integrity_hash == meta.integrity_hash
    assert len(timeframes["M1"]) == 5
    assert codec.verify_hash(meta2, timeframes)


def test_uncompressed_roundtrip():
    mem = memory_with(m1=3)
    codec = MemoryCodec(compress=False)
    data, meta = codec.serialize(mem, ts(1))
    meta2, tf = codec.deserialize(data)
    assert len(tf["M1"]) == 3


def test_rejects_unknown_schema_version():
    mem = memory_with(m1=1)
    codec = MemoryCodec(compress=False)
    data, _ = codec.serialize(mem, ts(1))
    tampered = data.replace(b'"schema_version":1', b'"schema_version":99')
    with pytest.raises(ValueError):
        codec.deserialize(tampered)


def test_hash_detects_tampering():
    mem = memory_with(m1=4)
    codec = MemoryCodec(compress=False)
    _, meta = codec.serialize(mem, ts(1))
    # a different memory -> different hash
    _, meta2 = codec.serialize(memory_with(m1=3), ts(1))
    assert meta.integrity_hash != meta2.integrity_hash
