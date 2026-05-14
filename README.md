# WordlistMaker

WordlistMaker adalah generator wordlist sederhana berbasis Python. Tool ini membuat variasi kata dari kata dasar, angka, simbol, gabungan kata, kapitalisasi, dan leetspeak sederhana.

Gunakan hanya untuk kebutuhan sah, misalnya audit password sistem milik sendiri, lab keamanan, atau pemulihan akun yang Anda miliki.

## Fitur

- Input kata dasar dari command line
- Input kata dasar dari file
- Variasi huruf kecil, huruf besar, dan kapitalisasi awal
- Variasi leetspeak sederhana, contoh `a` menjadi `4`, `e` menjadi `3`
- Tambahan angka di depan atau belakang kata
- Tambahan simbol umum atau simbol custom
- Gabungan beberapa kata dengan separator
- Filter panjang minimal dan maksimal
- Batas maksimal jumlah output
- Tanpa dependency eksternal, cukup Python 3

## Struktur

```text
WordlistMaker/
├── wordlist_maker.py
└── README.md
```

## Cara Menjalankan

Masuk ke folder tool:

```bash
cd /home/kali/WordlistMaker
```

Buat wordlist dasar:

```bash
python3 wordlist_maker.py -w admin toko jakarta -o hasil.txt
```

Hasil akan ditulis ke file output. Jika `-o` tidak diisi, output default adalah `wordlist.txt`.

## Contoh Penggunaan

Kata dasar dengan angka:

```bash
python3 wordlist_maker.py -w admin user -n 123 2024 01 -o hasil.txt
```

Tambahkan simbol umum:

```bash
python3 wordlist_maker.py -w admin toko --symbols -o hasil.txt
```

Tambahkan leetspeak:

```bash
python3 wordlist_maker.py -w admin password --leet -o hasil.txt
```

Tambahkan range tahun:

```bash
python3 wordlist_maker.py -w toko jakarta --years --year-start 2000 --year-end 2026 -o hasil.txt
```

Gunakan input dari file:

```bash
python3 wordlist_maker.py -i kata.txt -o hasil.txt
```

Gabungkan kata maksimal 3 kata:

```bash
python3 wordlist_maker.py -w admin toko jakarta --max-join 3 -o hasil.txt
```

Atur separator gabungan:

```bash
python3 wordlist_maker.py -w admin toko --separators _ - . -o hasil.txt
```

Batasi panjang hasil:

```bash
python3 wordlist_maker.py -w admin toko jakarta --min-length 6 --max-length 16 -o hasil.txt
```

Batasi jumlah baris output:

```bash
python3 wordlist_maker.py -w admin toko jakarta --symbols --leet --limit 5000 -o hasil.txt
```

Contoh lengkap:

```bash
python3 wordlist_maker.py -w admin toko jakarta -n 123 2024 --symbols --leet --max-join 2 --min-length 6 --max-length 20 --limit 10000 -o hasil.txt
```

## Format File Input

File input berisi satu kata per baris:

```text
admin
toko
jakarta
user
password
```

Jalankan:

```bash
python3 wordlist_maker.py -i kata.txt --symbols --years -o hasil.txt
```

## Opsi

| Opsi | Default | Keterangan |
| --- | --- | --- |
| `-w`, `--words` | kosong | Kata dasar dari command line |
| `-i`, `--input` | kosong | File input, satu kata per baris |
| `-o`, `--output` | `wordlist.txt` | File output |
| `-n`, `--numbers` | kosong | Angka tambahan, contoh `123 2024 01` |
| `--years` | mati | Tambahkan range tahun |
| `--year-start` | `1990` | Awal range tahun |
| `--year-end` | `2030` | Akhir range tahun |
| `--symbols` | mati | Tambahkan simbol umum: `! @ # . _ -` |
| `--custom-symbols` | kosong | Simbol custom |
| `--separators` | `"" _ - .` | Separator untuk gabungan kata |
| `--leet` | mati | Tambahkan variasi leetspeak sederhana |
| `--max-join` | `2` | Maksimal gabungan kata. Pilihan: `1`, `2`, `3` |
| `--min-length` | `4` | Panjang minimal hasil |
| `--max-length` | `24` | Panjang maksimal hasil |
| `--limit` | `100000` | Batas maksimal jumlah baris output |

## Leetspeak

Jika opsi `--leet` aktif, tool memakai mapping berikut:

| Huruf | Pengganti |
| --- | --- |
| `a` | `4` |
| `e` | `3` |
| `i` | `1` |
| `o` | `0` |
| `s` | `5` |
| `t` | `7` |

Contoh:

```text
password -> p455w0rd
admin -> 4dm1n
```

## Catatan

Jumlah kombinasi bisa tumbuh sangat cepat, terutama jika memakai `--max-join 3`, `--symbols`, `--years`, dan `--leet` secara bersamaan. Gunakan `--limit`, `--min-length`, dan `--max-length` agar output tetap terkendali.
