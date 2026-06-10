# IP Checker

A small Python script that reads a list of IP addresses or hostnames from a
file, pings each one, and writes a timestamped up/down report.

## What it does

Reads targets from `ips.txt` (one per line), sends a single ICMP echo to each,
and records whether it replied. Results are printed to the screen and saved to a
timestamped file so every run is kept as a record.

## Requirements

- Python 3 (standard library only — nothing to install)
- Linux or macOS (uses the `-c` and `-W` ping flags; Windows ping differs)

## Usage

1. List your targets in `ips.txt`, one per line:

```
   8.8.8.8
   google.com
   192.168.1.1
```

2. Run the script:

```bash
   python3 ip_checker.py
```

3. Output appears on screen and in a report file named
   `report_YYYY-MM-DD_HH-MM-SS.txt`:

```
   8.8.8.8          UP
   google.com       UP
   192.168.1.1      DOWN
```

## Limitations

This tool reports reachability by ICMP only. A host that blocks ICMP — common on
firewalls and many production servers — will show as DOWN even though it is
running normally. A DOWN result means "no ping reply," not "host is off"; the
script cannot distinguish a host that is down from one that is filtering ICMP.
