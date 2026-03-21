from __future__ import annotations

import asyncio
import argparse
import string
import subprocess
import time
import wave
from pathlib import Path

import edge_tts
import imageio_ffmpeg


OUT_ROOT = Path(r"f:\Project\OpenMATB-CN\includes\sounds\chinese")


def build_text_map() -> dict[str, str]:
    text_map: dict[str, str] = {}
    for d in string.digits:
        text_map[d] = d
    for c in string.ascii_lowercase:
        text_map[c] = c.upper()
    text_map.update(
        {
            "com_1": "通信一",
            "com_2": "通信二",
            "nav_1": "导航一",
            "nav_2": "导航二",
            "radio": "无线电",
            "point": "点",
            "frequency": "频率",
        }
    )
    return text_map


def write_silence_wav(path: Path, duration_s: float = 0.2, sample_rate: int = 24000) -> None:
    n_frames = int(sample_rate * duration_s)
    silence = b"\x00\x00" * n_frames
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(silence)


async def synthesize(text: str, out_file: Path, voice: str) -> None:
    mp3_file = out_file.with_suffix(".mp3")
    last_error: Exception | None = None
    for _ in range(5):
        try:
            tts = edge_tts.Communicate(text=text, voice=voice)
            await tts.save(str(mp3_file))
            last_error = None
            break
        except Exception as e:  # noqa: BLE001
            last_error = e
            time.sleep(1.5)
    if last_error is not None:
        raise last_error
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run(
        [
            ffmpeg_exe,
            "-y",
            "-i",
            str(mp3_file),
            "-ac",
            "1",
            "-ar",
            "24000",
            str(out_file),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    mp3_file.unlink(missing_ok=True)


async def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Chinese voice pack for OpenMATB communications.")
    parser.add_argument("--gender", choices=["male", "female"], default="male", help="Voice gender folder to output.")
    args = parser.parse_args()

    if args.gender == "female":
        voice = "zh-CN-XiaoxiaoNeural"
    else:
        voice = "zh-CN-YunjianNeural"

    out_dir = OUT_ROOT / args.gender
    out_dir.mkdir(parents=True, exist_ok=True)
    text_map = build_text_map()

    for name, text in text_map.items():
        out_file = out_dir / f"{name}.wav"
        if out_file.exists():
            print(f"skip: {out_file.name}")
            continue
        await synthesize(text, out_file, voice)
        print(f"generated: {out_file.name}")

    write_silence_wav(out_dir / "empty.wav")
    print("generated: empty.wav")
    print(f"done: {out_dir}")


if __name__ == "__main__":
    asyncio.run(main())

