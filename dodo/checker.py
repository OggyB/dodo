import concurrent.futures
from tqdm import tqdm
from dodo.utils import suppress_whois_logs, check_domain_availability
from importlib.resources import files

suppress_whois_logs()


def load_tlds():
    tlds_file = files("dodo").joinpath("tlds.txt")
    with tlds_file.open("r") as f:
        return sorted(set(t.strip() for t in f if t.strip()))


def check_all_domains(name, tlds):
    domains = [f"{name}.{tld}" for tld in tlds]
    results = []

    def check(domain):
        available, _ = check_domain_availability(domain)
        return domain, available

    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(tlds), 10)) as executor:
        for domain, available in tqdm(executor.map(check, domains), total=len(domains), desc="Progress", colour="cyan"):
            results.append((domain, available))

    return results


def _is_specific_domain(domain_name: str) -> bool:
    if domain_name.startswith("www.") or domain_name.startswith("http://") or domain_name.startswith("https://"):
        return True
    tlds = load_tlds()
    for tld in tlds:
        if domain_name.endswith(tld):
            return True
    return False


def check_specific_domain(domain_name: str) -> tuple[bool, str | None]:
    availability, _ = check_domain_availability(domain_name)
    if availability is None:
        return False, _

    return availability, None
