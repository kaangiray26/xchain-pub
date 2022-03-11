#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import secrets


class XLib:
    def encrypt(path, shares):
        """
        Read file content and create xor chain
        """
        data = b""
        keys = []

        basename = os.path.basename(path).zfill(256).encode()
        data += basename

        with open(path, "rb") as f:
            data += f.read()

        keys.append(secrets.token_bytes(len(data)))
        keys.append(bytes([keys[-1][i] ^ data[i] for i in range(len(data))]))

        while len(keys) != shares:
            k = keys[-1]
            del keys[-1]
            keys.append(secrets.token_bytes(len(data)))
            keys.append(bytes([keys[-1][i] ^ k[i] for i in range(len(k))]))

        index = 0
        token = secrets.token_hex(24)

        for key in keys:
            with open(f"encrypted/{token}_{index}.xc", "wb") as xc:
                xc.write(key)
            index += 1
        return token

    def decrypt(paths):
        """
        Xor keys as a block to reveal the original file
        """
        data = b""
        keys = []

        for path in paths:
            with open(path, "rb") as f:
                keys.append(f.read())

        data = keys[-1]
        del keys[-1]
        keys.reverse()

        for k in keys:
            data = bytes([data[i] ^ k[i] for i in range(len(k))])
        basename = data[:256].lstrip(b'0').decode()
        with open(f"decrypted/{basename}", "wb") as f:
            f.write(data[256:])

        return basename
