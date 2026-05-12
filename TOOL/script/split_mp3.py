#!/usr/bin/env python3
"""Split MP3 files into frame-aligned chunks without ffmpeg."""

from __future__ import annotations

import argparse
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
TOOL_DIR = SCRIPT_DIR.parent
DEFAULT_INPUT = TOOL_DIR / "audios" / "aiops_extracted.mp3"
DEFAULT_OUTPUT_DIR = TOOL_DIR / "audio_chunks"

BITRATES = {
    "V1L3": [None, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, None],
    "V2L3": [None, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, None],
}
SAMPLE_RATES = {
    0b11: [44100, 48000, 32000, None],
    0b10: [22050, 24000, 16000, None],
    0b00: [11025, 12000, 8000, None],
}


def skip_id3(data: bytes) -> int:
    if not data.startswith(b"ID3") or len(data) < 10:
        return 0
    size = 0
    for byte in data[6:10]:
        size = (size << 7) | (byte & 0x7F)
    return 10 + size


def parse_frame(data: bytes, offset: int) -> tuple[int, float] | None:
    if offset + 4 > len(data):
        return None
    header = int.from_bytes(data[offset : offset + 4], "big")
    if (header & 0xFFE00000) != 0xFFE00000:
        return None

    version_bits = (header >> 19) & 0b11
    layer_bits = (header >> 17) & 0b11
    bitrate_index = (header >> 12) & 0b1111
    sample_rate_index = (header >> 10) & 0b11
    padding = (header >> 9) & 0b1

    if layer_bits != 0b01 or version_bits == 0b01:
        return None
    sample_rates = SAMPLE_RATES.get(version_bits)
    sample_rate = sample_rates[sample_rate_index] if sample_rates else None
    if not sample_rate:
        return None

    version_key = "V1L3" if version_bits == 0b11 else "V2L3"
    bitrate_kbps = BITRATES[version_key][bitrate_index]
    if not bitrate_kbps:
        return None

    if version_bits == 0b11:
        frame_length = int((144000 * bitrate_kbps) / sample_rate + padding)
        samples_per_frame = 1152
    else:
        frame_length = int((72000 * bitrate_kbps) / sample_rate + padding)
        samples_per_frame = 576
    return frame_length, samples_per_frame / sample_rate


def split_mp3(input_path: Path, output_dir: Path, chunk_seconds: float, limit: int | None) -> list[Path]:
    data = input_path.read_bytes()
    offset = skip_id3(data)
    output_dir.mkdir(parents=True, exist_ok=True)

    chunks: list[Path] = []
    current = bytearray()
    current_seconds = 0.0
    chunk_index = 1

    while offset < len(data):
        parsed = parse_frame(data, offset)
        if not parsed:
            offset += 1
            continue
        frame_length, frame_seconds = parsed
        if offset + frame_length > len(data):
            break
        current.extend(data[offset : offset + frame_length])
        current_seconds += frame_seconds
        offset += frame_length

        if current_seconds >= chunk_seconds:
            out = output_dir / f"{input_path.stem}_part{chunk_index:03d}.mp3"
            out.write_bytes(current)
            chunks.append(out)
            if limit is not None and len(chunks) >= limit:
                return chunks
            chunk_index += 1
            current = bytearray()
            current_seconds = 0.0

    if current and (limit is None or len(chunks) < limit):
        out = output_dir / f"{input_path.stem}_part{chunk_index:03d}.mp3"
        out.write_bytes(current)
        chunks.append(out)
    return chunks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Split an MP3 file into frame-aligned chunks.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Input MP3 file.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for chunk files.")
    parser.add_argument("--chunk-seconds", type=float, default=300.0, help="Target chunk length in seconds.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of chunks to create.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    chunks = split_mp3(args.input.resolve(), args.output_dir.resolve(), args.chunk_seconds, args.limit)
    print(f"Wrote {len(chunks)} chunk(s) to {args.output_dir.resolve()}")
    for chunk in chunks:
        print(chunk)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
