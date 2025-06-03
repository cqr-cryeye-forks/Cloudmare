import pathlib
import re

from append_unique_list import append_unique_list
from clean_value import clean_value


def parse_success_lines(filepath: pathlib.Path) -> dict:
    # Container with keys for each record type holding lists of dicts
    results = {}

    success_re = re.compile(r"^\[\+]SUCCESS:\s*(.*)$")
    ip_paren_re = re.compile(r"\(([\d\.]+)\)")
    redirects_re = re.compile(r"Redirects to (http[^\s]+)")
    possible_ip_re = re.compile(r"Possible IP: ([\d\.]+)")
    mx_ns_re = re.compile(r"(MX|NS) Record: ([^\s]+) from: ([^\s]+)")

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        m = success_re.match(line.strip())
        if not m:
            continue

        data_str = m.group(1)
        entry = {}

        # Check MX/NS records
        mxns = mx_ns_re.match(data_str)
        if mxns:
            rec_type, rec_val, from_dom = mxns.groups()
            rec_val = clean_value(rec_val)
            from_dom = clean_value(from_dom)
            if not rec_val or not from_dom:
                continue  # skip empty

            rec_key = "mx_records" if rec_type == "MX" else "ns_records"
            entry = {rec_type.lower() + "_record": rec_val, "from_domain": from_dom}
            append_unique_list(results, rec_key, entry)
            continue  # done with this line

        # Possible IP
        pip = possible_ip_re.search(data_str)
        if pip:
            entry = {"possible_ip": pip.group(1)}
            append_unique_list(results, "possible_ips", entry)
            continue  # done

        # Redirects
        redir = redirects_re.search(data_str)
        if redir:
            host = data_str.split()[0]  # usually first token is host
            entry = {"redirects_to": redir.group(1), "host": host}
            append_unique_list(results, "redirections", entry)
            continue  # done

        # IP in parentheses + host
        ip_match = ip_paren_re.search(data_str)
        if ip_match:
            host = data_str.split()[0]
            entry = {"ip": ip_match.group(1), "host": host}
            append_unique_list(results, "ip_host", entry)
            continue

        # If none matched but line has a token, record it as host only under ip_host for simplicity
        host_candidate = data_str.split()[0]
        if host_candidate:
            entry = {"host": host_candidate}
            append_unique_list(results, "ip_host", entry)

    return results
