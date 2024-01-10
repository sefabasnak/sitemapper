import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def get_all_pages(domain):
    # Belirli bir domaindeki tüm sayfaları bulan fonksiyon
    all_pages = set()
    base_url = f"http://{domain}"

    def crawl_page(url):
        # Sayfadaki linkleri çeken fonksiyon
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Hata durumunda hemen programı sonlandır
        except requests.exceptions.RequestException as e:
            print(f"Hata: {e} - {url}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            absolute_url = urljoin(url, link)
            # Sadece belirli bir domain içindeki linkleri ekleyin
            if urlparse(absolute_url).hostname == domain:
                all_pages.add(absolute_url)

    def crawl_all_pages(url):
        # Tüm sayfalarda dolaşma
        try:
            crawl_page(url)
            for page in list(all_pages):
                crawl_all_pages(page)
        except Exception as e:
            print(f"Hata: {e} - {url}")

    crawl_all_pages(base_url)

    return all_pages

# Kullanıcıdan domaini al
domain = input("Lütfen domaini girin (örneğin: example.com): ")
all_pages = get_all_pages(domain)

# Bulunan sayfaları yazdırma
for page in all_pages:
    print(page)

