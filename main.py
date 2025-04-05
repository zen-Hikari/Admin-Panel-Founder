import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import time
from tqdm import tqdm
import colorama

colorama.init(autoreset=True)

# User-Agent list
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36"
]

# Wordlist umum untuk halaman admin
admin_paths = [
    "admin", "admin/login", "administrator", "adminpanel", "dashboard", "login", "user/login"
]

# Keyword yang menunjukkan form login
admin_keywords = ["login", "admin", "dashboard", "username", "password"]

def is_login_page(url):
    try:
        headers = {"User-Agent": random.choice(user_agents)}
        res = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            inputs = [i.get("type", "").lower() for f in soup.find_all("form") for i in f.find_all("input")]
            if "password" in inputs and any(k in res.text.lower() for k in admin_keywords):
                return True
        return False
    except:
        return False

def scan_url(url):
    if is_login_page(url):
        print(f"{colorama.Fore.GREEN}[+] Login page ditemukan: {url}")
        return url
    return None

def crawl_links(target_url, domain):
    try:
        headers = {"User-Agent": random.choice(user_agents)}
        res = requests.get(target_url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        return [urljoin(target_url, a['href']) for a in soup.find_all("a", href=True)
                if urlparse(urljoin(target_url, a['href'])).netloc == domain]
    except:
        return []

def main(target):
    print(f"{colorama.Fore.CYAN}[!] Memulai pencarian halaman login pada: {target}")
    parsed_url = urlparse(target)
    domain = parsed_url.netloc

    # Kumpulkan URL dari link internal dan wordlist
    urls_to_scan = set()

    print(f"{colorama.Fore.YELLOW}[*] Mengumpulkan link internal...")
    internal_links = crawl_links(target, domain)
    urls_to_scan.update(internal_links)

    print(f"{colorama.Fore.YELLOW}[*] Menambahkan wordlist umum...")
    for path in admin_paths:
        urls_to_scan.add(urljoin(target, path))

    found_urls = []

    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = {executor.submit(scan_url, url): url for url in urls_to_scan}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning"):
            result = future.result()
            if result:
                found_urls.append(result)

    print(f"\n{colorama.Fore.CYAN}[✓] Pencarian selesai. Halaman login ditemukan:")
    for url in found_urls:
        print(f"   {colorama.Fore.GREEN}{url}")

    if found_urls:
        with open("hasil_admin_finder.txt", "w") as f:
            for url in found_urls:
                f.write(url + "\n")
        print(f"{colorama.Fore.YELLOW}[*] Hasil disimpan ke 'hasil_admin_finder.txt'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Admin Panel Finder by @Novalhasmi W.")
    parser.add_argument("target", help="URL target (contoh: http://example.com)")
    args = parser.parse_args()

    main(args.target)
