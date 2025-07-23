import whois
import logging
from urllib.parse import urlparse


def suppress_whois_logs():
    logging.getLogger("whois.whois").setLevel(logging.CRITICAL)


def normalize_domain(domain_name: str) -> str:
    if domain_name.startswith("http://") or domain_name.startswith("https://"):
        parsed = urlparse(domain_name)
        domain = parsed.netloc or parsed.path
    else:
        domain = domain_name

    if domain.startswith("www."):
        domain = domain[4:]

    return domain.strip()


def check_domain_availability(domain):
    clean_domain_name = normalize_domain(domain)
    try:
        w = whois.whois(clean_domain_name)
        return not bool(w.domain_name), None
    except Exception as e:
        return None, str(e)