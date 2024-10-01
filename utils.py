import os
import requests
import urllib3
import re

PUBLIC_DOMAINS = [
    # Global and generic domains
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com', 'icloud.com', 'live.com',
    'mail.com', 'protonmail.com', 'zoho.com', 'fastmail.com', 'gmx.com', 'yandex.com', 'tutanota.com',
    'inbox.com', 'me.com', 'mail.ru', 'aim.com', 'freenet.de', 'gmx.net', 'hushmail.com', 
    'rediffmail.com', 'mailbox.org',

    # North America
    'yahoo.ca', 'hotmail.ca', 'outlook.ca', 'shaw.ca', 'sympatico.ca', 
    'rogers.com', 'comcast.net',  'bellsouth.net',  'sbcglobal.net',
    'att.net',  'verizon.net',  'charter.net',
    'hotmail.com.mx', 'yahoo.com.mx', 'msn.ca',

    # Europe
    'btinternet.com', 'talktalk.co.uk', 'blueyonder.co.uk',
    'bt.com', 'gmx.co.uk', 'mail.co.uk', 'yahoo.co.uk', 'hotmail.co.uk',
    'tiscali.co.uk', 'virginmedia.com', 'orange.net', 'alice.it', 'libero.it',
    'virgilio.it', 'fastwebnet.it', 'tin.it', 'tiscali.it', 'hotmail.it',
    'yahoo.it', 'telecomitalia.it', 'wanadoo.fr', 'orange.fr', 'yahoo.fr',
    'hotmail.fr', 'sfr.fr', 'free.fr', 'web.de', 'gmx.de',
    't-online.de', 'posteo.de', 'hotmail.de', 'yahoo.de',
    'o2.pl', 'wp.pl', 'onet.pl', 'interia.pl',
    'yahoo.pl', 'hotmail.pl', 't-online.hu', 'freemail.hu',

    # Asia
    'yahoo.co.in', 'rediffmail.com', 'hotmail.co.in',
    'gmail.co.in', 'in.com', 'sify.com',
    'vsnl.net', 'yahoo.co.jp', 'hotmail.co.jp',
    'outlook.co.jp', 'yahoo.com.sg',
    'hotmail.com.sg', 'outlook.com.sg',
    'yahoo.com.tw', 'hotmail.com.tw',
    'qq.com', '163.com', '126.com',
    'sina.com', 'sina.cn',
    'sohu.com', 'hanmail.net',
    'daum.net', 'naver.com',
    'yahoo.co.kr', 'outlook.kr',

    # South America
    'yahoo.com.br', 'hotmail.com.br',
    'uol.com.br', 'bol.com.br',
    'ig.com.br', 'terra.com.br',
    'globo.com', 'globomail.com',
    'zipmail.com.br',
    'oi.com.br',

    # Additional regional domains
    'itelefonica.com.br', 'hotmail.cl', 'yahoo.cl', 'outlook.cl', 'vtr.net',
    'hotmail.com.ar', 'yahoo.com.ar', 'fibertel.com.ar', 'speedy.com.ar', 'prodigy.net.mx',

    # Africa
    'yahoo.co.za', 'webmail.co.za', 'mweb.co.za', 'vodamail.co.za', 'telkomsa.net',

    # Australia and New Zealand
    'hotmail.com.au', 'yahoo.com.au', 'outlook.com.au', 'bigpond.com',
    'telstra.com', 'optusnet.com.au', 'iinet.net.au', 'internode.on.net',
    'hotmail.co.nz', 'yahoo.co.nz', 'xtra.co.nz',

    # Middle East
    'walla.co.il', 'bezeqint.net', 'mailbox.co.il'
]

DISPOSABLE_DOMAIN_SOURCES = [
    'https://github.com/disposable/disposable-email-domains/raw/refs/heads/master/domains.txt',
    'https://raw.githubusercontent.com/wesbos/burner-email-providers/master/emails.txt',
    'https://github.com/Xyborg/disposable-burner-email-providers/raw/refs/heads/master/disposable-domains.txt',
    'https://github.com/Betree/burnex/raw/refs/heads/master/priv/burner-email-providers/emails.txt',
    'https://github.com/FGRibreau/mailchecker/raw/refs/heads/master/list.txt',
    'https://github.com/disposable-email-domains/disposable-email-domains/raw/refs/heads/main/disposable_email_blocklist.conf',
    'https://raw.githubusercontent.com/beeyev/disposable-email-filter-php/refs/heads/master/src/DisposableEmailDomains/DisposableEmailDomainsList.php.data',
    'https://github.com/7c/fakefilter/raw/refs/heads/main/txt/data.txt',
    'https://www.stopforumspam.com/downloads/toxic_domains_whole.txt'
]

def find_domains(text):
    return re.findall(r'\b(?:[\w-]+\.)+\w{2,}\b', text)

def disposable_domain_scrapper():
    DOMAINS = []
    for src in DISPOSABLE_DOMAIN_SOURCES:
        try: 
            resp = requests.get(src, verify=False)
            if not resp.status_code==200:
                continue
            DOMAINS = DOMAINS + find_domains(resp.text)
        except Exception as e:
            print(e)
    return list(set(DOMAINS))

class EmailSuggest:
    def __init__(self, domains=None, second_level_domains=None, top_level_domains=None):
        self.domains = domains or [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'live.com',
            'msn.com', 'bell.net', 'comcast.net', 'aol.com', 'gmx.com',
            'icloud.com', 'qq.com', 'mail.com', 'yandex.com', 'sbcglobal.net',
            'verizon.net', 'rocketmail.com', 'earthlink.net', 'shaw.ca',
            'telus.net', 'optusnet.com.au', 'att.net', 'xtra.co.nz', 'web.de'
        ]
        self.second_level_domains = second_level_domains or [
            "yahoo", "hotmail", "mail", "live", "outlook", "gmx"
        ]
        self.top_level_domains = top_level_domains or [
            "com", "com.au", "com.tw", "ca", "co.nz", "co.uk", "de", "fr", "it",
            "ru", "net", "org", "edu", "gov", "jp", "nl", "kr", "se", "eu",
            "ie", "co.il", "us", "at", "be", "dk", "hk", "es", "gr", "ch",
            "no", "cz", "in", "net", "net.au", "info", "biz", "mil",
            "co.jp", "sg", "hu", "uk"
        ]
        self.domain_threshold = 2

    def suggest(self, domain):
        domain = domain.lower()

        # Check if the domain is already in the domains list
        if domain in self.domains:
            return None

        closest_domain = self.find_closest_domain(domain, self.domains)

        if closest_domain and closest_domain != domain:
            return closest_domain
        
        # If no close domain found, check for possible second-level and top-level suggestions
        domain_parts = domain.split('.')
        if len(domain_parts) < 2:
            return None

        second_level = domain_parts[-2]
        top_level = domain_parts[-1]

        closest_second_level = self.find_closest_domain(second_level, self.second_level_domains)
        closest_top_level = self.find_closest_domain(top_level, self.top_level_domains)

        suggestions = []
        if closest_second_level and closest_second_level != second_level:
            suggestions.append(domain.replace(second_level, closest_second_level))

        if closest_top_level and closest_top_level != top_level:
            suggestions.append(domain.replace(top_level, closest_top_level))

        return suggestions if suggestions else None

    def find_closest_domain(self, domain, domains):
        min_dist = float('inf')
        closest_domain = None

        for d in domains:
            dist = self.sift4_distance(domain, d)
            if dist < min_dist:
                min_dist = dist
                closest_domain = d

        # Ensure that the closest domain is a meaningful suggestion
        return closest_domain if min_dist <= self.domain_threshold and min_dist != 0 else None

    def sift4_distance(self, s1, s2):
        # Implement the sift4 distance calculation here
        l1, l2 = len(s1), len(s2)
        c1, c2 = 0, 0
        lcss = 0
        local_cs = 0
        trans = 0
        offset_arr = []

        while c1 < l1 and c2 < l2:
            if s1[c1] == s2[c2]:
                local_cs += 1
                is_trans = False
                i = 0
                while i < len(offset_arr):
                    ofs = offset_arr[i]
                    if c1 <= ofs[0] or c2 <= ofs[1]:
                        is_trans = abs(c2 - c1) >= abs(ofs[1] - ofs[0])
                        if is_trans:
                            trans += 1
                        else:
                            if not ofs[2]:
                                ofs[2] = True
                                trans += 1
                        break
                    else:
                        if c1 > ofs[1] and c2 > ofs[0]:
                            offset_arr.pop(i)
                        else:
                            i += 1
                offset_arr.append([c1, c2, is_trans])
            else:
                lcss += local_cs
                local_cs = 0
                if c1 != c2:
                    c1 = c2 = min(c1, c2)
                for j in range(5):
                    if c1 + j < l1 and s1[c1 + j] == s2[c2]:
                        c1 += j - 1
                        c2 -= 1
                        break
                    if c2 + j < l2 and s1[c1] == s2[c2 + j]:
                        c1 -= 1
                        c2 += j - 1
                        break
            c1 += 1
            c2 += 1
            if c1 >= l1 or c2 >= l2:
                lcss += local_cs
                local_cs = 0
                c1 = c2 = min(c1, c2)

        lcss += local_cs
        return round(max(l1, l2) - lcss + trans)


class MXRecordFinder:
    def __init__(self):
        pass

    # Get MX records for a domain
    def get_mx(self, domain: str):
        response = requests.get(f"https://dns.google/resolve?name={domain}&type=MX", verify=False).json()
        return [(answer["data"].split()[1].strip('.'), int(answer["data"].split()[0])) 
                for answer in response.get("Answer", []) 
                if answer["data"].strip('.') and answer["data"].split()[1] != "localhost"]

    # Get the best MX record based on priority
    def get_best_mx(self, domain: str):
        mx_records = self.get_mx(domain)
        valid_mx_records = [mx for mx in mx_records if mx[0] and mx[0] != "localhost"]
        best_mx = min(valid_mx_records, key=lambda mx: mx[1], default=None)
        return {"domain": best_mx[0], "priority": best_mx[1]} if best_mx else None

def is_valid_email(email):
    pattern = r'^[a-z0-9_\-\.]+(\+[a-z0-9_\-\.]+)*@[a-z0-9_\-\.]+\.[a-z]{2,6}$'
    return re.match(pattern, email) is not None

