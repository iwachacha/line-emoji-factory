# Codex向け line-emoji-factory 再監査・改善実装計画書

対象リポジトリ: `iwachacha/line-emoji-factory`  
監査対象: 2026-04-26 時点の `main` / latest visible commit `afde130` 系  
作業者想定: Codex / AI coding agent  
目的: 最新改善後の残存欠陥を厳密に潰し、実行可能・検証可能・申請準備可能な factory に戻す。

---

## 0. 監査結論

判定: **Fail / Emergency Repair Required**

最新状態は、設計の方向性自体はかなり良い。  
`tools/`, `schemas/`, `tests/`, `examples/soeshirushi`, `requirements-dev.txt`, GitHub Actions workflow などが追加され、前回計画の多くがファイル構成上は反映されている。

しかし、現状はまだ完了ではない。

主な理由は以下。

```text
Critical:
  - Python / PowerShell / YAML / Markdown の多くが raw 上で1行化されている。
  - Python tools は shebang 行に本体が吸収され、実行しても何もしない可能性が高い。
  - GitHub Actions workflow も1行化されており、CIとして信頼できない。
  - requirements-dev.txt が1行で、pip install が壊れる可能性が高い。
  - AGENTS.md / PROJECT_MAP.md が旧スキル・旧templates・旧workflowを正本として参照し続けている。
  - 旧スキルと新スキルが共存しており、Codex の入口が二重化している。
  - scripts/init-brand-repo.ps1 が旧scaffoldのまま残っている。
  - templates root 直下と templates/repo 以下に同名・旧型の manifest template が共存している。
  - example manifest や review-risk-keywords.yaml が YAML として壊れている可能性が高い。
```

このため、次の作業は新機能追加ではない。  
最優先は **実行可能性の回復、正本ドリフトの除去、CIで再発防止** である。

---

## 1. Codex への絶対指示

### 1.1 最初にやること

Codex は作業開始直後に必ず次を実行すること。

```bash
git status --short
git rev-parse HEAD
git ls-files | sort > /tmp/line-emoji-files.txt
```

主要ファイルの行数を確認する。

```bash
wc -l   README.md   AGENTS.md   PROJECT_MAP.md   requirements-dev.txt   .github/workflows/validate.yml   tools/*.py   tools/*.ps1   scripts/*.ps1   schemas/*.json   rules/*.yaml   examples/soeshirushi/brand-manifest.yaml   tests/*.py
```

次に、現状の壊れ方を確認する。

```bash
head -n 3 tools/validate-assets.py
head -n 3 tools/package-release.py
head -n 3 .github/workflows/validate.yml
head -n 3 requirements-dev.txt
head -n 3 rules/review-risk-keywords.yaml
head -n 3 examples/soeshirushi/brand-manifest.yaml
```

### 1.2 Codex がやってはいけないこと

```text
- CIが通っているように見えるだけで完了扱いしない。
- GitHubのrendered viewだけを見て判断しない。raw file と parser を必ず見る。
- 1行化されたPythonをそのまま黒魔術的に通そうとしない。
- compileall だけでPythonが正常と判断しない。
- AGENTS.md / PROJECT_MAP.md が旧入口を指している状態でスキル再編完了と言わない。
- scripts/init-brand-repo.ps1 を旧実装のまま残さない。
- root templates と templates/repo の同名正本を両方残さない。
- package-release.py のLINE提出用zipに metadata / report / json を混ぜない。
- official LINE guideline にない仕様を推測で固定しない。
```

### 1.3 完了報告で必ず書くこと

Codex は各PRごとに次を報告する。

```markdown
## Summary
- ...

## Changed files
- ...

## Verification
- [x] python -m py_compile ...
- [x] python tools/check-source-integrity.py
- [x] python tools/validate-schemas.py --check-schemas schemas
- [x] pytest
- [x] pwsh ./tools/validate-brand-repo.ps1 tests/fixtures/brand-static-ok

## Known limitations
- ...

## Follow-up
- ...
```

実行できなかった検証は、実行できなかった理由を書く。  
「未確認だが大丈夫そう」は禁止。

---

## 2. 監査根拠

### 2.1 raw file collapse

監査時点の raw では以下が1行化されていた。

```text
tools/validate-assets.py: 1 line
tools/validate-brand-repo.py: 1 line
tools/validate-metadata.py: 1 line
tools/check-project-map-paths.py: 1 line
tools/check-example-drift.py: 1 line
tests/test_validate_assets.py: 1 line
tests/test_package_release.py: 1 line
.github/workflows/validate.yml: 1 line
requirements-dev.txt: 1 line
rules/review-risk-keywords.yaml: 1 line
examples/soeshirushi/brand-manifest.yaml: 1 line
```

特に Python は、次のような形になっていた。

```text
#!/usr/bin/env python from __future__ import annotations import argparse ...
```

この場合、ファイル全体が shebang コメント扱いになり、Pythonとして実行しても本体が動かない可能性が高い。  
`compileall` では検出できない可能性があるため、専用の source integrity check が必要である。

### 2.2 AGENTS / PROJECT_MAP drift

`AGENTS.md` は、まだ次の旧スキルを入口として指している。

```text
skills/line-emoji-producer/SKILL.md
skills/line-emoji-improvement-auditor/SKILL.md
skills/line-emoji-doc-auditor/SKILL.md
skills/line-emoji-factory-evolver/SKILL.md
skills/line-emoji-skill-builder/SKILL.md
```

`PROJECT_MAP.md` も同様に旧スキル、旧templates、旧workflowを正本として扱っている。

これは単なる文書遅れではない。  
Codex が最初に読む正本が古いので、実装が新しくても作業入口が壊れる。

### 2.3 duplicate canonical sources

監査時点では次の重複が残っていた。

```text
skills/line-emoji-router/SKILL.md
skills/line-emoji-producer/SKILL.md

templates/brand-repo-manifest-template.yaml
templates/repo/brand-repo-manifest-template.yaml

tools/init-brand-repo.ps1
scripts/init-brand-repo.ps1
```

これらは全て正本の二重化である。  
残すなら明確な deprecated stub / wrapper にする。  
推奨は、旧正本を削除または最小 wrapper 化すること。

### 2.4 LINE公式仕様との関係

LINE Creators Market の絵文字ガイドラインでは、少なくとも以下が明記されている。

```text
- トークルームタブ画像: 1個、96px × 74px
- 絵文字コンテンツ画像: 8〜40個、180px × 180px
- PNG形式
- 背景透過
- 72dpi以上
- RGB
- 1画像 1MB以下
- ZIP upload は20MB以下
- クリエイター名 50文字以内
- 絵文字タイトル 40文字以内
- 説明文 160文字以内
- コピーライト 50文字以内、英数字のみ
- 全角は2文字カウント
- 絵文字は使えない
- 余白をつけすぎない
- アウトラインは太く濃く
- 表情差を大きく
- 装飾はシンプルに
- 告知表現、単なる企業ロゴ、特定個人向け、LINE以外のサービス名は避ける
```

したがって、この factory の validator / package / metadata / checklist は、これらを壊さないように設計する。

---

## 3. 実装PR分割

以下の順に作業すること。  
PR番号は便宜上のラベルであり、Codex branch / PR title に利用してよい。

```text
PR-A: Emergency source restoration and anti-collapse guard
PR-B: Canonical source cleanup
PR-C: YAML / manifest / requirements repair
PR-D: CI repair and integrity gates
PR-E: Generated brand repo scaffold repair
PR-F: Packaging and validator logic audit
PR-G: Metadata risk system repair
PR-H: Documentation synchronization
PR-I: Optional quality upgrades
```

PR-A〜PR-H を P0 とする。  
PR-I は P1。

---

# PR-A: Emergency source restoration and anti-collapse guard

## 4. 目的

1行化されたソースを実行可能な通常形式へ戻し、再発をCIで止める。

## 4.1 対象

```text
tools/*.py
tests/*.py
tools/*.ps1
scripts/*.ps1
.github/workflows/*.yml
requirements-dev.txt
rules/*.yaml
examples/**/*.yaml
schemas/*.json
README.md
AGENTS.md
PROJECT_MAP.md
docs/*.md
skills/**/SKILL.md
templates/**/*.md
templates/**/*.yaml
rules/*.md
workflows/*.md
```

## 4.2 復旧方針

### 4.2.1 履歴から復元できる場合

まず git history を確認する。

```bash
git log --stat -- tools/validate-assets.py
git log --stat -- .github/workflows/validate.yml
git log --stat -- AGENTS.md PROJECT_MAP.md
```

過去に正常なmulti-line版があるなら、そこから復元してよい。

```bash
git show <good_commit>:tools/validate-assets.py > tools/validate-assets.py
```

### 4.2.2 履歴にも正常版がない場合

Codex が実装内容からmulti-lineへ再構築する。  
ただし、1行化されたPythonをそのまま機械的に改行するだけでは危険である。

Python は以下を満たすこと。

```text
- shebang と import が別行
- 関数定義が別行
- if / for / try / except / with / def / class が適切にindentされる
- 文字列リテラルが途中で壊れない
- python -m py_compile で通る
- 実行時に main() が呼ばれる
```

PowerShell は以下を満たすこと。

```text
- param block が複数行
- function が複数行
- if / foreach がブロックとして読める
- Parser.ParseFile でエラーなし
```

YAML は以下を満たすこと。

```text
- 1 key 1行
- list は `- item`
- nested mapping はindent
- python yaml.safe_load でdict/listになる
```

## 4.3 追加する tool

```text
tools/check-source-integrity.py
```

## 4.4 check-source-integrity.py の仕様

このtoolは、単なるformat checkerではなく「壊れたソースをCIで止める」ためのgateである。

### 検査対象

```text
tools/*.py
tests/*.py
*.md
docs/*.md
rules/*.md
workflows/*.md
skills/**/SKILL.md
templates/**/*.md
templates/**/*.yaml
schemas/*.json
.github/workflows/*.yml
requirements-dev.txt
examples/**/*.yaml
```

### Hard error 条件

```text
- 対象の .py が 5行未満
- 対象の .py が shebang から始まり、2行目が存在しない
- .py の1行目に `from __future__` や `import` が含まれる
- .py 内に `def main` があるべきファイルで main が検出できない
- .yml / .yaml が 2行未満
- requirements-dev.txt が1行で複数packageを含む
- .github/workflows/*.yml が2行未満
- AGENTS.md / PROJECT_MAP.md / README.md が10行未満
- JSON schema が1行のみ
```

JSON schema は1行でもparse可能だが、reviewabilityを重視してmulti-line必須にする。

### 参考実装イメージ

```python
from __future__ import annotations

import ast
import sys
from pathlib import Path

MIN_LINES_BY_SUFFIX = {
    ".py": 5,
    ".yml": 2,
    ".yaml": 2,
    ".json": 2,
    ".md": 3,
}

CRITICAL_MARKDOWN = {
    Path("README.md"): 20,
    Path("AGENTS.md"): 20,
    Path("PROJECT_MAP.md"): 20,
}

def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()

def fail(message: str, errors: list[str]) -> None:
    errors.append(message)

def check_python(path: Path, errors: list[str]) -> None:
    lines = read_lines(path)
    if len(lines) < 5:
        fail(f"{path}: Python file is too short; possible collapsed source", errors)
    if lines and lines[0].startswith("#!") and (" import " in lines[0] or "from __future__" in lines[0]):
        fail(f"{path}: shebang and code appear collapsed on line 1", errors)
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        fail(f"{path}: syntax error: {exc}", errors)
        return
    if path.parent.name == "tools" and path.name.endswith(".py"):
        if not any(isinstance(node, ast.FunctionDef) and node.name == "main" for node in tree.body):
            fail(f"{path}: tool file does not define main()", errors)

def main() -> int:
    errors: list[str] = []
    for path in Path(".").rglob("*"):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if not path.is_file():
            continue
        if path.suffix == ".py":
            check_python(path, errors)
    for path, min_lines in CRITICAL_MARKDOWN.items():
        if path.exists() and len(read_lines(path)) < min_lines:
            fail(f"{path}: too few lines; possible collapsed documentation", errors)
    if Path("requirements-dev.txt").exists():
        lines = read_lines(Path("requirements-dev.txt"))
        if len(lines) < 3 or any(" " in line.strip() for line in lines if line.strip() and not line.startswith("#")):
            fail("requirements-dev.txt: expected one package per line", errors)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("source integrity check passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

## 4.5 受け入れ条件

```bash
python tools/check-source-integrity.py
python -m py_compile $(git ls-files '*.py')
python -m compileall tools tests
pwsh -NoProfile -Command '
Get-ChildItem -Recurse -Filter *.ps1 | ForEach-Object {
  $tokens = $null
  $errors = $null
  [System.Management.Automation.Language.Parser]::ParseFile($_.FullName, [ref]$tokens, [ref]$errors) | Out-Null
  if ($errors.Count -gt 0) {
    $errors
    exit 1
  }
}
'
python - <<'PY'
import yaml, json
from pathlib import Path

for path in Path(".").rglob("*.yaml"):
    if ".git" in path.parts:
        continue
    yaml.safe_load(path.read_text(encoding="utf-8"))

for path in Path("schemas").glob("*.json"):
    json.loads(path.read_text(encoding="utf-8"))

print("yaml/json parse passed")
PY
```

PR-A は、機能改善ではなく「実行可能な状態へ戻す」だけに集中する。

---

# PR-B: Canonical source cleanup

## 5. 目的

AGENTS / PROJECT_MAP / skills / scripts / templates の正本ドリフトを解消する。

## 5.1 問題

現状は新旧の入口が共存している。

```text
Old:
  line-emoji-producer
  line-emoji-doc-auditor
  line-emoji-improvement-auditor
  line-emoji-factory-evolver
  line-emoji-skill-builder

New:
  line-emoji-router
  line-emoji-market-scout
  line-emoji-brand-distiller
  line-emoji-set-architect
  line-emoji-production-director
  line-emoji-asset-validator
  line-emoji-submission-auditor
  line-emoji-release-packager
  line-emoji-ip-governor
  line-emoji-post-release-analyst
  line-emoji-factory-auditor
```

現状の AGENTS / PROJECT_MAP は旧入口を正本にしている。  
これでは Codex は古い作業フローへ戻る。

## 5.2 実装方針

### 5.2.1 AGENTS.md を新正本に更新

AGENTS.md は以下を入口にする。

```text
通常入口:
  skills/line-emoji-router/SKILL.md

市場観測:
  skills/line-emoji-market-scout/SKILL.md

ブランド核:
  skills/line-emoji-brand-distiller/SKILL.md

セット設計:
  skills/line-emoji-set-architect/SKILL.md

制作進行:
  skills/line-emoji-production-director/SKILL.md

画像検査:
  skills/line-emoji-asset-validator/SKILL.md

申請監査:
  skills/line-emoji-submission-auditor/SKILL.md

release package:
  skills/line-emoji-release-packager/SKILL.md

固定IP:
  skills/line-emoji-ip-governor/SKILL.md

公開後学習:
  skills/line-emoji-post-release-analyst/SKILL.md

factory監査:
  skills/line-emoji-factory-auditor/SKILL.md
```

削除する文言。

```text
- 作業完了は remote push 完了まで含む
```

置き換える。

```text
作業完了は、変更内容、検証結果、未完了項目、必要な記録更新を明示すること。
remote push は権限がある場合のみ行う。
```

### 5.2.2 PROJECT_MAP.md を新構造に更新

PROJECT_MAP.md の正本層は最低限以下にする。

```text
AGENTS.md
PROJECT_MAP.md
docs/
rules/
workflows/
templates/
schemas/
tools/
skills/
examples/
tests/
.github/workflows/
```

旧templates root 直下のパスを参照しない。  
`templates/repo/...`, `templates/brand/...`, `templates/release/...` の階層化後のパスを正本にする。

### 5.2.3 旧スキル削除またはdeprecated stub化

推奨は削除。

削除対象。

```text
skills/line-emoji-producer/
skills/line-emoji-doc-auditor/
skills/line-emoji-improvement-auditor/
skills/line-emoji-factory-evolver/
skills/line-emoji-skill-builder/
```

削除が怖い場合は、各 SKILL.md を10行程度の deprecated stub にする。

```markdown
---
name: line-emoji-producer
description: Deprecated. Use line-emoji-router.
---

# Deprecated

Use `../line-emoji-router/SKILL.md`.
```

ただし、PROJECT_MAP / AGENTS には deprecated skill を正本として載せない。

### 5.2.4 scripts/init-brand-repo.ps1

`tools/init-brand-repo.ps1` を正本とする。

`scripts/init-brand-repo.ps1` は削除するか、薄いwrapperにする。

推奨 wrapper。

```powershell
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $RemainingArgs
)

$tool = Join-Path $PSScriptRoot "..\tools\init-brand-repo.ps1"
& $tool @RemainingArgs
exit $LASTEXITCODE
```

現状の scripts 側旧scaffoldは削除する。

### 5.2.5 root templates の旧正本削除

削除対象。

```text
templates/brand-repo-manifest-template.yaml
templates/brand-repo-blueprint.md
templates/brand-repo-readme-template.md
```

正本は以下。

```text
templates/repo/brand-repo-manifest-template.yaml
templates/repo/brand-repo-blueprint.md
templates/repo/brand-repo-readme-template.md
```

同様に root 直下の旧 prompt / QA / release template が残っていれば、階層化先へ一本化する。

## 5.3 追加する tool

```text
tools/check-canonical-drift.py
```

### 仕様

以下を hard error にする。

```text
- AGENTS.md が旧スキル名を含む
- PROJECT_MAP.md が旧スキル名を含む
- PROJECT_MAP.md が templates/brand-repo-manifest-template.yaml を含む
- scripts/init-brand-repo.ps1 が旧実装を含む
- root templates に旧正本ファイルが存在する
- skills/line-emoji-producer/SKILL.md が存在し、Deprecated と書かれていない
```

## 5.4 受け入れ条件

```bash
python tools/check-canonical-drift.py
python tools/check-project-map-paths.py
grep -R "line-emoji-producer" AGENTS.md PROJECT_MAP.md && exit 1 || true
grep -R "templates/brand-repo-manifest-template.yaml" AGENTS.md PROJECT_MAP.md && exit 1 || true
```

---

# PR-C: YAML / manifest / requirements repair

## 6. 目的

壊れている可能性のある YAML / requirements / manifest を実際にparse可能にする。

## 6.1 requirements-dev.txt

現状は以下のような1行。

```text
jsonschema pillow pytest pyyaml
```

修正。

```text
jsonschema
pillow
pytest
PyYAML
```

必要に応じて追加。

```text
ruff
```

ただし、追加したらCIでも使う。

## 6.2 review-risk-keywords.yaml

現状は `keywords: - campaign ...` のような1行で、YAMLとして壊れている可能性が高い。

修正方針。

```yaml
hard_ng:
  external_services:
    - Discord
    - Slack
    - WhatsApp
    - Telegram
    - Messenger
    - Facebook
    - Instagram
    - TikTok
    - YouTube
    - Twitter
    - X

review:
  promotion:
    - 発売
    - 新発売
    - 予約
    - セール
    - キャンペーン
    - 期間限定
    - 無料
    - プレゼント
    - 割引
    - campaign
    - discount
    - free
    - giveaway
    - sale

  personal_targeting:
    - 専用
    - さんへ
    - ちゃんへ
    - くんへ
```

`validate-metadata.py` 側もこの構造に対応させる。  
後方互換として `keywords: [...]` も読めるようにしてよい。

## 6.3 examples/soeshirushi/brand-manifest.yaml

multi-line YAMLへ復元する。

必ず次でparseできること。

```bash
python - <<'PY'
from pathlib import Path
import yaml
data = yaml.safe_load(Path("examples/soeshirushi/brand-manifest.yaml").read_text(encoding="utf-8"))
assert isinstance(data, dict)
assert data["schema_version"] == "1.0"
assert data["releases"][0]["id"] == "release-001"
print("example manifest parse passed")
PY
```

## 6.4 schemas/*.json

JSON schema は parse可能でも、1行はレビュー不能なので整形する。

```bash
for f in schemas/*.json; do
  python -m json.tool "$f" > "$f.tmp" && mv "$f.tmp" "$f"
done
```

## 6.5 受け入れ条件

```bash
python -m pip install -r requirements-dev.txt
python - <<'PY'
from pathlib import Path
import yaml, json

for path in Path(".").rglob("*.yaml"):
    if ".git" not in path.parts:
        yaml.safe_load(path.read_text(encoding="utf-8"))

for path in Path("schemas").glob("*.json"):
    json.loads(path.read_text(encoding="utf-8"))

print("all YAML and JSON parse")
PY
python tools/validate-schemas.py --check-schemas schemas
```

---

# PR-D: CI repair and integrity gates

## 7. 目的

CI を本当に gate として機能させる。

## 7.1 現状問題

`.github/workflows/validate.yml` が1行化されており、workflow として信用できない。  
また、`compileall` だけでは collapsed Python を検出できない。

## 7.2 修正後 workflow

最低限の構成。

```yaml
name: validate

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install validation dependencies
        run: python -m pip install -r requirements-dev.txt

      - name: Source integrity
        run: python tools/check-source-integrity.py

      - name: Canonical drift
        run: python tools/check-canonical-drift.py

      - name: Compile Python
        run: python -m py_compile $(git ls-files '*.py')

      - name: Check schema files
        run: python tools/validate-schemas.py --check-schemas schemas

      - name: Check YAML and JSON parse
        run: python tools/check-data-files.py

      - name: Check project map paths
        run: python tools/check-project-map-paths.py

      - name: Check example drift
        run: python tools/check-example-drift.py examples/soeshirushi

      - name: Check PowerShell syntax
        shell: pwsh
        run: |
          Get-ChildItem -Recurse -Filter *.ps1 | ForEach-Object {
            $tokens = $null
            $errors = $null
            [System.Management.Automation.Language.Parser]::ParseFile($_.FullName, [ref]$tokens, [ref]$errors) | Out-Null
            if ($errors.Count -gt 0) {
              $errors | ForEach-Object {
                Write-Error "$($_.Extent.File):$($_.Extent.StartLineNumber): $($_.Message)"
              }
              exit 1
            }
          }

      - name: Test suite
        run: pytest
```

## 7.3 追加する tool

```text
tools/check-data-files.py
```

### 責務

```text
- 全 *.yaml / *.yml を yaml.safe_load する
- schemas/*.json を json.loads する
- requirements-dev.txt が1依存1行か確認する
- .github/workflows/*.yml が yaml.safe_load できるか確認する
```

## 7.4 CI negative tests

現状の tests は存在するが、1行化により実行不能の可能性が高い。  
復旧後、次の negative tests が実際にfailを検出すること。

```text
- fully transparent image
- wrong filename in submission stage
- missing tab image
- invalid metadata length
- emoji in metadata
- bad copyright
- missing required snapshot
- fixed_ip missing IP files
- collapsed source fixture
- old canonical skill reference fixture
```

## 7.5 受け入れ条件

```bash
python tools/check-source-integrity.py
python tools/check-canonical-drift.py
python tools/check-data-files.py
python -m py_compile $(git ls-files '*.py')
pytest
```

---

# PR-E: Generated brand repo scaffold repair

## 8. 目的

`tools/init-brand-repo.ps1` が生成する brand repo を、現行 schema / tools / package pipeline と整合させる。

## 8.1 問題

現状の `tools/init-brand-repo.ps1` は新構造を作ろうとしているが、次の不安が残る。

```text
- 1行化されていて構文信頼性が低い。
- BrandType generic でも ip files を常に生成している。
- review-risk-keywords.yaml を standalone repo にコピーしていない。
- generated repo の validate-metadata.py は rules/review-risk-keywords.yaml を探すが、generated repo に rules/ がない。
- submission/images/.gitkeep を作っているが、package pipeline は submission/line-upload/images を使う。
- sync対象 snapshot と schema snapshots required がズレる可能性がある。
- scripts/init-brand-repo.ps1 が旧構造を作る。
```

## 8.2 修正方針

### 8.2.1 BrandType generic

generic では `brand/ip/` を生成しない。  
ただし、将来的な切替のために `templates/ip/` は factory に残す。

### 8.2.2 BrandType fixed_ip

`-BrandType fixed_ip` のときだけ生成。

```text
brand/ip/ip-style-bible.md
brand/ip/reference-asset-register.md
brand/ip/ip-approval-log.md
brand/ip/character-expression-matrix.md
```

manifest に `ip:` block を入れるのも fixed_ip のときだけ。

テンプレートを分けるか、init script が block を差し込む。

推奨。

```text
templates/repo/brand-repo-manifest-template.yaml
templates/repo/brand-repo-manifest-ip-block-template.yaml
```

### 8.2.3 review-risk-keywords.yaml の扱い

generated standalone repo でも metadata validator が同じリスク語を使えるようにする。

選択肢A: generated repo に `rules/review-risk-keywords.yaml` をコピーする。  
選択肢B: `validate-metadata.py` の探索順を増やす。

推奨はB + A。

探索順。

```text
1. CLI --risk-keywords
2. brand repo rules/review-risk-keywords.yaml
3. brand repo references/shared/review-risk-keywords.yaml
4. factory root rules/review-risk-keywords.yaml
5. built-in default
```

generated repo には以下をコピーする。

```text
references/shared/review-risk-keywords.yaml
```

### 8.2.4 submission output directories

scaffold は以下を作る。

```text
releases/release-001/submission/
releases/release-001/submission/line-upload/
releases/release-001/submission/internal-archive/
```

ただし `line-upload/images` は package-release が生成してもよい。  
`.gitkeep` は作るなら正しい場所に置く。

```text
releases/release-001/submission/line-upload/images/.gitkeep
```

古い `submission/images/.gitkeep` は作らない。

## 8.3 受け入れ条件

```bash
tmpdir="$(mktemp -d)"
pwsh ./tools/init-brand-repo.ps1   -BrandSlug "smoke-brand"   -BrandName "Smoke Brand"   -Destination "$tmpdir/smoke-brand"   -InitialSetCount 8   -BrandType generic

python tools/validate-brand-repo.py "$tmpdir/smoke-brand"
test ! -d "$tmpdir/smoke-brand/brand/ip"

tmpdir2="$(mktemp -d)"
pwsh ./tools/init-brand-repo.ps1   -BrandSlug "ip-brand"   -BrandName "IP Brand"   -Destination "$tmpdir2/ip-brand"   -InitialSetCount 8   -BrandType fixed_ip

python tools/validate-brand-repo.py "$tmpdir2/ip-brand"
test -f "$tmpdir2/ip-brand/brand/ip/ip-style-bible.md"
```

---

# PR-F: Packaging and validator logic audit

## 9. 目的

ソース復旧後、package / validator の実ロジックを再監査し、実申請事故を防ぐ。

## 9.1 package-release.py の修正

### 9.1.1 release-specific metadata を優先

現状ロジックは top-level `manifest.submission.metadata_path` を優先している可能性がある。  
multi-release では危険。

優先順位を固定する。

```text
1. manifest.releases[].submission / metadata.yaml
2. releases/<release_id>/submission/metadata.yaml
3. manifest.submission.metadata_path
```

ただし、3 は active_release と一致するときだけ許可する。

疑似実装。

```python
def resolve_metadata_path(brand_repo: Path, manifest: dict, release_info: dict, release_id: str) -> Path:
    release_submission = release_info.get("submission")
    if release_submission:
        path = brand_repo / release_submission / "metadata.yaml"
        if path.exists():
            return path

    path = brand_repo / "releases" / release_id / "submission" / "metadata.yaml"
    if path.exists():
        return path

    active = manifest.get("production", {}).get("active_release")
    fallback = manifest.get("submission", {}).get("metadata_path")
    if fallback and active == release_id:
        return brand_repo / fallback

    return path
```

### 9.1.2 targetごとの挙動

```text
--target line-upload:
  - line-upload/images をclean
  - images.zipを作る
  - internal-archiveは触らない

--target internal-archive:
  - 既存の line-upload/images.zip が必要
  - なければ error
  - package.zipを作る

--target both:
  - line-upload と internal-archive を両方作る
```

### 9.1.3 ZIP検証

`images.zip` は画像のみ。

検査。

```text
- metadata.yaml が入っていない
- asset-map.json が入っていない
- package-report.md が入っていない
- tab.png が入っている
- 001.png ... expected_count.png が入っている
- zip total <= 20MB
```

### 9.1.4 internal archive size

LINE公式の20MB制限は upload ZIP に対する制限である。  
internal archive は内部保管用なので、20MBでHard NGにする必要はない。  
警告にするか、別制限にする。

```text
line-upload/images.zip > 20MB: Hard error
internal-archive/package.zip > 20MB: Warning or configurable
```

## 9.2 validate-assets.py の修正

### 9.2.1 fully transparent はHard error

維持。

### 9.2.2 nearly empty / excessive margin

まだ不足している場合は追加。

```text
visible alpha bbox area < 15%: Hard error
visible alpha bbox area < 35%: Warning
any transparent margin > 35%: Warning
```

ただし、テキスト絵文字など例外があるため、最初は warning でもよい。

### 9.2.3 contact sheet

contact sheet 出力は維持。  
CI では出力ファイル存在とサイズを確認する。

### 9.2.4 APNG validation

APNG対応が入っている場合でも、Pillowのメタデータ解釈は要検証。

追加 fixture。

```text
animation-ok
animation-static-file
animation-too-few-frames
animation-too-many-frames
animation-too-long
animation-loop-zero
animation-too-large
animation-no-alpha
```

loop 0 の意味が無限再生として解釈される場合、LINE仕様の1〜4ループと合うかを確認し、baselineに記録する。

### 9.2.5 filename rule

LINE公式は「ファイル名には文字に対応したナンバー」としており、詳細はパッケージタイプ別で変わる。  
現在の `001.png ...` は静止画emoji packageの想定としてよいが、公式の「パッケージタイプとファイル名」を再確認し、`rules/line-platform-baseline.md` に根拠を追記する。

## 9.3 受け入れ条件

```bash
pytest tests/test_validate_assets.py
pytest tests/test_package_release.py
python tools/package-release.py tests/fixtures/brand-static-ok --release-id release-001 --target both --clean
python tools/validate-assets.py   tests/fixtures/brand-static-ok/releases/release-001/submission/line-upload/images   --expected-count 8   --stage submission   --asset-type static   --zip tests/fixtures/brand-static-ok/releases/release-001/submission/line-upload/images.zip
```

---

# PR-G: Metadata risk system repair

## 10. 目的

metadata validator と review-risk keywords の責務を分ける。

## 10.1 現状問題

`validate-metadata.py` は `keywords:` flat list を読む設計に見える。  
しかし改善計画上は hard_ng / review を分けるべきだった。

## 10.2 新しい risk keyword schema

```yaml
hard_ng:
  external_services:
    - Discord
    - Slack
    - WhatsApp
    - Telegram
    - Messenger
    - Instagram
    - TikTok
    - YouTube
    - Twitter
    - X

review:
  promotion:
    - 発売
    - 新発売
    - 予約
    - セール
    - キャンペーン
    - 期間限定
    - 無料
    - プレゼント
    - 割引
    - campaign
    - discount
    - free
    - giveaway
    - sale

  personal_targeting:
    - 専用
    - さんへ
    - ちゃんへ
    - くんへ

  corporate_logo_like:
    - ロゴ
    - 公式
```

## 10.3 validate-metadata.py の挙動

```text
Hard error:
  - length violation
  - emoji included
  - invalid copyright
  - hard_ng keyword

Warning:
  - review keyword
```

CLI。

```bash
python tools/validate-metadata.py metadata.yaml
python tools/validate-metadata.py metadata.yaml --warnings-as-errors
python tools/validate-metadata.py metadata.yaml --risk-keywords rules/review-risk-keywords.yaml
```

## 10.4 受け入れ条件

```bash
pytest tests/test_validate_metadata.py
python tools/validate-metadata.py tests/fixtures/metadata/valid.yaml
python tools/validate-metadata.py tests/fixtures/metadata/emoji-in-title.yaml && exit 1 || true
python tools/validate-metadata.py tests/fixtures/metadata/external-service.yaml && exit 1 || true
python tools/validate-metadata.py tests/fixtures/metadata/promotion-warning.yaml
python tools/validate-metadata.py tests/fixtures/metadata/promotion-warning.yaml --warnings-as-errors && exit 1 || true
```

---

# PR-H: Documentation synchronization

## 11. 目的

README / docs / AGENTS / PROJECT_MAP を、実際の構造と一致させる。

## 11.1 README

README は以下を明記する。

```text
- このfactoryが現在正式対応するのは static emoji packaging である。
- APNG validation はあるが、animation release packaging は未実装ならそう書く。
- line-upload/images.zip は画像のみ。
- internal-archive/package.zip は内部保管用。
- Quickstart のコマンドはCIで実行されている。
- examples/soeshirushi は design-stage / standalone generated repo sample であり、production-readyではない。
```

## 11.2 docs/quickstart.md

READMEより詳細にする。

必須セクション。

```text
1. Requirements
2. Create a brand repo
3. Edit brand-manifest.yaml
4. Add tab image
5. Add final content images
6. Validate brand repo
7. Package release
8. Check line-upload ZIP
9. Internal archive
10. Common failures
```

## 11.3 AGENTS.md

旧入口を消す。  
Codex向けに読む順序を明確化する。

```text
1. AGENTS.md
2. PROJECT_MAP.md
3. skills/line-emoji-router/SKILL.md
4. task-specific skill
5. task-specific rules/workflows/templates
6. schemas
7. tools
8. tests
```

## 11.4 PROJECT_MAP.md

以下を正本として載せる。

```text
tools/check-source-integrity.py
tools/check-canonical-drift.py
tools/check-data-files.py
tools/validate-assets.py
tools/validate-metadata.py
tools/package-release.py
tools/validate-brand-repo.py
.github/workflows/validate.yml
```

旧正本への参照を消す。

## 11.5 root の計画書

`codex-line-emoji-factory-improvement-plan.md` がrootに残っている場合は移動する。

推奨。

```text
docs/internal/codex-line-emoji-factory-improvement-plan.md
```

または削除。  
rootにあると README / PROJECT_MAP / 計画書のどれが正本か混乱する。

---

# PR-I: Optional quality upgrades

## 12. 目的

P0完了後に、factoryの実運用品質をさらに上げる。

## 12.1 asset visual quality

追加できる検査。

```text
- alpha bbox area ratio
- excessive margin
- duplicate / near-duplicate hash
- low contrast warning
- low color variety warning
- 32px / 24px preview contact sheet
```

## 12.2 release-002 fixture

multi-release事故を防ぐ。

```text
tests/fixtures/brand-two-releases/
  releases/release-001/submission/metadata.yaml
  releases/release-002/submission/metadata.yaml
```

テスト。

```text
package release-002 を実行したとき、release-002のmetadataを使う。
release-001のmetadataを使ったらfail。
```

## 12.3 fixed_ip fixture

```text
tests/fixtures/brand-fixed-ip-ok/
tests/fixtures/brand-fixed-ip-missing-style-bible/
```

## 12.4 example drift

`check-example-drift.py` の対象を見直す。

現状の standalone tool list に、少なくとも以下を追加する。

```text
tools/validate-brand-repo.py
tools/check-source-integrity.py
tools/check-data-files.py
tools/check-canonical-drift.py
rules/review-risk-keywords.yaml
```

standalone example に本当にtoolsを内包する方針なら、drift checkは完全にする。  
内包しない方針なら、exampleからtools/schemasを外し、factory root toolsを使う例にする。

---

## 13. 最終完了条件

以下を全て満たすまで「完了」と言わない。

```bash
python tools/check-source-integrity.py
python tools/check-canonical-drift.py
python tools/check-data-files.py
python -m py_compile $(git ls-files '*.py')
python -m compileall tools tests
python tools/validate-schemas.py --check-schemas schemas
python tools/check-project-map-paths.py
python tools/check-example-drift.py examples/soeshirushi
pytest
```

PowerShell。

```powershell
Get-ChildItem -Recurse -Filter *.ps1 | ForEach-Object {
  $tokens = $null
  $errors = $null
  [System.Management.Automation.Language.Parser]::ParseFile($_.FullName, [ref]$tokens, [ref]$errors) | Out-Null
  if ($errors.Count -gt 0) {
    $errors
    exit 1
  }
}
```

Scaffold smoke。

```bash
tmpdir="$(mktemp -d)"

pwsh ./tools/init-brand-repo.ps1   -BrandSlug "smoke-brand"   -BrandName "Smoke Brand"   -Destination "$tmpdir/smoke-brand"   -InitialSetCount 8   -BrandType generic

python tools/validate-brand-repo.py "$tmpdir/smoke-brand"
```

Package smoke。

```bash
# add 8 valid 180x180 PNGs and 1 valid 96x74 tab image
python tools/package-release.py "$tmpdir/smoke-brand" --release-id release-001 --target both --clean
python tools/validate-assets.py   "$tmpdir/smoke-brand/releases/release-001/submission/line-upload/images"   --expected-count 8   --stage submission   --asset-type static   --zip "$tmpdir/smoke-brand/releases/release-001/submission/line-upload/images.zip"
```

ZIP content check。

```bash
python - <<'PY'
from pathlib import Path
import zipfile

root = Path("$tmpdir/smoke-brand/releases/release-001/submission")
with zipfile.ZipFile(root / "line-upload/images.zip") as z:
    names = set(z.namelist())
    assert "metadata.yaml" not in names
    assert "asset-map.json" not in names
    assert "package-report.md" not in names
    assert "tab.png" in names
    assert "001.png" in names
    assert "008.png" in names

with zipfile.ZipFile(root / "internal-archive/package.zip") as z:
    names = set(z.namelist())
    assert "metadata.yaml" in names
    assert "asset-map.json" in names
    assert "package-report.md" in names
    assert "line-upload/images.zip" in names

print("zip content check passed")
PY
```

---

## 14. Codex作業キュー

### CFX-EMERGENCY-001: Restore executable source files

```text
Priority: P0
Files:
  tools/*.py
  tests/*.py
  .github/workflows/validate.yml
  requirements-dev.txt
  rules/review-risk-keywords.yaml
  examples/soeshirushi/brand-manifest.yaml

Acceptance:
  python tools/check-source-integrity.py
  python -m py_compile $(git ls-files '*.py')
```

### CFX-EMERGENCY-002: Add source integrity guard

```text
Priority: P0
Files:
  tools/check-source-integrity.py
  .github/workflows/validate.yml

Acceptance:
  collapsed Python fixture fails.
  collapsed workflow fixture fails.
  requirements one-line fixture fails.
```

### CFX-EMERGENCY-003: Remove canonical drift

```text
Priority: P0
Files:
  AGENTS.md
  PROJECT_MAP.md
  skills/
  templates/
  scripts/

Acceptance:
  AGENTS / PROJECT_MAP do not mention old canonical skills.
  old templates are deleted or deprecated.
  scripts/init-brand-repo.ps1 is wrapper or deleted.
```

### CFX-EMERGENCY-004: Repair YAML and requirements

```text
Priority: P0
Files:
  requirements-dev.txt
  rules/review-risk-keywords.yaml
  examples/soeshirushi/brand-manifest.yaml
  templates/repo/brand-repo-manifest-template.yaml

Acceptance:
  python -m pip install -r requirements-dev.txt
  all yaml safe_load passes.
```

### CFX-EMERGENCY-005: Repair CI

```text
Priority: P0
Files:
  .github/workflows/validate.yml
  tools/check-data-files.py
  tools/check-canonical-drift.py

Acceptance:
  CI includes source integrity, canonical drift, data parse, pytest.
```

### CFX-P0-006: Fix generated repo risk keyword behavior

```text
Priority: P0
Files:
  tools/init-brand-repo.ps1
  tools/validate-metadata.py
  tools/check-example-drift.py

Acceptance:
  generated repo can validate metadata with copied or discoverable risk keywords.
```

### CFX-P0-007: Fix release-specific metadata resolution

```text
Priority: P0
Files:
  tools/package-release.py
  tests/test_package_release.py

Acceptance:
  release-002 packaging uses release-002 metadata.
```

### CFX-P0-008: Harden fixed_ip scaffold and validation

```text
Priority: P0
Files:
  tools/init-brand-repo.ps1
  schemas/brand-manifest.schema.json
  tests/test_validate_brand_repo.py

Acceptance:
  generic scaffold does not require IP files.
  fixed_ip scaffold creates IP files.
  fixed_ip missing IP files fails.
```

### CFX-P1-009: Add visual quality warnings

```text
Priority: P1
Files:
  tools/validate-assets.py
  rules/asset-validation-rules.md
  tests/test_validate_assets.py

Acceptance:
  empty / near-empty / excessive-margin images produce error or warning.
  contact sheet is generated.
```

### CFX-P1-010: Update docs

```text
Priority: P1
Files:
  README.md
  docs/quickstart.md
  AGENTS.md
  PROJECT_MAP.md

Acceptance:
  README commands match CI smoke commands.
  docs mention current animation packaging limitation.
```

---

## 15. 最終ゴール

この改善計画が完了した状態は以下。

```text
- raw files が正常なmulti-line sourceになっている。
- Python / PowerShell / YAML / JSON / workflow がparse可能。
- collapsed source がCIで必ずfailする。
- AGENTS.md / PROJECT_MAP.md が新スキル・新toolsを正本として参照する。
- old producer / old auditor / old templates / old script が正本から消える。
- requirements-dev.txt で依存関係をinstallできる。
- generated brand repo が validate-brand-repo.py を通る。
- line-upload/images.zip は画像だけを含む。
- internal archive は metadata / report / asset-map を含む。
- release-002 packaging がrelease-002 metadataを使う。
- static emoji の画像仕様が検査される。
- metadata の文字数、絵文字、copyright、risk keyword が検査される。
- fixed_ip は必要ファイルなしで通らない。
- examples/soeshirushi は design-stage example として正しくdrift checkされる。
```

この状態になって初めて、`line-emoji-factory` は「改善作業が完了した」と言える。
