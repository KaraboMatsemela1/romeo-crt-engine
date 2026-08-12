# GitHub Bootstrap

Target repository: `KaraboMatsemela1/romeo-crt-engine`  
Recommended visibility: **Private** while strategy research and any future broker integration remain proprietary.

## One-time creation using GitHub CLI

From the parent directory containing this repository:

```bash
cd romeo-crt-engine
gh auth login
gh repo create KaraboMatsemela1/romeo-crt-engine \
  --private \
  --description "Evidence-driven CRT strategy research, validation and execution engine" \
  --source . \
  --remote origin \
  --push
```

If the empty repository is created through GitHub's web UI instead:

```bash
cd romeo-crt-engine
git remote add origin git@github.com:KaraboMatsemela1/romeo-crt-engine.git
git push -u origin main
```

After the repository exists, connected GitHub tooling can create/update files, branches, issues and pull requests directly.
