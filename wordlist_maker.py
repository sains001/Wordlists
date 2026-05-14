#!/usr/bin/env python3
"""
Wordlist Maker - generator wordlist sederhana.

Gunakan hanya untuk kebutuhan sah, misalnya audit password sistem milik sendiri,
lab keamanan, atau pemulihan akun yang Anda miliki.
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path


DEFAULT_SYMBOLS = ["!", "@", "#", ".", "_", "-"]
LEET_MAP = str.maketrans({
    "a": "4",
    "A": "4",
    "e": "3",
    "E": "3",
    "i": "1",
    "I": "1",
    "o": "0",
    "O": "0",
    "s": "5",
    "S": "5",
    "t": "7",
    "T": "7",
})


def clean_words(words: list[str]) -> list[str]:
    cleaned = []
    seen = set()
    for word in words:
        value = word.strip()
        if value and value not in seen:
            cleaned.append(value)
            seen.add(value)
    return cleaned


def load_words(args: argparse.Namespace) -> list[str]:
    words = list(args.words or [])
    if args.input:
        path = Path(args.input)
        if not path.exists():
            raise FileNotFoundError(f"File input tidak ditemukan: {path}")
        words.extend(path.read_text(encoding="utf-8", errors="ignore").splitlines())
    return clean_words(words)


def case_variants(word: str) -> set[str]:
    return {
        word,
        word.lower(),
        word.upper(),
        word.capitalize(),
    }


def base_variants(words: list[str], use_leet: bool) -> set[str]:
    variants = set()
    for word in words:
        variants.update(case_variants(word))
        if use_leet:
            variants.add(word.translate(LEET_MAP))
            variants.add(word.capitalize().translate(LEET_MAP))
    return {v for v in variants if v}


def join_word_combinations(words: list[str], max_join: int, separators: list[str]) -> set[str]:
    combos = set(words)
    if max_join <= 1:
        return combos

    for size in range(2, max_join + 1):
        for parts in itertools.permutations(words, size):
            combos.add("".join(parts))
            for sep in separators:
                combos.add(sep.join(parts))
    return combos


def add_affixes(items: set[str], numbers: list[str], symbols: list[str]) -> set[str]:
    output = set(items)
    for item in items:
        for number in numbers:
            output.add(f"{item}{number}")
            output.add(f"{number}{item}")
        for symbol in symbols:
            output.add(f"{item}{symbol}")
            output.add(f"{symbol}{item}")
        for number in numbers:
            for symbol in symbols:
                output.add(f"{item}{number}{symbol}")
                output.add(f"{item}{symbol}{number}")
    return output


def filter_length(items: set[str], min_len: int, max_len: int) -> list[str]:
    return sorted(item for item in items if min_len <= len(item) <= max_len)


def generate_wordlist(args: argparse.Namespace) -> list[str]:
    words = load_words(args)
    if not words:
        raise ValueError("Masukkan minimal satu kata dengan --words atau --input.")

    numbers = args.numbers or []
    if args.years:
        numbers.extend(str(year) for year in range(args.year_start, args.year_end + 1))
    numbers = clean_words(numbers)

    symbols = DEFAULT_SYMBOLS if args.symbols else []
    if args.custom_symbols:
        symbols.extend(args.custom_symbols)
    symbols = clean_words(symbols)

    variants = base_variants(words, args.leet)
    combined = join_word_combinations(sorted(variants), args.max_join, args.separators)
    final = add_affixes(combined, numbers, symbols)
    filtered = filter_length(final, args.min_length, args.max_length)

    if len(filtered) > args.limit:
        return filtered[: args.limit]
    return filtered


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generator wordlist Python untuk audit sah dan lab keamanan."
    )
    parser.add_argument("-w", "--words", nargs="*", help="Kata dasar, contoh: admin toko jakarta")
    parser.add_argument("-i", "--input", help="File berisi kata dasar, satu kata per baris.")
    parser.add_argument("-o", "--output", default="wordlist.txt", help="Nama file output.")
    parser.add_argument("-n", "--numbers", nargs="*", default=[], help="Angka tambahan, contoh: 123 2024 01")
    parser.add_argument("--years", action="store_true", help="Tambahkan range tahun.")
    parser.add_argument("--year-start", type=int, default=1990, help="Awal range tahun.")
    parser.add_argument("--year-end", type=int, default=2030, help="Akhir range tahun.")
    parser.add_argument("--symbols", action="store_true", help="Tambahkan simbol umum.")
    parser.add_argument("--custom-symbols", nargs="*", default=[], help="Simbol custom, contoh: '$' '%'")
    parser.add_argument("--separators", nargs="*", default=["", "_", "-", "."], help="Pemisah kombinasi kata.")
    parser.add_argument("--leet", action="store_true", help="Tambahkan variasi leetspeak sederhana.")
    parser.add_argument("--max-join", type=int, default=2, choices=[1, 2, 3], help="Maksimal gabungan kata.")
    parser.add_argument("--min-length", type=int, default=4, help="Panjang minimal hasil.")
    parser.add_argument("--max-length", type=int, default=24, help="Panjang maksimal hasil.")
    parser.add_argument("--limit", type=int, default=100000, help="Batas maksimal jumlah baris output.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        words = generate_wordlist(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    output_path = Path(args.output)
    output_path.write_text("\n".join(words) + ("\n" if words else ""), encoding="utf-8")
    print(f"Selesai: {len(words)} kata ditulis ke {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
