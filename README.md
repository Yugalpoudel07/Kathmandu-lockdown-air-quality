# Kathmandu-lockdown-air-quality
Did Kathmandu's air get cleaner during the 2020 COVID lockdown? An analysis of US Embassy PM2.5 data.

## The question

During Nepal's 2020 COVID lockdown (from 24 March 2020), was Kathmandu's daily PM2.5 lower than in the same calendar weeks of 2017-2019, and by how much?

*Main number:* difference in mean daily PM2.5 (2020 lockdown weeks minus the 2017-2019 same-weeks average), in µg/m³, with a bootstrap 95% confidence interval (resampling days, seed 42).

## Get the data

```
python src/download_data.py
```

Source, licence and column details: [data/README.md](data/README.md).
