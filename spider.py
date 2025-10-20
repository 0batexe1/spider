#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, json, threading, queue, re, os, sys, time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from colorama import Fore, init
import argparse, jsbeautifier

init(autoreset=True)

# -------------------
# Config & Keywords
# -------------------
KEYWORDS = [
    "api_key", "secret", "token", "access_key", "client_secret", "private_key",
    "jwt", "password", "pem", "rsa", "ssh", "auth", "Auth", "Key", "PwD"
]

HTTP_METHODS = ["GET", "POST", "PUT", "PATCH"]
TIMEOUT = 10
RETRIES = 2

# -------------------
# Global files
# -------------------
URLS_FILE = "urls.txt"
RAW_JSON_FILE = "raw_findings.json"
TESTED_JSON_FILE = "tested_findings.json"
HTML_REPORT_FILE = "aquatone_style_report.html"

# -------------------
# Threading
# -------------------
q = queue.Queue()
visited = set()
lock = threading.Lock()

# -------------------
# Argparse
# -------------------
parser = argparse.ArgumentParser(description="Multi-threaded web scanner with depth, dir/sub/all modes and cross-endpoint validation")
parser.add_argument("-u", "--url", help="Target URL")
parser.add_argument("-t", "--txt", help="File with URLs")
parser.add_argument("-th", "--threads", type=int, default=10, help="Number of threads")
parser.add_argument("-m", "--mode", action="append", choices=["dep1","dep2","dep3","dir","sub","all"], help="Scan modes")
parser.add_argument("--proxy", help="Optional proxy, e.g., http://127.0.0.1:8080")
args = parser.parse_args()

if not args.url and not args.txt:
    print(Fore.RED + "[!] URL veya TXT dosyası girilmedi!")
    sys.exit(1)

targets = []
if args.url:
    targets.append(args.url.strip())
if args.txt:
    with open(args.txt, "r") as f:
        for line in f:
            url = line.strip()
            if url:
                targets.append(url)

MODES = args.mode if args.mode else ["all"]
PROXY = {"http": args.proxy, "https": args.proxy} if args.proxy else None

# -------------------
# Helper functions
# -------------------
def save_file(filename, content):
    with lock:
        with open(filename, "a") as f:
            f.write(content + "\n")

def extract_keywords(text):
    findings = []
    for k in KEYWORDS:
        regex = re.compile(rf"{k}\s*[:=]\s*['\"]?([\w\-/+_]+)['\"]?", re.IGNORECASE)
        matches = regex.findall(text)
        for m in matches:
            findings.append({"type": k, "value": m})
    return findings

def test_key(url, key_value):
    for method in HTTP_METHODS:
        for attempt in range(RETRIES):
            try:
                headers = {"Authorization": key_value}
                params = {"api_key": key_value}
                r = requests.request(method, url, headers=headers, params=params, timeout=TIMEOUT, proxies=PROXY)
                if r.status_code == 200:
                    return True
            except:
                time.sleep(1)
    return False

def same_domain(base, url):
    return urlparse(base).netloc == urlparse(url).netloc

# -------------------
# Crawl function
# -------------------
def crawl(url, depth=1):
    if url in visited or not same_domain(targets[0], url):
        return
    visited.add(url)
    save_file(URLS_FILE, url)
    print(Fore.BLUE + "[URL] " + url)

    try:
        r = requests.get(url, timeout=TIMEOUT, proxies=PROXY)
        text = r.text
    except:
        print(Fore.YELLOW + "[ERROR] Cannot access " + url)
        return

    if ".js" in url:
        try:
            text = jsbeautifier.beautify(text)
        except:
            pass

    findings = extract_keywords(text)
    raw_results = []
    for f in findings:
        raw_results.append({
            "url": url,
            "type": f['type'],
            "value": f['value'],
            "curl": f"curl -H 'Authorization: {f['value']}' {url}"
        })

    save_file(RAW_JSON_FILE, json.dumps(raw_results))

    # Depth link extraction
    if any(m in MODES for m in ["dep1","dep2","dep3","dir","all"]):
        try:
            soup = BeautifulSoup(text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = urljoin(url, a["href"])
                if href not in visited and same_domain(targets[0], href) and depth < 3:
                    q.put((href, depth+1))
        except:
            pass

# -------------------
# Worker thread
# -------------------
def worker():
    while True:
        try:
            url, depth = q.get(timeout=5)
        except:
            break
        crawl(url, depth)
        q.task_done()

# -------------------
# Start crawling
# -------------------
for t in targets:
    q.put((t,1))

threads = []
for i in range(args.threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

q.join()
for t in threads:
    t.join()

print(Fore.GREEN + "[+] Crawl finished.")

# -------------------
# Cross-endpoint testing
# -------------------
all_findings = []
if os.path.exists(RAW_JSON_FILE):
    with open(RAW_JSON_FILE,"r") as f:
        for line in f:
            all_findings.extend(json.loads(line))

# Remove duplicates
unique_findings = {f['value']: f for f in all_findings}.values()

active_findings = []
for f in unique_findings:
    active_urls = []
    for url in targets:
        if test_key(url, f['value']):
            active_urls.append(url)
    f['status'] = 200 if active_urls else 403
    f['active_on'] = active_urls
    active_findings.append(f)

with open(TESTED_JSON_FILE,"w") as f:
    json.dump(active_findings, f, indent=2)

print(Fore.GREEN + f"[+] Cross-endpoint testing finished. {len(active_findings)} findings tested.")

# -------------------
# HTML rapor (Aquatone tarzı)
# -------------------
html_content = f"""
<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<title>Scan Report</title>
<style>
body {{ font-family: Arial; background: #1e1e1e; color: #ccc; }}
.container {{ width: 90%; margin: auto; }}
.finding {{ padding: 10px; margin:5px; border-radius:5px; }}
.active {{ background: #ff4d4d; }}
.inactive {{ background: #2d2d2d; }}
.type {{ font-weight:bold; }}
.curl {{ font-family: monospace; color:#0f0; }}
</style>
</head>
<body>
<div class='container'>
<h1>Scan Report</h1>
<div id='results'></div>
<script>
const findings = {json.dumps(active_findings)};
const container = document.getElementById('results');
findings.forEach(f => {{
  let div = document.createElement('div');
  div.className = 'finding ' + (f.status==200?'active':'inactive');
  div.innerHTML = `<div class='type'>${{f.type}}</div><div>URL: ${{f.url}}</div><div>Value: ${{f.value}}</div><div>Active on: ${{f.active_on.join(', ')}}</div><div class='curl'>${{f.curl}}</div>`;
  container.appendChild(div);
}});
</script>
</div>
</body>
</html>
"""

with open(HTML_REPORT_FILE,"w") as f:
    f.write(html_content)

print(Fore.GREEN + f"[+] HTML report generated: {HTML_REPORT_FILE}")
