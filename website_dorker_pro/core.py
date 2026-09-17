"""
Dependency-free passive recon engine for WebsiteDorkerPro.

Uses only the Python standard library (urllib, socket, ssl, json, re) so it
runs anywhere, including headless servers and offline setups. No pip
dependencies are required.

NOTE: This module must NOT import tkinter or any GUI code. Keep it pure.
"""

import socket
import ssl
import json
import re
import urllib.request
import urllib.error
from urllib.parse import urljoin

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)
DEFAULT_TIMEOUT = 10

# Common paths probed by the lightweight directory fuzzer
FUZZ_PATHS = [
    "/robots.txt", "/sitemap.xml", "/sitemap_index.xml", "/wp-login.php",
    "/xmlrpc.php", "/.git/HEAD", "/.env", "/.htaccess", "/config.php",
    "/config.inc.php", "/phpinfo.php", "/info.php", "/test.php",
    "/admin/", "/login/", "/backup/", "/backup.zip", "/db.sql",
    "/database.sql", "/dump.sql", "/.DS_Store", "/web.config",
    "/crossdomain.xml", "/README.md", "/server-status", "/server-info",
]

# HTTP response headers that matter from an infosec point of view
IMPORTANT_HEADERS = [
    "Strict-Transport-Security", "Content-Security-Policy",
    "X-Content-Type-Options", "X-Frame-Options", "X-XSS-Protection",
    "Referrer-Policy", "Permissions-Policy", "Server", "X-Powered-By",
]


def _ssl_context():
    """Build an SSL context that silently tolerates common recon targets."""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    except Exception:
        return None


def http_fetch(url, timeout=DEFAULT_TIMEOUT, max_bytes=512 * 1024):
    """
    Fetch a URL with a browser User-Agent.

    Returns a dict with keys: url, status, headers, body.
    Never raises; on network failure status is None and body contains the error.
    """
    result = {"url": url, "status": None, "headers": {}, "body": ""}
    req = urllib.request.Request(
        url,
        headers={"User-Agent": DEFAULT_USER_AGENT, "Accept-Encoding": "identity"},
    )
    try:
        opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=_ssl_context())
        )
        with opener.open(req, timeout=timeout) as resp:
            result["status"] = resp.getcode()
            result["headers"] = dict(resp.headers.items())
            result["body"] = resp.read(max_bytes).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        result["status"] = e.code
        result["headers"] = dict(e.headers.items()) if e.headers else {}
        try:
            result["body"] = e.read(max_bytes).decode("utf-8", errors="replace")
        except Exception:
            result["body"] = ""
    except Exception as e:  # socket timeouts, SSL errors, etc.
        result["body"] = f"ERROR: {type(e).__name__}: {e}"
    return result


def normalize_domain(domain):
    """Strip scheme, www, ports, paths and query strings from a target."""
    domain = re.sub(r"^https?://", "", domain or "")
    domain = re.sub(r"^www\.", "", domain)
    domain = re.sub(r"/.*$", "", domain)          # path
    domain = re.sub(r":[0-9]+$", "", domain)       # port
    domain = re.sub(r"[?#].*$", "", domain)        # query/fragment
    return domain.strip().lower()


def resolve_ip(domain, timeout=5):
    """Resolve a domain to its IPv4 addresses using a plain socket."""
    domain = normalize_domain(domain)
    if not domain:
        return []
    try:
        infos = socket.getaddrinfo(domain, None, socket.AF_INET)
        return sorted({info[4][0] for info in infos})
    except Exception:
        return []


def check_robots(domain):
    """Fetch and parse /robots.txt, returning allowed/disallowed paths."""
    domain = normalize_domain(domain)
    if not domain:
        return {"status": None, "rules": []}
    res = http_fetch(f"https://{domain}/robots.txt")
    rules = []
    if res["status"] in (200, 206):
        agent = None
        for line in res["body"].splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key, value = key.strip().upper(), value.strip()
            if key == "USER-AGENT":
                agent = value or "*"
            elif key in ("ALLOW", "DISALLOW"):
                rules.append({"agent": agent or "*", "action": key, "path": value})
    return {"status": res["status"], "rules": rules}


def check_sitemap(domain):
    """Fetch /sitemap.xml (or index) and extract discovered URLs."""
    domain = normalize_domain(domain)
    if not domain:
        return {"status": None, "urls": []}
    candidates = ["/sitemap.xml", "/sitemap_index.xml", "/sitemap-index.xml"]
    urls = []
    status = None
    for path in candidates:
        res = http_fetch(f"https://{domain}{path}")
        if res["status"] in (200, 206):
            status = res["status"]
            urls = re.findall(r"<loc>\s*(.*?)\s*</loc>", res["body"], re.S)
            break
    return {"status": status, "urls": urls}


def get_security_headers(domain):
    """Fetch the homepage and report HTTP + security headers."""
    domain = normalize_domain(domain)
    if not domain:
        return {"status": None, "important": [], "all": {}}
    res = http_fetch(f"https://{domain}/")
    important = {
        header: res["headers"].get(header)
        for header in IMPORTANT_HEADERS
        if res["headers"].get(header)
    }
    return {"status": res["status"], "important": important, "all": res["headers"]}


def http_status(domain):
    """Check HTTP vs HTTPS reachability and their status codes."""
    domain = normalize_domain(domain)
    if not domain:
        return {}
    http_res = http_fetch(f"http://{domain}/", max_bytes=2 * 1024)
    https_res = http_fetch(f"https://{domain}/", max_bytes=2 * 1024)
    return {
        "http": http_res["status"],
        "https": https_res["status"],
        "fallback": http_res["headers"].get("Location", ""),
    }


def enumerate_subdomains(domain):
    """
    Passive subdomain enumeration via crt.sh certificate transparency logs
    and the AlienVault OTX passive DNS feed. Pure HTTP, no API keys.
    """
    domain = normalize_domain(domain)
    if not domain:
        return []
    found = set()

    # crt.sh certificate transparency
    try:
        res = http_fetch(f"https://crt.sh/?q=%25.{domain}&output=json")
        if res["status"] == 200 and res["body"].lstrip().startswith("["):
            for entry in json.loads(res["body"]):
                names = entry.get("name_value", "")
                for name in names.splitlines():
                    name = name.strip().lower().lstrip("*.")
                    found.add(name)
    except Exception:
        pass

    # AlienVault OTX passive DNS
    try:
        res = http_fetch(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns")
        if res["status"] == 200:
            data = json.loads(res["body"])
            for row in data.get("passive_dns", []):
                hostname = (row.get("hostname") or "").strip().lower()
                if hostname:
                    found.add(hostname)
    except Exception:
        pass

    return sorted(found)


def weak_fuzz(domain, paths=None):
    """Probe a list of common paths, returning (path, status) results."""
    domain = normalize_domain(domain)
    if not domain:
        return []
    paths = paths or FUZZ_PATHS
    results = []
    for path in paths:
        res = http_fetch(f"https://{domain}{urljoin('/', path)}", max_bytes=2 * 1024)
        if res["status"] and res["status"] not in (404, 400, 500):
            results.append((path, res["status"]))
    return results


def passive_recon(domain):
    """
    Run the full lightweight reconnaissance sweep and return a plain-text
    report. Safe to call from any thread; returns everything, opens nothing.
    """
    domain = normalize_domain(domain)
    if not domain:
        return "No valid domain provided."

    lines = []
    lines.append("=" * 56)
    lines.append(f"PASSIVE RECON REPORT for {domain}")
    lines.append("=" * 56)

    ips = resolve_ip(domain)
    lines.append(f"\n[IP RESOLUTION]")
    lines.append(f"  IPv4 addresses: {', '.join(ips) if ips else 'unresolvable'}")

    status = http_status(domain)
    lines.append(f"\n[HTTP / HTTPS]")
    lines.append(f"  http:  {status.get('http')}")
    lines.append(f"  https: {status.get('https')}")

    rx = check_robots(domain)
    lines.append(f"\n[ROBOTS.TXT] (status {rx['status']})")
    if rx["rules"]:
        for rule in rx["rules"][:15]:
            lines.append(f"  {rule['action']:9} {rule['path']}")
    elif rx["status"] == 200:
        lines.append("  (no rules found)")

    sm = check_sitemap(domain)
    lines.append(f"\n[SITEMAP] (status {sm['status']})")
    if sm["urls"]:
        lines.append(f"  {len(sm['urls'])} URLs discovered (first 5):")
        for u in sm["urls"][:5]:
            lines.append(f"  - {u}")
    else:
        lines.append("  no sitemap found")

    hdrs = get_security_headers(domain)
    lines.append(f"\n[SECURITY HEADERS] (status {hdrs['status']})")
    if hdrs["important"]:
        for key, value in hdrs["important"].items():
            lines.append(f"  {key}: {value}")
    else:
        lines.append("  none of the important security headers present")

    subs = enumerate_subdomains(domain)
    lines.append(f"\n[SUBDOMAINS] ({len(subs)} found via crt.sh + OTX)")
    for sub in subs[:20]:
        lines.append(f"  - {sub}")

    fuzz = weak_fuzz(domain)
    lines.append(f"\n[PATH PROBE] ({len(fuzz)} interesting hits)")
    for path, code in fuzz[:20]:
        lines.append(f"  {code}  {path}")

    lines.append("\n" + "=" * 56)
    lines.append("Report generated at {} (EDT).".format(
        "v2.1" if False else __import__("time").strftime("%Y-%m-%d %H:%M:%S")
    ))
    lines.append("=" * 56)
    return "\n".join(lines)
