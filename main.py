
import sys, json, time, random, re, threading
from datetime import datetime
from pathlib import Path

import tls_client
from colorama import Fore, Style, init

sys.stdout.reconfigure(encoding="utf-8")
init(autoreset=True)


CONFIG_PATH = Path(__file__).parent / "config.json"

BEARER = ("AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs"
          "%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

POLL_BASE         = 90
POLL_JITTER       = 30
FOLLOW_MEAN       = 8.0
FOLLOW_STD        = 3.0
DRIFT_CHANCE      = 0.15
DRIFT_RANGE       = (25, 90)
FOLLOWS_PER_CYCLE = 5

class L:
    @staticmethod
    def _ts(): return f"\033[90m[{datetime.now().strftime('%H:%M:%S')}]\033[0m"
    @staticmethod
    def ok(m):   print(f"{L._ts()} {Fore.GREEN}[+]{Style.RESET_ALL} {m}")
    @staticmethod
    def warn(m): print(f"{L._ts()} {Fore.YELLOW}[!]{Style.RESET_ALL} {m}")
    @staticmethod
    def err(m):  print(f"{L._ts()} {Fore.RED}[-]{Style.RESET_ALL} {m}")
    @staticmethod
    def info(m): print(f"{L._ts()} {Fore.CYAN}[>]{Style.RESET_ALL} {m}")
    @staticmethod
    def dbg(m):  print(f"    \033[90m{m}\033[0m")
    @staticmethod
    def div():   print(f"\033[90m{'-'*60}\033[0m")

class Human:
    @staticmethod
    def between():
        time.sleep(abs(random.gauss(1.1, 0.4)))

    @staticmethod
    def before_follow():
        d = max(2.0, random.gauss(FOLLOW_MEAN, FOLLOW_STD))
        L.info(f"Thinking {d:.1f}s...")
        time.sleep(d)

    @staticmethod
    def maybe_drift():
        if random.random() < DRIFT_CHANCE:
            d = random.uniform(*DRIFT_RANGE)
            L.warn(f"Break {d:.0f}s...")
            time.sleep(d)

    @staticmethod
    def next_poll():
        w = max(30, POLL_BASE + random.gauss(0, POLL_JITTER))
        L.info(f"Next check in {w:.0f}s")
        time.sleep(w)

def derive_ct0(auth_token: str) -> str:
    L.info("Deriving fresh ct0...")
    s = tls_client.Session(client_identifier="chrome_131",
                            random_tls_extension_order=True)
    s.headers.update({
        "User-Agent": UA,
        "Cookie": f"auth_token={auth_token}",
    })
    r = s.get("https://x.com/home")
    L.dbg(f"x.com/home → {r.status_code}")

    for hk, hv in r.headers.items():
        if hk.lower() == "set-cookie" and "ct0" in hv:
            m = re.search(r"ct0=([^;]+)", hv)
            if m:
                return m.group(1)

    for c in s.cookies:
        if c.name == "ct0":
            return c.value

    return ""

class Client:
    API = "https://api.x.com"

    def __init__(self, auth_token: str, ct0: str):
        self.auth_token = auth_token
        self.ct0        = ct0
        self.sess       = self._build()
        L.info("TLS client ready (chrome_131)")

    def _build(self):
        s = tls_client.Session(client_identifier="chrome_131",
                                random_tls_extension_order=True)
        s.headers.update({
            "User-Agent":                UA,
            "Accept":                    "*/*",
            "Accept-Language":           "en-US,en;q=0.9",
            "Accept-Encoding":           "gzip, deflate, br",
            "Authorization":             f"Bearer {BEARER}",
            "x-csrf-token":              self.ct0,
            "x-twitter-auth-type":       "OAuth2Session",
            "x-twitter-active-user":     "yes",
            "x-twitter-client-language": "en",
            "Cookie":                    f"auth_token={self.auth_token}; ct0={self.ct0}",
            "Referer":                   "https://x.com/",
            "Origin":                    "https://x.com",
            "sec-ch-ua":                 '"Not_A Brand";v="8","Chromium";v="131","Google Chrome";v="131"',
            "sec-ch-ua-mobile":          "?0",
            "sec-ch-ua-platform":        '"Windows"',
            "sec-fetch-dest":            "empty",
            "sec-fetch-mode":            "cors",
            "sec-fetch-site":            "same-site",
        })
        return s

    def _get(self, path, params=None):
        url = self.API + path
        try:
            r = self.sess.get(url, params=params)
            L.dbg(f"GET {path} → {r.status_code}")
            if r.status_code not in (200, 201):
                L.dbg(f"  {r.text[:200]}")
            Human.between()
            return r
        except Exception as e:
            L.err(f"GET {path}: {e}")
            return None

    def _post(self, path, data=None):
        url = self.API + path
        try:
            r = self.sess.post(url, data=data,
                               headers={"Content-Type": "application/x-www-form-urlencoded"})
            L.dbg(f"POST {path} → {r.status_code}")
            if r.status_code not in (200, 201):
                L.dbg(f"  {r.text[:200]}")
            Human.between()
            return r
        except Exception as e:
            L.err(f"POST {path}: {e}")
            return None

    def verify(self) -> bool:
        r = self._get("/1.1/followers/ids.json",
                      {"cursor": "-1", "count": "1", "skip_status": "true"})
        return r is not None and r.status_code == 200

    def get_follower_ids(self) -> set:
        ids, cursor = set(), "-1"
        while True:
            r = self._get("/1.1/followers/ids.json",
                          {"cursor": cursor, "count": "5000", "skip_status": "true"})
            if not r or r.status_code != 200:
                break
            d = r.json()
            ids.update(str(i) for i in d.get("ids", []))
            cursor = str(d.get("next_cursor", 0))
            if cursor == "0":
                break
        L.info(f"Followers: {len(ids)}")
        return ids

    def get_following_ids(self) -> set:
        ids, cursor = set(), "-1"
        while True:
            r = self._get("/1.1/friends/ids.json",
                          {"cursor": cursor, "count": "5000", "skip_status": "true"})
            if not r or r.status_code != 200:
                break
            d = r.json()
            ids.update(str(i) for i in d.get("ids", []))
            cursor = str(d.get("next_cursor", 0))
            if cursor == "0":
                break
        L.info(f"Following: {len(ids)}")
        return ids

    def follow(self, user_id: str) -> bool:
        r = self._post("/1.1/friendships/create.json",
                       {"user_id": user_id, "include_followed_by": "true"})
        if r and r.status_code in (200, 201):
            L.ok(f"Followed @{r.json().get('screen_name', user_id)}")
            return True
        if r and r.status_code == 429:
            L.warn("Rate limited — backing off 15 min...")
            time.sleep(900)
            return False
        L.err(f"Follow {user_id} failed: {r.status_code if r else 'err'}")
        return False

def run(client: Client):
    L.div()
    L.info("Auto follow-back running")
    L.info(f"Poll ~{POLL_BASE}s  |  max {FOLLOWS_PER_CYCLE} follows/cycle")
    L.div()

    done: set = set()
    seed = client.get_following_ids()
    if seed:
        done = seed
        L.info(f"Seeded {len(seed)} already-followed IDs")

    while True:
        try:
            L.div()
            followers = client.get_follower_ids()
            following = client.get_following_ids()
            pending   = list(followers - following - done)

            if not pending:
                L.info("No new followers to follow back")
            else:
                random.shuffle(pending)
                batch = pending[:FOLLOWS_PER_CYCLE]
                if len(pending) > FOLLOWS_PER_CYCLE:
                    L.warn(f"{len(pending)} pending — doing {len(batch)} now")
                for uid in batch:
                    Human.before_follow()
                    Human.maybe_drift()
                    if client.follow(uid):
                        done.add(uid)
        except Exception as e:
            L.err(f"Cycle error: {e}")
        Human.next_poll()

if __name__ == "__main__":
    L.div()
    L.info("x.com Auto Follow-Back Tool")
    L.div()

    if not CONFIG_PATH.exists():
        L.err("config.json not found")
        raise SystemExit(1)

    cfg        = json.loads(CONFIG_PATH.read_text())
    auth_token = cfg.get("auth_token", "").strip()

    if not auth_token:
        L.err("auth_token missing from config.json")
        L.err("")
        L.err("Get it once:")
        L.err("  1. Open Chrome on x.com → F12")
        L.err("  2. Application → Cookies → https://x.com")
        L.err("  3. Copy the 'auth_token' value → paste in config.json")
        raise SystemExit(1)

    L.info(f"auth_token: ...{auth_token[-8:]}")

    ct0 = derive_ct0(auth_token)
    if not ct0:
        L.err("Could not derive ct0 — is auth_token valid?")
        raise SystemExit(1)
    L.ok(f"ct0 derived: {ct0[:16]}...")

    cfg["ct0"] = ct0
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2))

    client = Client(auth_token, ct0)
    if not client.verify():
        L.err("Auth check failed — get a fresh auth_token from Chrome DevTools")
        raise SystemExit(1)
    L.ok("Authenticated!")

    run(client)
