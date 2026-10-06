"""Download the raw Kathmandu air-quality data into data/raw/.

Source: Open Data Nepal (Open Knowledge Nepal), "Air Quality Data in Kathmandu"
        https://opendatanepal.com/dataset/air-quality-data-in-kathmandu
Licence: Creative Commons Attribution Share-Alike (CC BY-SA)

Two CSV files, one per US Embassy (US Diplomatic Post) monitor in Kathmandu.
The script only uses the Python standard library, so it runs before
`pip install -r requirements.txt` if needed.

Usage (from the project root):
    python src/download_data.py           # download missing files, verify all
    python src/download_data.py --force   # re-download even if files exist
"""

import argparse
import hashlib
import sys
import urllib.request
from pathlib import Path

# Project root = the folder that contains src/ (works from any working directory)
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"

BASE = (
    "https://api.opendatanepal.com/dataset/518f6d75-3a43-4cef-90a6-9149a2815e6d/resource"
)

# The publisher's files have temporary names (tmp*.csv); we save them under
# descriptive names. URLs checked 6 Oct 2026 (site relaunched June 2026).
# file name in data/raw -> (download URL, expected SHA-256 of the file we analysed)
FILES = {
    "kathmandu_embassy.csv": (
        f"{BASE}/ad8d1b4d-7667-455d-ab74-d5966e8ba4c3/download/tmpv4ryiymi.csv",
        "ef6e51da2ab7ef474e1a221906904784eb7f1e4cdbbbd1d32cb140b75770f8c3",
    ),
    "kathmandu_phora_durbar.csv": (
        f"{BASE}/918b774b-2a51-404f-92a0-0be1fe780f90/download/tmpaoakgen9.csv",
        "e8d9dd5ecbc0d6f109195d65bf05ac57abfc2b5901ef1b22af8785e2b8031da6",
    ),
}


def sha256(path: Path) -> str:
    """Return the SHA-256 hex digest of a file (read in chunks)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path) -> None:
    """Download url to dest via a temporary .part file, so a failed
    download never leaves a half-written CSV behind."""
    tmp = dest.with_suffix(dest.suffix + ".part")
    print(f"  downloading {url}")
    urllib.request.urlretrieve(url, tmp)
    tmp.replace(dest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help="re-download existing files")
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    all_ok = True

    for name, (url, expected) in FILES.items():
        dest = RAW_DIR / name
        print(f"{name}:")
        if dest.exists() and not args.force:
            print("  already present, skipping download")
        else:
            try:
                download(url, dest)
            except OSError as err:  # URLError, HTTP errors, no internet...
                print(f"  ERROR: download failed ({err}).")
                print("  Download it by hand from the page in data/README.md,")
                print(f"  save it as data/raw/{name}, then run this script again.")
                all_ok = False
                continue

        actual = sha256(dest)
        size_mb = dest.stat().st_size / 1e6
        with open(dest, encoding="utf-8") as f:
            n_rows = sum(1 for _ in f) - 1  # minus header
        print(f"  {size_mb:.1f} MB, {n_rows:,} rows, sha256 {actual[:12]}...")
        if actual == expected:
            print("  checksum OK (identical to the file used in this analysis)")
        else:
            all_ok = False
            print("  WARNING: checksum differs - the publisher may have updated the file")

    print("\nDone." if all_ok else "\nDone, but with checksum warnings (see above).")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
