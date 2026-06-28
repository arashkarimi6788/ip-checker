# IP Checker

A small Python tool that reads a named inventory of hosts from a file, pings them
in parallel, and writes a timestamped up/down report.

## What it does

Reads a CSV inventory (`name,ip` per line), sends a single ICMP echo to each host
concurrently using a thread pool, and records whether it replied. Results are
printed to the screen, saved to a timestamped report file, and logged to
`ping.log` so every run is kept as a record.

## Requirements

- Python 3 (standard library only — nothing to install)
- Linux or macOS (uses the `-c` and `-w` ping flags; Windows ping differs)

## Usage

1. List your hosts in `inventory.txt`, one `name,ip` pair per line:

```
dns,8.8.8.8
google,google.com
gateway,192.168.1.1
```

2. Run the script:

```bash
python3 ping.py
```

You can point it at a different inventory file and tune the number of parallel
workers:

```bash
python3 ping.py hosts.csv --workers 100
```

Full options:

```
usage: ping.py [-h] [--workers WORKERS] [inventory]

Ping a named inventory of hosts

positional arguments:
  inventory          CSV inventory file (name,ip per line). Defaults to inventory.txt

options:
  -h, --help         show this help message and exit
  --workers WORKERS  Number of parallel ping workers (default: 50)
```

3. Output appears on screen and in a report file named
   `report_YYYY-MM-DD_HH-MM-SS.txt`:

```
Ping report - 2026-06-13_14-44-11
4 UP, 2 DOWN
----------------------------------------
dns          (8.8.8.8        ) UP
dns2         (4.2.2.4        ) UP
core-sw      (10.10.10.10    ) DOWN
google       (google.com     ) UP
yahoo        (yahoo.com      ) UP
router       (180.34.56.23   ) DOWN
```

## Limitations

This tool reports reachability by ICMP only. A host that blocks ICMP — common on
firewalls and many production servers — will show as DOWN even though it is
running normally. A DOWN result means "no ping reply," not "host is off"; the
script cannot distinguish a host that is down from one that is filtering ICMP.
