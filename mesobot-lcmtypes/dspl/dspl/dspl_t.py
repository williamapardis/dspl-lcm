"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class dspl_t(object):
    __slots__ = ["utime", "lightNumber", "temperature", "humidity", "channelMode", "lightLevel", "secsSinceComs", "nackCount"]

    __typenames__ = ["int64_t", "int32_t", "double", "double", "int32_t", "int32_t", "double", "double"]

    __dimensions__ = [None, None, None, None, None, None, None, None]

    def __init__(self):
        self.utime = 0
        self.lightNumber = 0
        self.temperature = 0.0
        self.humidity = 0.0
        self.channelMode = 0
        self.lightLevel = 0
        self.secsSinceComs = 0.0
        self.nackCount = 0.0

    def encode(self):
        buf = BytesIO()
        buf.write(dspl_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">qiddiidd", self.utime, self.lightNumber, self.temperature, self.humidity, self.channelMode, self.lightLevel, self.secsSinceComs, self.nackCount))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != dspl_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return dspl_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = dspl_t()
        self.utime, self.lightNumber, self.temperature, self.humidity, self.channelMode, self.lightLevel, self.secsSinceComs, self.nackCount = struct.unpack(">qiddiidd", buf.read(52))
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if dspl_t in parents: return 0
        tmphash = (0xeb8194e0394cd2e1) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if dspl_t._packed_fingerprint is None:
            dspl_t._packed_fingerprint = struct.pack(">Q", dspl_t._get_hash_recursive([]))
        return dspl_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", dspl_t._get_packed_fingerprint())[0]
