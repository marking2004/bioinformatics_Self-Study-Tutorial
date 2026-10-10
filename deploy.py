#!/usr/bin/env python3
"""Deploy Hugo public/ to a GitHub repo root via the Contents API.

- Uploads every file under public/ (overwriting existing, creating new).
- Deletes repo files that Hugo no longer produces (preserves PRESERVE set).
- Uses the GitHub Contents API (works where git push is blocked by proxy).
"""
import os, sys, json, base64, time, socket, urllib.request, urllib.error

PAT = os.environ["DEPLOY_PAT"]
REPO = os.environ["DEPLOY_REPO"]            # owner/name
PUBLIC = os.environ.get("DEPLOY_PUBLIC", "public")
BRANCH = os.environ.get("DEPLOY_BRANCH", "main")
DRY = os.environ.get("DEPLOY_DRY", "0") == "1"

PRESERVE = {".gitignore", "README.md"}      # keep these even if not in public/
API = f"https://api.github.com/repos/{REPO}"

def api(method, path, data=None, sha=None, retries=6):
    url = API + path
    headers = {
        "Authorization": f"Bearer {PAT}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "hugo-deploy",
        "Content-Type": "application/json",
    }
    body = None
    if data is not None:
        body = json.dumps(data).encode()
    elif method in ("PUT", "DELETE"):
        body = b""  # placeholder; real payload set by caller
    last = None
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.status, json.loads(r.read().decode() or "{}")
        except urllib.error.HTTPError as e:
            msg = e.read().decode()
            try:
                msg = json.loads(msg).get("message", msg)
            except Exception:
                pass
            return e.code, {"message": msg}
        except (TimeoutError, urllib.error.URLError, socket.timeout) as e:
            last = e
            print(f"  retry {attempt}/{retries} {method} {path}: {e}")
            time.sleep(min(2 ** attempt, 20))
    return 0, {"message": f"timeout after {retries} retries: {last}"}

# 1) detect default branch if not given explicitly
if BRANCH == "main":
    st, info = api("GET", "")
    if st == 200 and info.get("default_branch"):
        BRANCH = info["default_branch"]

# 2) get existing repo file tree (recursive) -> path -> sha
existing = {}
st, tree = api("GET", f"/git/trees/{BRANCH}?recursive=1")
if st != 200:
    print("FAILED to fetch repo tree:", st, tree.get("message"))
    sys.exit(1)
for item in tree.get("tree", []):
    if item["type"] == "blob":
        existing[item["path"]] = item["sha"]

# 3) local public files
local = {}
for root, _, files in os.walk(PUBLIC):
    for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, PUBLIC).replace("\\", "/")
        local[rel] = full

print(f"Branch: {BRANCH}")
print(f"Local files ({len(local)}) | Repo blobs ({len(existing)})")

# 4) plan uploads
uploads = sorted(local.keys())
deletes = sorted(p for p in existing if p not in local and p not in PRESERVE)

print("\n--- UPLOAD ({} files) ---".format(len(uploads)))
for p in uploads:
    mode = "update" if p in existing else "create"
    print(f"  {mode:6} {p}")

print("\n--- DELETE ({} files) ---".format(len(deletes)))
for p in deletes:
    print(f"  del {p}")

if DRY:
    print("\n[DRY RUN] no changes made.")
    sys.exit(0)

# 5) execute uploads
ok = err = 0
for p in uploads:
    with open(local[p], "rb") as fh:
        content = base64.b64encode(fh.read()).decode()
    data = {
        "message": f"deploy: {p}",
        "content": content,
        "branch": BRANCH,
    }
    if p in existing:
        data["sha"] = existing[p]
    st, resp = api("PUT", f"/contents/{p}", data=data)
    if st in (200, 201):
        ok += 1
        print(f"  ok  {p}")
    else:
        err += 1
        print(f"  ERR {p} -> {st} {resp.get('message')}")

# 6) execute deletes
for p in deletes:
    data = {"message": f"remove stale: {p}", "branch": BRANCH, "sha": existing[p]}
    st, resp = api("DELETE", f"/contents/{p}", data=data)
    if st in (200, 204):
        ok += 1
        print(f"  ok  del {p}")
    else:
        err += 1
        print(f"  ERR del {p} -> {st} {resp.get('message')}")

print(f"\nDONE. ok={ok} err={err}")
sys.exit(1 if err else 0)
