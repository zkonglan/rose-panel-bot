"""Overlay deployment settings onto upstream wrangler.toml -> wrangler.deploy.toml."""
import re
import sys

src = sys.argv[1] if len(sys.argv) > 1 else "wrangler.toml"
dst = sys.argv[2] if len(sys.argv) > 2 else "wrangler.deploy.toml"

import os

# Private values come from GitHub Actions secrets (never commit them to the public repo).
KV_ID = os.environ.get("KV_ID", "").strip()
ADMIN_IDS = os.environ.get("ADMIN_IDS", "").strip()
if not re.fullmatch(r"[0-9a-f]{32}", KV_ID):
    sys.exit("KV_ID secret missing or invalid")
if not re.fullmatch(r"\d+(,\d+)*", ADMIN_IDS):
    sys.exit("ADMIN_IDS secret missing or invalid")
VARS = {
    "ADMIN_IDS": ADMIN_IDS,
    "BOT_USERNAME": "Akina_PM_Bot",
    "APP_SHORT_NAME": "panel",
}

t = open(src, encoding="utf-8").read()

# worker name / domain
t = re.sub(r'^name\s*=\s*"[^"]*"', 'name = "rose-panel-bot"', t, count=1, flags=re.M)
t = re.sub(r'^(main\s*=.*)$',
           r'\1\nworkers_dev = false\nroutes = [{ pattern = "bot.akina.live", custom_domain = true }]',
           t, count=1, flags=re.M)

# KV id
n = 0
def kv(m):
    global n
    n += 1
    return f'binding = "TOPIC_MAP"\nid = "{KV_ID}"'
t = re.sub(r'binding\s*=\s*"TOPIC_MAP"(\s*\n\s*#?\s*id\s*=\s*"[^"]*")?', kv, t, count=1)
if n != 1:
    sys.exit("TOPIC_MAP KV binding not found in upstream wrangler.toml")

# vars
if not re.search(r'^\[vars\]', t, flags=re.M):
    t += "\n[vars]\n"
for k, v in VARS.items():
    t = re.sub(rf'^{k}\s*=.*\n', '', t, flags=re.M)
    t = re.sub(r'^\[vars\]\s*$', f'[vars]\n{k} = "{v}"', t, count=1, flags=re.M)

if "DEV_PREVIEW" in t and re.search(r'^DEV_PREVIEW\s*=\s*"true"', t, flags=re.M):
    sys.exit("refuse: DEV_PREVIEW=true in upstream config")

open(dst, "w", encoding="utf-8").write(t)
print("wrote", dst)
