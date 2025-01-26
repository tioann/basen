import basen


def test_base_n(test_strings, base, name):
    for input_str, expected_enc in test_strings.items():
        encoded = base.encode(input_str.encode())
        decoded = base.decode(encoded).decode()
        print(f"{name}: {encoded} -> {decoded}")
        assert decoded == input_str
        assert encoded == expected_enc


def example_Base93Json():
    b = basen.JsonBase93
    test_strings = {
        "Hello, World!": r"H3Q%Zi8j;I^8L%fA",
    }
    print(f"JsonBase93 src_len={b.src_len}, dst_len={b.dst_len}, exp_factor={b.exp_factor}")
    test_base_n(test_strings, b, "JsonBase93")


def example_base64():
    b = basen.Base64
    test_strings = {
        "": "",
        "foo": "Zm9v",
        "foobar": "Zm9vYmFy",
    }
    test_base_n(test_strings, b, "Base64")


def example_base16():
    b = basen.Base16
    test_strings = {
        "": "",
        "f": "66",
        "fo": "666F",
        "foo": "666F6F",
        "foob": "666F6F62",
        "fooba": "666F6F6261",
        "foobar": "666F6F626172",
    }
    test_base_n(test_strings, b, "Base16")


def example_base32():
    b = basen.Base32
    test_strings = {
        "": "",
        "fooba": "MZXW6YTB",
    }
    test_base_n(test_strings, b, "Base32")


def example_base32hex():
    b = basen.Base32Hex
    test_strings = {
        "": "",
        "fooba": "CPNMUOJ1",
    }
    test_base_n(test_strings, b, "Base32Hex")


def example_base58():
    test_strings = {
        "1234598760": "3mJr7AoUXx2Wqd",
        "abcdefghijklmnopqrstuvwxyz": "3yxU3u1igY8WkgtjK92fbJQCd4BZiiT1v25f",
        "00000000000000000000000000000000000000000000000000000000000000": "3sN2THZeE9Eh9eYrwkvZqNstbHGvrxSAM7gXUXvyFQP8XvQLUqNCS27icwUeDT7ckHm4FUHM2mTVh1vbLmk7y"
    }

    for input_str, expected_enc in test_strings.items():
        base58 = basen.BaseN(charset=basen.Base58Charset, src_len=len(input_str))
        encoded = base58.encode(input_str.encode())
        decoded = base58.decode(encoded).decode()
        print(f"Base58: {encoded} -> {decoded}")
        assert decoded == input_str
        assert encoded == expected_enc


example_Base93Json()
example_base64()
example_base16()
example_base32()
example_base32hex()
example_base58()
