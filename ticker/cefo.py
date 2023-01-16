import io


class FullGlyphBlock:
    size: int = 12

    prefix: int
    offset: int
    widths: list[int]

    def __init__(self, data: bytes) -> None:
        offpfx = int.from_bytes(data[0:4], "little")
        widths = int.from_bytes(data[4:12], "little")

        self.prefix = offpfx & 0xFFF
        self.offset = offpfx >> 12
        self.widths = [(widths >> (i * 4)) & 0xF for i in range(16)]

    def __str__(self) -> str:
        return "<glyphs {0:03X}0-{0:03X}F at {1:05X}>".format(self.prefix, self.offset)


class SparseGlyphBlock:
    size: int = 6

    prefix: int
    offset: int
    widths: list[tuple[int, int]]

    def __init__(self, data: bytes, sgly: bytes) -> None:
        lenpfx = int.from_bytes(data[0:2], "little")
        offset = int.from_bytes(data[2:4], "little")
        sgly_offset = int.from_bytes(data[4:6], "little")
        sgly_data = sgly[sgly_offset:(sgly_offset + (lenpfx >> 12))]

        self.prefix = lenpfx & 0xFFF
        self.offset = offset
        self.widths = [(byte >> 4, byte & 0xF) for byte in sgly_data]

    def __str__(self) -> str:
        return "<glyphs {} at {:05X}>".format(", ".join("{:03X}{:X}".format(self.prefix, i[0]) for i in self.widths), self.offset)


class CelonesFont:
    bitmap: bytes

    _full_blocks: list[FullGlyphBlock]
    _sparse_blocks: list[SparseGlyphBlock]

    def __init__(self, filename: str) -> None:
        with io.open(filename, mode="rb") as cefo:
            # Verify the basic header structure
            fourcc = cefo.read(4)
            if fourcc != b"RIFF":
                raise ValueError("File is not RIFF")

            size = int.from_bytes(cefo.read(4), "little")
            fourcc = cefo.read(4)
            if fourcc != b"CeFo":
                raise ValueError("File is not a Celones Font")

            # Load applicable RIFF chunks
            fblk, sblk, sgly, bmp = b"", b"", b"", b""
            while size > 0:
                fourcc = cefo.read(4)
                chunk_size = int.from_bytes(cefo.read(4), "little")
                data = cefo.read(chunk_size)

                if fourcc == b"fblk":
                    fblk = data
                elif fourcc == b"sblk":
                    sblk = data
                elif fourcc == b"sgly":
                    sgly = data
                elif fourcc == b"bmp ":
                    bmp = data

                size -= 8 + chunk_size

            # Populate full glyph block list
            count = round(len(fblk) / FullGlyphBlock.size)
            self._full_blocks = [FullGlyphBlock(
                fblk[i * FullGlyphBlock.size:]) for i in range(count)]

            # Populate sparse glyph block list
            count = round(len(sblk) / SparseGlyphBlock.size)
            self._sparse_blocks = [SparseGlyphBlock(
                sblk[i * SparseGlyphBlock.size:], sgly) for i in range(count)]

            # Set the glyph bitmap
            self.bitmap = bmp

    def __getitem__(self, index: int) -> bytes:
        try:
            block = next(
                b for b in self._full_blocks if b.prefix == index >> 4)
            start = block.offset + sum(block.widths[:index & 0xF])
            stop = start + block.widths[index & 0xF]
            return self.bitmap[start:stop]

        except StopIteration:
            pass

        try:
            block = next(
                b for b in self._sparse_blocks if b.prefix == index >> 4)
            start = block.offset
            for i, width in block.widths:
                if i == index & 0xF:
                    return self.bitmap[start:start + width]

                start += width

        except StopIteration:
            pass

        return b""

    def print(self, text: str) -> bytearray:
        try:
            return bytearray(b"\0".join(self[ord(c)] for c in text))
        except MemoryError:
            return None # type: ignore
