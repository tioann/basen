import math
import random

class BaseN:
    """
    A class to represent a base-N encoding/decoding system.
    """

    def __init__(self, charset: str, src_len: int|None=None, dst_len: int|None=None, max_dst_len: int=120):
        """
        Constructs all the necessary attributes for the BaseN object.

        Parameters:
        -----------
        charset : str
            The set of characters used for encoding.
        src_len : int, optional
            The length of the source string to be encoded (default is None for automcatically calculating an optimal value).
        dst_len : int, optional
            The length of the destination encoded string (default is None).
        max_dst_len : int, optional
            The maximum length of the destination encoded string (default is 120). Used to limit the search of optimal source length.
        """
        self.charset = charset
        self.base = len(charset)
        self.char_to_idx = {c: i for i, c in enumerate(self.charset)}
        self.max_dst_len = max_dst_len
        self.exp_factor = 8 / math.log2(self.base)  # src to dst size expansion factor
        if src_len is not None:
            self.src_len = src_len
            if dst_len is not None:
                self.dst_len = dst_len
            else:
                self.dst_len = math.ceil(src_len * self.exp_factor)
        else:
            self.dst_len = self.calc_rate()
            self.src_len = int(self.dst_len / self.exp_factor)
        self.check()

    def check(self):
        """
        Validates the charset to ensure all characters are unique.
        """
        t = set()
        for c in self.charset:
            if c in t:
                raise ValueError(f"Duplicate character found in charset: {c}")
            t.add(c)

    def calc_rate(self):
        """
        Calculates the optimal destination length for encoding.

        Returns:
        --------
        int
            The optimal destination length.
        """
        best = None
        best_rate = None
        for dst_len in range(self.max_dst_len):
            src_len = int(dst_len / self.exp_factor)
            if src_len == 0:
                continue
            exp_rate = dst_len / src_len
            if best_rate is None or best_rate > exp_rate:
                best_rate = exp_rate
                best = dst_len
        return best

    def encode(self, bdata: bytes) -> str:
        """
        Encodes the given bytes data to a base-N string.

        Parameters:
        -----------
        bdata : bytes
            The data to be encoded.

        Returns:
        --------
        str
            The encoded base-N string.
        """
        res = []
        idx = 0
        while idx < len(bdata):
            # Determine the length of the source segment to encode
            src_len = len(bdata) - idx if len(bdata) - idx < self.src_len else self.src_len
            # Convert the source segment to an integer
            num = int.from_bytes(bdata[idx:idx + src_len], 'big')
            # Encode the integer to a base-N string
            enc = []
            while num > 0:
                num, rem = divmod(num, self.base)
                enc.append(self.charset[rem])
            # Add padding if necessary
            # while len(enc) < self.dst_len:
            #     enc.append(self.charset[0])
            res.extend(reversed(enc))
            idx += src_len
        return ''.join(res)

    def decode(self, s: str) -> bytes:
        """
        Decodes the given base-N string to bytes data.

        Parameters:
        -----------
        s : str
            The base-N string to be decoded.

        Returns:
        --------
        bytes
            The decoded bytes data.
        """
        res = bytearray()
        idx = 0
        while idx < len(s):
            # Determine the length of the destination segment to decode
            dst_len = len(s) - idx if len(s) - idx < self.dst_len else self.dst_len
            # Convert the base-N string segment to an integer
            num = 0
            for c in s[idx:idx + dst_len]:
                num = num * self.base + self.char_to_idx[c]
            # Convert the integer to bytes
            res.extend(num.to_bytes((num.bit_length() + 7) // 8, 'big'))
            idx += dst_len
        return bytes(res)

Base16 = BaseN(charset="0123456789ABCDEF", src_len=1, dst_len=2)
Base32 = BaseN(charset="ABCDEFGHIJKLMNOPQRSTUVWXYZ234567", src_len=5, dst_len=8)
Base32Hex = BaseN(charset="0123456789ABCDEFGHIJKLMNOPQRSTUV", src_len=5, dst_len=8)
Base64 = BaseN(charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", src_len=3, dst_len=4)
Base64Url = BaseN(charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_", src_len=3, dst_len=4)
# Base58 as specified for bitcoin does not do segmentation so no fixed src length to work with
Base58Charset = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
JsonBase93 = BaseN(charset="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~`!@#$%^&*()_+-={}|[]:;'<>?,./ ")
