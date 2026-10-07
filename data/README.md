# Data

## Source

| | |
|---|---|
| Publisher | Open Data Nepal (run by Open Knowledge Nepal) |
| Dataset | [Air Quality Data in Kathmandu](https://opendatanepal.com/dataset/air-quality-data-in-kathmandu) |
| Original measurements | US Department of State, US Diplomatic Post monitors in Kathmandu (distributed in OpenAQ format) |
| Licence | Creative Commons Attribution Share-Alike (CC BY-SA). Attribution: "Air Quality Data in Kathmandu", Open Data Nepal / Open Knowledge Nepal, CC BY-SA. |
| Resources | Uploaded 18 July 2025 to the relaunched portal (data itself ends 13 March 2021) |
| Downloaded | 6 October 2026 |

## How to get the files

From the project root:

```
python src/download_data.py
```

The script downloads both CSVs into `data/raw/`, then prints each file's size, row count and SHA-256 checksum and checks it against the checksum of the files used in this analysis. If the checksum differs, the publisher has changed the file and results may not match.

Manual fallback: open the [dataset page](https://opendatanepal.com/dataset/air-quality-data-in-kathmandu), click **Download** on each resource ("index us diplomatic post embassy" / "... phora durbar"), and save the file under the name in the "Saved as" column. The publisher's own file names are `tmpv4ryiymi.csv` (Embassy) and `tmpaoakgen9.csv` (Phora Durbar).

| Saved as (`data/raw/`) | Station | Direct download | Size | Rows | SHA-256 |
|---|---|---|---|---|---|
| `kathmandu_embassy.csv` | US Diplomatic Post: Embassy Kathmandu (locationId 3459; 27.7387 N, 85.3362 E) | [link](https://api.opendatanepal.com/dataset/518f6d75-3a43-4cef-90a6-9149a2815e6d/resource/ad8d1b4d-7667-455d-ab74-d5966e8ba4c3/download/tmpv4ryiymi.csv) | 8.7 MB | 60,779 | `ef6e51da2ab7ef474e1a221906904784eb7f1e4cdbbbd1d32cb140b75770f8c3` |
| `kathmandu_phora_durbar.csv` | US Diplomatic Post: Phora Durbar Kathmandu (locationId 3460; 27.7125 N, 85.3157 E) | [link](https://api.opendatanepal.com/dataset/518f6d75-3a43-4cef-90a6-9149a2815e6d/resource/918b774b-2a51-404f-92a0-0be1fe780f90/download/tmpaoakgen9.csv) | 9.2 MB | 61,976 | `e8d9dd5ecbc0d6f109195d65bf05ac57abfc2b5901ef1b22af8785e2b8031da6` |

Row counts exclude the header. The raw files are not committed to Git (see `.gitignore`); `data/raw/` is never edited. Cleaned data is written by notebook 01 to `data/processed/`.

## What one row is

**One station x one hour x one pollutant** (long format). Each hour normally has two rows: one `pm25` and one `o3`. This project uses only `parameter == "pm25"`.

## Columns

| Column | Meaning | Example |
|---|---|---|
| `locationId` | OpenAQ station id (3459 Embassy, 3460 Phora Durbar) | `3459` |
| `location` | Station name | `US Diplomatic Post: Embassy Kathmandu` |
| `city`, `country` | Always `Kathmandu`, `NP` | |
| `utc` | Timestamp in UTC (ISO 8601) | `2021-03-12T18:15:00+00:00` |
| `local` | Same moment in Nepal time, **UTC+05:45** | `2021-03-13T00:00:00+05:45` |
| `parameter` | Pollutant: `pm25` (fine particles, PM2.5) or `o3` (ozone) | `pm25` |
| `value` | Measured concentration (hourly) | `50` |
| `unit` | `µg/m³` for pm25, `ppm` for o3 | `µg/m³` |
| `latitude`, `longitude` | Station coordinates | `27.738703`, `85.336205` |

## Things to know (found while exploring; handled in notebook 01)

- **Time zone.** Every UTC timestamp is at :15 past the hour, which is exactly on the hour in Nepal time (+05:45). Daily averages use the `local` column so a "day" is a Nepali calendar day.
- **Time range.** 2017-03-03 05:00 to 2021-03-13 00:00 local time. The dataset description says data from 2015, but these files start in March 2017, so the 2017 baseline is partial (no Jan-Feb 2017).
- **Missing-value codes.** `-999` (pm25) and `-0.999` (o3) mean "no reading". PM2.5 rows with -999: Embassy 3,383; Phora Durbar 2,401.
- **Other negative PM2.5 values** (-1 to -15): Embassy 178 rows, Phora Durbar 46. Physically impossible; treated as invalid.
- **Maximum PM2.5 = 985 µg/m³** in both files, which may be the instrument ceiling. Checked in notebook 01.
- **Gaps.** Hours with no row at all (monitor offline) are not marked; counted per day in notebook 01.

## Processed files (made by notebook 01, not committed)

| File (`data/processed/`) | One row | Rows | Columns |
|---|---|---|---|
| `pm25_hourly_clean.csv` | one valid PM2.5 reading (station × hour) | 57,202 | `station`, `locationId`, `local_dt` (Nepal time), `date`, `pm25` (µg/m³), `is_suspect` (isolated spike or 985 ceiling; kept, flagged) |
| `pm25_daily.csv` | one station × one Nepal calendar day, including days with no data | 2,944 (1,472 days × 2 stations) | `station`, `date`, `n_hours` (valid hourly readings, 0-24), `pm25_mean`, `pm25_median`, `pm25_mean_no_suspect` (µg/m³), `valid_day` (`n_hours >= 18`) |

Notebook 02 uses `pm25_daily.csv`. The cleaning steps and row counts are in the main [README](../README.md#cleaning-decisions).
