import subprocess
from datetime import datetime
import sys

def read_ips(filename):
	with open(filename) as f:
		return [line.strip() for line in f if line.strip()]

def is_up(ip):
	result = subprocess.run(["ping", "-c", "1", ip],
		stdout=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL,
	)
	return result.returncode == 0

def main():
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "ips.txt"
	try:
		ips = read_ips(filename)
	except FileNotFoundError:
		print(f"Could not find {filename} - create it with one target per line.")
		sys.exit(1)

# gather : build an IP -> status table
	results = {}
	for ip in ips:
		results[ip] = "UP" if is_up(ip) else "DOWN"
# summarise: count straight from the table
	up_count = list(results.values()).count("UP")
	down_count = len(results) - up_count

	timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	report_name = f"report_{timestamp}.txt"

	
	with open(report_name, "w") as report:
		report.write(f"Ping report -  {timestamp}\n")
		report.write(f"{up_count} UP , {down_count} DOWN\n")
		report.write("-" * 30 + "\n")
		for ip, status in results.items():
#			status = "UP" if is_up(ip) else "DOWN"
			line = f"{ip:<16} {status}"
			print(line)
			report.write(line + "\n")
	print(f"\nReport written to {report_name}")

if __name__ == "__main__":
	main()
