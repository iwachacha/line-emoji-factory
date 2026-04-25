# Codex向け line-emoji-factory 改善実装計画書

対象リポジトリ: `iwachacha/line-emoji-factory`  
監査対象コミット: `375e87fa69750687140408cca55a1654cde96191`  
作成日: 2026-04-25  
作業者想定: Codex / AI coding agent  
目的: 監査結果をもとに、実際に安全な PR として実装できる粒度へ分解する。

---

## 0. Codex への最重要指示

この文書は人間向けの提案書ではなく、Codex がそのまま作業計画として実行するための指示書である。

### 0.1 作業方針

Codex は以下を守ること。

```text
- 既存の思想は残す。
- 壊れている構造は壊してよい。
- ただし、壊す場合は必ず migration / README / CI / tests を同時に更新する。
- 1 PR で全てを直そうとしない。
- まず「壊れた package を出さない」ことを最優先する。
- 仕様文書、schema、tools、CI が食い違う状態を残さない。
- 新しい tool は必ず positive test と negative test を持つ。
- examples/soeshirushi を production-ready と偽らない。
```

### 0.2 Codex が最初に行う確認

作業開始時に必ず実行する。

```bash
git status --short
git rev-parse HEAD
find . -maxdepth 3 -type f | sort | sed 's#^\./##' | head -200
```

その後、主要ファイルの行数を確認する。

```bash
wc -l README.md AGENTS.md PROJECT_MAP.md
wc -l tools/*.py tools/*.ps1 scripts/*.ps1 2>/dev/null || true
wc -l schemas/*.json .github/workflows/*.yml
```

監査時点では、raw 上で README、`package-release.py`、`validate-assets.py`、`validate-brand-repo.ps1`、CI yaml が実質1行化されていた。まずこれを通常フォーマットへ戻すこと。

### 0.3 作業してはいけないこと

```text
- LINE提出用ZIPに metadata.yaml や内部reportを混ぜない。
- release-001 を validator の正本として hardcode しない。
- initial_set_count を常に 8 と仮定しない。
- fixed_ip の必須ファイルを「テンプレートがあるだけ」で済ませない。
- 完全透明画像だけで asset validator の品質を pass と見なさない。
- 旧スキルと新スキルを両方 canonical として残さない。
- scripts/ と tools/ の両方に同名の正本 script を持たせない。
- README のコマンド例と実際の tool の挙動を食い違わせない。
- CI が通るだけで実申請可能と書かない。
```

---

## 1. 現状の監査サマリ

### 1.1 良くなった点

今回の改善コミットでは、以下が追加・改善された。

```text
- README
- docs/
- rules/
- workflows/
- skills/
- templates/
- schemas/
- tools/
- CI
- examples/soeshirushi
```

これは大きな進歩である。

特に良い点は以下。

```text
- スキルを実務寄りに増やした。
- asset / metadata / manifest / schema / package の tool を追加した。
- examples/soeshirushi を参照例として整備し始めた。
- LINE仕様 baseline が強化された。
- GitHub Actions に smoke test を入れた。
```

### 1.2 まだ危険な点

現時点で最も危険なのは、**提出用 package が安全ではないこと**である。

監査時点の `package-release.py` は、`production/finals` から `submission/images` へ PNG をコピーし、さらに `metadata.yaml` と images を同じ `package.zip` に入れている。

これは内部保存用 archive と LINE提出用 image ZIP が混ざっている。

また、以下も P0 問題である。

```text
- file name 正規化がない。
- tab image が package の必須要素になっていない。
- animation emoji 用 validator がない。
- validate-brand-repo.ps1 が release-001 hardcode。
- manifest schema が pathMap に寄りすぎて required key が弱い。
- old skills がまだ残っている。
- scripts/init-brand-repo.ps1 と tools/init-brand-repo.ps1 が共存している。
- examples/soeshirushi と sandbox/soeshirushi が共存している。
- templates の root 直下と templates/repo に重複がある。
- CI は smoke test 中心で negative test が足りない。
```

---

## 2. 公式仕様を壊さないための基準

Codex は公式仕様を勝手に推測しないこと。

### 2.1 現在確認済みの公式仕様

LINE Creators Market の絵文字ガイドラインでは、少なくとも以下が必要である。

```text
トークルームタブ画像:
  - 1個
  - 96px × 74px

コンテンツ画像:
  - 絵文字: 8〜40個
  - 180px × 180px

画像:
  - PNG
  - 背景透過
  - 72dpi以上
  - RGB
  - 1画像 1MB以下
  - ZIP upload の場合 20MB以下

テキスト:
  - クリエイター名: 50文字以内
  - 絵文字タイトル: 40文字以内
  - 絵文字説明文: 160文字以内
  - コピーライト: 50文字以内、英数字のみ
  - 全角文字は2文字カウント
  - 絵文字は使えない
```

また、公式ガイドライン上、以下の品質観点も重要である。

```text
- 余白をつけすぎない。
- 小さく表示しても見える。
- アウトラインは太め・濃い色。
- 単体送信でスタンプのようにも使いやすい。
- 表情には大きな差をつける。
- 装飾はシンプルにする。
- 使いやすいものから並べる。
- 日常会話で使いにくいものは避ける。
- 特定個人向け、告知表現、単なる企業ロゴ、他サービス名は避ける。
```

### 2.2 Codex が追加調査すべき公式仕様

ファイル名規則は、公式ページ内の「パッケージタイプとファイル名」リンク先を確認し、`rules/line-platform-baseline.md` と validator に反映すること。

作業前に確認する。

```text
- 静止画絵文字の正式ファイル名規則
- tab image の正式ファイル名
- animation emoji の正式ファイル名規則
- APNG の容量、frame、loop、duration
- デコ文字 package を扱うか、今回 scope out するか
```

今回の P0 scope では、まず `package_type: emoji` の静止画絵文字に限定してよい。デコ文字は明示的に unsupported として fail する。

---

## 3. PR 分割方針

Codex は以下の順番で PR を分けること。

```text
PR-01: Source normalization and legacy cleanup preparation
PR-02: Safe release packaging
PR-03: Manifest-driven validation
PR-04: Asset validator expansion
PR-05: Metadata validator and schema hardening
PR-06: CI negative tests and project map checks
PR-07: Skill / directory canonicalization
PR-08: Docs and quickstart synchronization
```

PR-01〜PR-06 を P0 とする。  
PR-07〜PR-08 は P1 だが、P0 の結果を README に反映するため、PR-08 は早めに行ってよい。

---

# PR-01: Source normalization and legacy cleanup preparation

## 4. 目的

raw 上で主要ファイルが1行化されている状態を直す。

これは diff、review、grep、lint、Codex の後続作業の前提である。

## 4.1 対象ファイル

最低限、以下を通常の複数行へ整形する。

```text
README.md
AGENTS.md
PROJECT_MAP.md
.github/workflows/validate.yml
tools/*.py
tools/*.ps1
scripts/*.ps1
schemas/*.json
templates/**/*.md
templates/**/*.yaml
skills/**/SKILL.md
rules/*.md
workflows/*.md
docs/*.md
examples/soeshirushi/**/*.md
examples/soeshirushi/**/*.yaml
```

## 4.2 実装指示

Codex は内容を大きく変えず、まず整形だけ行う。

```bash
python -m json.tool schemas/brand-manifest.schema.json > /tmp/schema.json
mv /tmp/schema.json schemas/brand-manifest.schema.json
```

JSON schema は全て `python -m json.tool` 相当で複数行化する。

YAML と Markdown は破壊的な自動整形が難しければ手動整形する。

PowerShell は以下を満たすように整形する。

```text
- param block は複数行
- function は複数行
- array は1要素1行
- if / else はブロック構造
```

Python は以下を満たす。

```text
- import は1行ずつ
- 関数定義は複数行
- 1行 100〜120文字程度を目安
- argparse は読みやすく改行
```

## 4.3 受け入れ条件

```bash
python -m compileall tools
python tools/validate-schemas.py --check-schemas schemas
pwsh -NoProfile -Command '
Get-ChildItem -Recurse -Filter *.ps1 | ForEach-Object {
  $tokens = $null
  $errors = $null
  [System.Management.Automation.Language.Parser]::ParseFile($_.FullName, [ref]$tokens, [ref]$errors) | Out-Null
  if ($errors.Count -gt 0) { $errors; exit 1 }
}
'
```

PR-01 では機能変更を最小化する。  
ただし、明らかな構文エラーがあれば修正してよい。

---

# PR-02: Safe release packaging

## 5. 目的

`package-release.py` を安全な申請用 package generator にする。

現在の最大問題は、LINE提出用 image ZIP と内部保存用 archive が混ざっていることである。

## 5.1 最終的な出力構造

`package-release.py` は以下を作る。

```text
releases/release-001/
  submission/
    line-upload/
      images.zip
      images/
        tab.png
        001.png
        002.png
        ...
    internal-archive/
      package.zip
      metadata.yaml
      package-report.md
      asset-map.json
      package-checksums.txt
```

ただし、正式な tab filename が公式仕様で異なる場合は、`tab.png` ではなく公式名に合わせること。  
必ず `rules/line-platform-baseline.md` にその根拠を追記する。

## 5.2 CLI 仕様

`tools/package-release.py` の CLI を次にする。

```bash
python tools/package-release.py BRAND_REPO \
  --release-id release-001 \
  --target both \
  --clean
```

### 引数

```text
BRAND_REPO:
  brand repository root

--release-id:
  default: manifest の active release
  manifest から読めない場合のみ release-001 fallback

--target:
  line-upload | internal-archive | both
  default: both

--clean:
  output directory を作り直す

--expected-count:
  原則 deprecated
  manifest.product.initial_set_count を使う
  指定された場合は manifest と一致しなければ error

--asset-type:
  原則 deprecated
  manifest.product.item_type / animation を使う
```

## 5.3 入力構造

```text
releases/release-001/
  production/
    tab/
      source-tab.png
    finals/
      any-source-name-a.png
      any-source-name-b.png
      ...
  submission/
    metadata.yaml
```

`production/finals` のファイル名は任意でよい。  
`package-release.py` が submission 用に正規化する。

## 5.4 asset-map.json

ファイル名を正規化するとき、必ず mapping を残す。

```json
{
  "release_id": "release-001",
  "content_images": [
    {
      "slot": 1,
      "source": "production/finals/ok.png",
      "submission": "submission/line-upload/images/001.png"
    }
  ],
  "tab_image": {
    "source": "production/tab/source-tab.png",
    "submission": "submission/line-upload/images/tab.png"
  }
}
```

## 5.5 line-upload ZIP のルール

`line-upload/images.zip` は画像だけを含む。

入れてよいもの。

```text
- tab image
- content images
```

入れてはいけないもの。

```text
- metadata.yaml
- package-report.md
- asset-map.json
- checksum
- release-log.md
- internal note
```

## 5.6 internal archive のルール

`internal-archive/package.zip` は保管用なので、以下を含めてよい。

```text
- line-upload/images.zip
- metadata.yaml
- package-report.md
- asset-map.json
- package-checksums.txt
- release spec snapshot
- manifest snapshot
```

## 5.7 stale file 対策

`--clean` 指定時は以下を削除してから作り直す。

```text
submission/line-upload/
submission/internal-archive/
```

`--clean` 未指定で既存ファイルがある場合は error にするか、明示的に上書きする。  
サイレントに古いファイルを混ぜない。

## 5.8 release-log の idempotency

現在の release-log append は、実行するたびに同じ内容が増える危険がある。

修正方針。

```text
- release-log.md に毎回追記しない。
- package-report.md を生成し、release-log には必要なら latest package summary block を置換する。
- 追記する場合は timestamp と checksum を含める。
- CI smoke では release-log が重複しないことを確認する。
```

## 5.9 受け入れ条件

テスト fixture を作る。

```text
tests/fixtures/brand-static-ok/
  brand-manifest.yaml
  releases/release-001/
    production/tab/source-tab.png
    production/finals/a.png ... h.png
    submission/metadata.yaml
```

実行。

```bash
python tools/package-release.py tests/fixtures/brand-static-ok --release-id release-001 --target both --clean
python tools/validate-assets.py tests/fixtures/brand-static-ok/releases/release-001/submission/line-upload/images \
  --expected-count 8 \
  --tab-image tests/fixtures/brand-static-ok/releases/release-001/submission/line-upload/images/tab.png \
  --stage submission \
  --asset-type static
```

確認。

```bash
python - <<'PY'
from pathlib import Path
import zipfile

root = Path("tests/fixtures/brand-static-ok/releases/release-001/submission")
line_zip = root / "line-upload/images.zip"
internal_zip = root / "internal-archive/package.zip"

assert line_zip.exists()
assert internal_zip.exists()

with zipfile.ZipFile(line_zip) as z:
    names = set(z.namelist())
    assert "metadata.yaml" not in names
    assert any(name.endswith("001.png") for name in names)
    assert any("tab" in name.lower() for name in names)

with zipfile.ZipFile(internal_zip) as z:
    names = set(z.namelist())
    assert any(name.endswith("metadata.yaml") for name in names)
    assert any(name.endswith("asset-map.json") for name in names)
PY
```

---

# PR-03: Manifest-driven validation

## 6. 目的

`validate-brand-repo.ps1` から `release-001` hardcode と `expected-count 8` 前提を消す。

## 6.1 現在の問題

監査時点の `validate-brand-repo.ps1` は、以下を hardcode していた。

```text
releases/release-001/release-spec.md
releases/release-001/production-handoff.md
releases/release-001/submission/metadata.yaml
...
```

これは release-002 以降や、manifest-driven repo では壊れる。

## 6.2 実装方針

`validate-brand-repo.ps1` は brand-manifest.yaml を読む。

PowerShell で YAML parse が難しければ、Python helper を追加してよい。

```text
tools/read-manifest.py
tools/validate-brand-repo.py
```

より良い方針は、`validate-brand-repo.ps1` を thin wrapper にし、実体を Python に移すこと。

```text
tools/validate-brand-repo.ps1
  -> python tools/validate-brand-repo.py
```

## 6.3 新しい validator の責務

```text
- brand-manifest.yaml が存在する
- schema validation を通す
- manifest 内の required path が存在する
- snapshots の required key が存在する
- releases[] の各 release を検査する
- --release-id 指定時は対象 release のみ検査する
- fixed_ip の場合は IP files を必須にする
- product.initial_set_count を assets validator に渡す
- product.item_type / animation を assets validator に渡す
```

## 6.4 CLI

```bash
python tools/validate-brand-repo.py BRAND_REPO
python tools/validate-brand-repo.py BRAND_REPO --release-id release-001
pwsh ./tools/validate-brand-repo.ps1 BRAND_REPO
```

PowerShell wrapper は互換維持用。

## 6.5 manifest に active release を追加

`brand-manifest.schema.json` と template に追加する。

```yaml
production:
  active_release: release-001
```

または top-level にする。

```yaml
active_release: release-001
```

推奨は top-level。

```yaml
active_release: release-001
```

理由: validation、packaging、README の標準対象として使うため。

## 6.6 受け入れ条件

次を通す。

```bash
python tools/validate-brand-repo.py tests/fixtures/brand-static-ok
python tools/validate-brand-repo.py tests/fixtures/brand-static-ok --release-id release-001
pwsh ./tools/validate-brand-repo.ps1 tests/fixtures/brand-static-ok
```

次は失敗する。

```bash
python tools/validate-brand-repo.py tests/fixtures/brand-missing-snapshot
python tools/validate-brand-repo.py tests/fixtures/brand-fixed-ip-missing-style-bible
python tools/validate-brand-repo.py tests/fixtures/brand-release-missing-metadata
```

---

# PR-04: Asset validator expansion

## 7. 目的

`validate-assets.py` を、静止画 / アニメーション、production / submission の違いを扱える validator にする。

## 7.1 CLI

```bash
python tools/validate-assets.py IMAGES_DIR \
  --expected-count 8 \
  --tab-image path/to/tab.png \
  --asset-type static \
  --stage submission
```

### 引数

```text
--asset-type:
  static | animation
  default: static

--stage:
  production | submission
  default: production

--expected-count:
  8, 16, 24, 32, 40

--tab-image:
  tab image path

--zip:
  optional zip path

--report:
  optional JSON report output

--preview-contact-sheet:
  optional PNG output for visual review
```

## 7.2 static validation

Hard error。

```text
- directory missing
- expected count mismatch
- file is not PNG
- size is not 180x180
- unsupported color mode
- no alpha / no transparency
- each content image > 1MB
- zip > 20MB
- fully transparent image
- nearly empty image below area threshold
```

Warning。

```text
- dpi missing
- dpi below 72
- excessive transparent margin
- extremely low color variety
- visually near-duplicate image
```

## 7.3 submission stage filename rule

`--stage submission` のときだけ、ファイル名規則を Hard error にする。

```text
001.png
002.png
...
```

tab image filename は公式仕様確認後に実装する。  
未確認なら baseline に TODO を残さず、いったん `--tab-filename-profile` で設定可能にする。

## 7.4 production stage filename rule

`--stage production` では、任意ファイル名を許可する。  
package-release が submission 用に正規化するため。

## 7.5 transparency / empty image

現在の CI は完全透明画像で pass している。これは避ける。

実装例。

```python
def alpha_bbox(image):
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    alpha = image.getchannel("A")
    return alpha.getbbox()

bbox = alpha_bbox(image)
if bbox is None:
    errors.append("fully transparent image")
```

面積率。

```python
visible_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
total_area = image.width * image.height
area_ratio = visible_area / total_area
if area_ratio < 0.15:
    errors.append("visible area too small")
elif area_ratio < 0.35:
    warnings.append("visible area may be too small")
```

threshold は rules に書く。

## 7.6 margin warning

```python
left, top, right, bottom = bbox
margin_left = left / image.width
margin_top = top / image.height
margin_right = (image.width - right) / image.width
margin_bottom = (image.height - bottom) / image.height
```

いずれかが大きすぎる場合 warning。

## 7.7 contact sheet

小サイズ視認性は完全自動判定しにくい。  
最初は contact sheet を出すだけでよい。

```bash
python tools/validate-assets.py ... --preview-contact-sheet report/contact-sheet.png
```

contact sheet には以下を含める。

```text
- original 180px
- 48px preview
- 32px preview
- 24px preview
```

## 7.8 animation validation

P0 では `--asset-type animation` が指定されたら、未対応として fail してよい。

ただし、baseline と README には明記する。

```text
animation emoji validation is planned but not yet implemented.
Do not package animation emoji with current static pipeline.
```

P1 で以下を実装する。

```text
- APNG detection
- max 300KB
- frame count 5〜20
- duration <= 4 sec
- loop count 1〜4
```

## 7.9 受け入れ条件

Positive。

```bash
python tools/validate-assets.py tests/fixtures/assets/static-ok/images \
  --expected-count 8 \
  --tab-image tests/fixtures/assets/static-ok/tab.png \
  --asset-type static \
  --stage submission
```

Negative。

```bash
python tools/validate-assets.py tests/fixtures/assets/wrong-size --expected-count 8 --stage submission
python tools/validate-assets.py tests/fixtures/assets/fully-transparent --expected-count 8 --stage submission
python tools/validate-assets.py tests/fixtures/assets/wrong-filename --expected-count 8 --stage submission
python tools/validate-assets.py tests/fixtures/assets/no-alpha --expected-count 8 --stage submission
```

全て expected failure として CI に入れる。

---

# PR-05: Metadata validator and schema hardening

## 8. 目的

metadata schema と validator を、公式仕様と審査リスクにより近づける。

## 8.1 schema 側で見ること

`schemas/submission-metadata.schema.json` に追加。

```text
- additionalProperties: false
- creator_name minLength
- title minLength
- description minLength
- copyright minLength
- copyright pattern の簡易版
- locale pattern
- suggest_tags maxItems
- suggest_tags item type
```

JSON Schema で全角2カウントは無理に扱わない。  
それは `validate-metadata.py` の責務。

## 8.2 validator 側で見ること

Hard error。

```text
- creator_name > 50 LINE count
- title > 40 LINE count
- description > 160 LINE count
- copyright > 50
- copyright non ASCII / non alnum allowed pattern violation
- emoji included
- missing required field
```

Review warning。

```text
- 告知表現
- 発売 / 新発売 / 予約 / セール / キャンペーン / 期間限定 / 無料 / プレゼント
- 他サービス名
- Discord / Slack / WhatsApp / Telegram / Messenger / Facebook / Instagram / TikTok / YouTube / X
- 個人名らしき表現
- 日付告知らしき表現
- 単なる企業ロゴっぽい title
```

外部サービス名は基本 Hard NG に寄せるが、false positive があり得る場合は severity を設定化する。

## 8.3 forbidden patterns を外部ファイル化

validator に直書きしない。

```text
rules/review-risk-keywords.yaml
```

例。

```yaml
hard_ng:
  external_services:
    - Discord
    - Slack
    - WhatsApp
    - Telegram
    - Messenger

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
```

`validate-metadata.py` はこの YAML を読む。

## 8.4 受け入れ条件

Positive。

```bash
python tools/validate-metadata.py tests/fixtures/metadata/valid.yaml
```

Negative hard error。

```bash
python tools/validate-metadata.py tests/fixtures/metadata/too-long-title.yaml
python tools/validate-metadata.py tests/fixtures/metadata/emoji-in-title.yaml
python tools/validate-metadata.py tests/fixtures/metadata/bad-copyright.yaml
```

Warning expected。

```bash
python tools/validate-metadata.py tests/fixtures/metadata/promotion-warning.yaml --allow-warnings
```

warning を error 扱いにする option も追加する。

```bash
python tools/validate-metadata.py ... --warnings-as-errors
```

---

# PR-06: CI negative tests and project map checks

## 9. 目的

CI を smoke test から破損検知 gate にする。

## 9.1 追加する CI job

```yaml
jobs:
  lint
  schema
  tools
  scaffold
  validators-positive
  validators-negative
  package
  project-map
```

最初は1 job内 step でもよいが、ログを読みやすくする。

## 9.2 追加する checks

```text
- python -m compileall tools
- schema validation
- PowerShell syntax
- markdownlint または markdown syntax check
- yamllint または YAML parse check
- scaffold smoke test
- positive asset validation
- negative asset validation
- positive metadata validation
- negative metadata validation
- package-release safe ZIP check
- PROJECT_MAP path existence check
- README command smoke test
```

## 9.3 check-project-map-paths.py

追加する。

```text
tools/check-project-map-paths.py
```

責務。

```text
- PROJECT_MAP.md 内の backtick path を抽出
- rules/ workflows/ templates/ schemas/ tools/ skills/ docs/ examples/ で始まる path を確認
- 存在しない path があれば fail
- directory path と file path の両方に対応
```

## 9.4 README command smoke test

README の Quickstart が壊れていないことを確認する。

最低限、README に書くコマンドと CI の smoke command を揃える。

`docs/quickstart.md` にも同じコマンドがあるなら、両方を更新する。

## 9.5 受け入れ条件

CI で以下が失敗を検出すること。

```text
- wrong image size
- fully transparent image
- wrong filename in submission stage
- missing tab image
- invalid metadata
- missing snapshot
- fixed_ip missing IP files
- PROJECT_MAP broken path
```

---

# PR-07: Skill / directory canonicalization

## 10. 目的

旧構造と新構造の共存を解消し、Codex や人間が読む正本を迷わないようにする。

## 10.1 現在の問題

監査対象コミットでは、新スキルだけでなく旧スキルも残っていた。

```text
skills/line-emoji-doc-auditor/
skills/line-emoji-factory-evolver/
skills/line-emoji-improvement-auditor/
skills/line-emoji-producer/
skills/line-emoji-skill-builder/
```

新スキルがあるにもかかわらず旧スキルも残ると、router の指示、AGENTS.md、PROJECT_MAP が食い違う。

## 10.2 対応方針

どちらかを選ぶ。

### 推奨: 旧スキルを削除

```text
delete:
  skills/line-emoji-doc-auditor/
  skills/line-emoji-factory-evolver/
  skills/line-emoji-improvement-auditor/
  skills/line-emoji-producer/
  skills/line-emoji-skill-builder/
```

必要な内容は `line-emoji-factory-auditor` と `line-emoji-router` に移す。

### 互換重視: redirect stub にする

削除が怖い場合は、各旧 `SKILL.md` を短い redirect にする。

```markdown
# Deprecated: line-emoji-producer

This skill is deprecated.

Use:
- `line-emoji-router` for entry routing
- `line-emoji-brand-distiller` for brand design
- `line-emoji-set-architect` for release set design
- `line-emoji-production-director` for production handoff
```

ただし、`agents/openai.yaml` も deprecated にするか削除する。

## 10.3 scripts と tools の重複

監査対象コミットには以下が共存していた。

```text
scripts/init-brand-repo.ps1
tools/init-brand-repo.ps1
```

対応方針。

```text
- canonical は tools/init-brand-repo.ps1
- scripts/init-brand-repo.ps1 は削除
```

互換維持が必要なら、scripts 側は wrapper にする。

```powershell
& (Join-Path $PSScriptRoot "..\tools\init-brand-repo.ps1") @args
```

README と docs は `tools/` のみを案内する。

## 10.4 templates の重複

監査対象コミットでは root templates と `templates/repo/` に似たファイルがあった。

```text
templates/brand-repo-blueprint.md
templates/brand-repo-manifest-template.yaml
templates/brand-repo-readme-template.md
templates/repo/brand-repo-blueprint.md
templates/repo/brand-repo-manifest-template.yaml
templates/repo/brand-repo-readme-template.md
```

対応方針。

```text
- canonical は templates/repo/
- root 直下の重複は削除
```

## 10.5 sandbox/soeshirushi の重複

監査対象コミットでは以下が共存していた。

```text
examples/soeshirushi/
sandbox/soeshirushi/
```

対応方針。

```text
- canonical は examples/soeshirushi/
- sandbox/soeshirushi は削除
```

もし履歴として残すなら、`sandbox/soeshirushi/README.md` だけ残し、以下を書いて中身は消す。

```markdown
# Deprecated

Moved to `examples/soeshirushi`.
```

## 10.6 受け入れ条件

```bash
test ! -d skills/line-emoji-producer || grep -q "Deprecated" skills/line-emoji-producer/SKILL.md
test -f tools/init-brand-repo.ps1
test ! -f scripts/init-brand-repo.ps1 || grep -q "tools" scripts/init-brand-repo.ps1
test -f templates/repo/brand-repo-manifest-template.yaml
test ! -f templates/brand-repo-manifest-template.yaml
test -d examples/soeshirushi
test ! -d sandbox/soeshirushi
python tools/check-project-map-paths.py
```

---

# PR-08: Docs and quickstart synchronization

## 11. 目的

README / docs / AGENTS / PROJECT_MAP を、実際の tool 挙動と一致させる。

## 11.1 README に必ず書くこと

```text
- 必要環境
  - Python 3.12
  - PowerShell 7 目安
  - pip dependencies
- 新規 brand repo 作成
- manifest の initial_set_count 設定
- finals と tab image の配置場所
- package-release の実行
- line-upload ZIP と internal archive の違い
- validate-brand-repo の実行
- fixed_ip の場合に必要な追加ファイル
- examples/soeshirushi は design-stage example であること
```

## 11.2 Quickstart の推奨コマンド

README の Quickstart は最終的にこうする。

```powershell
python -m pip install -r requirements-dev.txt

./tools/init-brand-repo.ps1 `
  -BrandSlug "my-brand" `
  -BrandName "マイブランド" `
  -Destination ".\brands\my-brand" `
  -InitialSetCount 16

./tools/validate-brand-repo.ps1 ".\brands\my-brand"

# final assets を配置
# .\brands\my-brand\releases\release-001\production\tab\source-tab.png
# .\brands\my-brand\releases\release-001\production\finals\*.png

python ./tools/package-release.py ".\brands\my-brand" `
  --release-id release-001 `
  --target both `
  --clean

./tools/validate-brand-repo.ps1 ".\brands\my-brand"
```

`InitialSetCount` は `init-brand-repo.ps1` が対応してから README に載せる。  
まだ未対応なら README に載せない。

## 11.3 docs/quickstart.md

README より詳しい説明を置く。

```text
- generated repo layout
- what to edit first
- where to put images
- how to package
- how to validate
- common failure examples
```

## 11.4 AGENTS.md

Codex / AI agent 向けに、正本の読み順を明確にする。

```text
1. AGENTS.md
2. PROJECT_MAP.md
3. relevant skill/SKILL.md
4. relevant rules/
5. relevant workflows/
6. relevant templates/
7. schemas/
8. tools/
```

また、作業完了条件を修正する。

```text
作業完了:
  - owner file 更新または更新案
  - tests / validation の実行結果
  - 未完了項目の明示
  - push は権限がある場合のみ
```

## 11.5 PROJECT_MAP.md

正本だけを載せる。  
deprecated file は載せない。  
どうしても載せるなら deprecated section を分ける。

---

# 12. 追加の実装詳細

## 12.1 requirements-dev.txt を追加

CI とローカル検証を揃える。

```text
jsonschema
pyyaml
pillow
pytest
```

必要なら以下。

```text
ruff
yamllint
markdownlint-cli
```

Node 依存を避けたいなら Markdown lint は後回しでもよい。  
ただし YAML parse と Python compile は必須。

## 12.2 tests ディレクトリ

追加する。

```text
tests/
  fixtures/
    brand-static-ok/
    brand-missing-snapshot/
    brand-fixed-ip-missing-style-bible/
    brand-release-missing-metadata/
    assets/
      static-ok/
      wrong-size/
      fully-transparent/
      wrong-filename/
      no-alpha/
    metadata/
      valid.yaml
      too-long-title.yaml
      emoji-in-title.yaml
      bad-copyright.yaml
      promotion-warning.yaml
  test_validate_assets.py
  test_validate_metadata.py
  test_package_release.py
  test_validate_brand_repo.py
```

pytest まで入れるのが重ければ、CI shell script でもよい。  
ただし negative test は必ず入れる。

## 12.3 fixture image の作り方

完全透明画像を positive に使わない。

OK画像は、透明背景に不透明な四角や丸を描画する。

```python
from pathlib import Path
from PIL import Image, ImageDraw

root = Path("tests/fixtures/assets/static-ok/images")
root.mkdir(parents=True, exist_ok=True)

for i in range(8):
    img = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((25, 25, 155, 155), fill=(0, 0, 0, 255))
    draw.text((70, 75), str(i + 1), fill=(255, 255, 255, 255))
    img.save(root / f"{i + 1:03}.png", dpi=(72, 72))
```

タブ画像も同様に作る。

```python
img = Image.new("RGBA", (96, 74), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.rectangle((10, 10, 86, 64), fill=(0, 0, 0, 255))
img.save("tests/fixtures/assets/static-ok/tab.png", dpi=(72, 72))
```

## 12.4 manifest schema の厳格化

`pathMap` の乱用をやめる。

### snapshots

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "line_platform_baseline",
    "structure_constraints",
    "emoji_product_rules",
    "review_risk_rules",
    "evaluation_model",
    "quality_control_workflow",
    "usage_validation_workflow",
    "asset_validation_rules",
    "submission_metadata_rules"
  ],
  "properties": {
    "line_platform_baseline": { "type": "string" },
    "structure_constraints": { "type": "string" },
    "emoji_product_rules": { "type": "string" },
    "review_risk_rules": { "type": "string" },
    "evaluation_model": { "type": "string" },
    "quality_control_workflow": { "type": "string" },
    "usage_validation_workflow": { "type": "string" },
    "asset_validation_rules": { "type": "string" },
    "submission_metadata_rules": { "type": "string" }
  }
}
```

### fixed_ip conditional

```json
{
  "if": {
    "properties": {
      "brand": {
        "properties": {
          "type": { "const": "fixed_ip" }
        }
      }
    }
  },
  "then": {
    "required": ["ip"],
    "properties": {
      "ip": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "style_bible",
          "reference_asset_register",
          "approval_log",
          "character_expression_matrix"
        ],
        "properties": {
          "style_bible": { "type": "string" },
          "reference_asset_register": { "type": "string" },
          "approval_log": { "type": "string" },
          "character_expression_matrix": { "type": "string" }
        }
      }
    }
  }
}
```

## 12.5 init-brand-repo.ps1 の改善

`InitialSetCount` を追加する。

```powershell
[ValidateSet(8, 16, 24, 32, 40)]
[int]$InitialSetCount = 8
```

`BrandType` も追加する。

```powershell
[ValidateSet("generic", "fixed_ip", "collaboration")]
[string]$BrandType = "generic"
```

`BrandType fixed_ip` の場合は IP files も生成する。

```text
brand/ip/ip-style-bible.md
brand/ip/reference-asset-register.md
brand/ip/ip-approval-log.md
brand/ip/character-expression-matrix.md
```

## 12.6 sync-shared-snapshots.ps1

snapshots required set が増えたら同期対象も更新する。

required snapshots は1箇所に定義する。  
PowerShell と schema と README で別々に持たない。

候補。

```text
config/required-snapshots.yaml
```

---

# 13. 完了判定

## 13.1 P0 完了条件

P0 は次を全て満たしたら完了。

```bash
python -m compileall tools
python tools/validate-schemas.py --check-schemas schemas
python tools/check-project-map-paths.py
pwsh ./tools/validate-brand-repo.ps1 tests/fixtures/brand-static-ok
python tools/package-release.py tests/fixtures/brand-static-ok --release-id release-001 --target both --clean
pytest
```

さらに以下がすべて成り立つこと。

```text
- line-upload ZIP に metadata.yaml が入らない。
- internal archive には metadata と report が入る。
- content image が submission 用に正規化される。
- tab image が package に含まれる。
- wrong filename は submission stage で fail する。
- fully transparent image は fail する。
- release-001 hardcode が validator から消える。
- fixed_ip manifest では IP files が必須になる。
- old skills は削除または deprecated stub になる。
- scripts/init-brand-repo.ps1 は削除または wrapper になる。
- examples/soeshirushi と sandbox/soeshirushi の重複が消える。
```

## 13.2 P1 完了条件

```text
- animation emoji は明示的に unsupported fail、または専用 validator 実装済み。
- contact sheet preview を生成できる。
- metadata forbidden keywords が外部ファイル化されている。
- README と docs/quickstart のコマンドが実際に通る。
- CI に negative tests がある。
```

## 13.3 P2 完了条件

```text
- animation APNG validation が実装されている。
- post-release metrics schema がある。
- production_profile が manifest と tools に接続されている。
- examples/soeshirushi が standalone generated repo sample として drift check されている。
```

---

# 14. Codex 用作業キュー

以下の順に着手する。

## CFX-P0-001: Normalize source formatting

```text
Files:
  README.md
  tools/*.py
  tools/*.ps1
  schemas/*.json
  .github/workflows/validate.yml

Acceptance:
  wc -l で主要ファイルが1行ではない。
  compile / parse が通る。
```

## CFX-P0-002: Split line-upload ZIP and internal archive

```text
Files:
  tools/package-release.py
  rules/release-packaging-rules.md
  templates/submission/package-report-template.md
  docs/quickstart.md

Acceptance:
  line-upload/images.zip contains only images.
  internal-archive/package.zip contains metadata and reports.
```

## CFX-P0-003: Add tab image to package pipeline

```text
Files:
  tools/package-release.py
  tools/validate-assets.py
  templates/repo/brand-repo-blueprint.md
  tools/init-brand-repo.ps1

Acceptance:
  Missing tab image fails package-release.
```

## CFX-P0-004: Normalize submission filenames

```text
Files:
  tools/package-release.py
  tools/validate-assets.py
  rules/line-platform-baseline.md
  rules/asset-validation-rules.md

Acceptance:
  production finals may have arbitrary names.
  submission images are 001.png...
  asset-map.json records mapping.
```

## CFX-P0-005: Make validate-brand-repo manifest-driven

```text
Files:
  tools/validate-brand-repo.py
  tools/validate-brand-repo.ps1
  schemas/brand-manifest.schema.json
  templates/repo/brand-repo-manifest-template.yaml

Acceptance:
  No release-001 hardcode except fallback / fixture.
  releases[] are read from manifest.
```

## CFX-P0-006: Harden brand manifest schema

```text
Files:
  schemas/brand-manifest.schema.json
  templates/repo/brand-repo-manifest-template.yaml

Acceptance:
  missing required snapshots fail.
  fixed_ip missing IP files fail.
```

## CFX-P0-007: Expand asset validator

```text
Files:
  tools/validate-assets.py
  tests/fixtures/assets/*
  .github/workflows/validate.yml

Acceptance:
  fully transparent images fail.
  wrong filename fails in submission stage.
  wrong filename is allowed in production stage.
```

## CFX-P0-008: Expand metadata validator

```text
Files:
  tools/validate-metadata.py
  rules/review-risk-keywords.yaml
  tests/fixtures/metadata/*
  schemas/submission-metadata.schema.json

Acceptance:
  too long / emoji / bad copyright fail.
  promotion warning is reported.
```

## CFX-P0-009: Add CI negative tests

```text
Files:
  .github/workflows/validate.yml
  tests/fixtures/*
  tests/*.py

Acceptance:
  CI intentionally checks expected failures.
```

## CFX-P0-010: Canonicalize old skills and duplicate directories

```text
Files:
  skills/
  scripts/
  templates/
  sandbox/
  PROJECT_MAP.md
  AGENTS.md

Acceptance:
  no ambiguous canonical duplicate remains.
```

## CFX-P0-011: Sync README and quickstart

```text
Files:
  README.md
  docs/quickstart.md
  AGENTS.md
  PROJECT_MAP.md

Acceptance:
  README commands match tools.
  docs do not claim production-ready where not true.
```

---

# 15. Codex final response format

各 PR または作業単位の最後に、Codex は以下を報告すること。

```markdown
## Summary
- ...

## Changed files
- ...

## Validation
- [x] python -m compileall tools
- [x] python tools/validate-schemas.py --check-schemas schemas
- [x] pytest
- [x] pwsh ./tools/validate-brand-repo.ps1 tests/fixtures/brand-static-ok

## Known limitations
- ...

## Follow-up
- ...
```

検証を実行できなかった場合は、実行できなかった理由を書く。  
「たぶん動く」は禁止。

---

# 16. 最終ゴール

この計画の最終ゴールは、以下の状態である。

```text
- README の Quickstart が実際に通る。
- scaffold した brand repo が manifest-driven に検証される。
- static emoji の画像仕様が最低限自動検査される。
- 完全透明画像や wrong filename が CI で止まる。
- LINE提出用 image ZIP と内部保存 archive が分離される。
- tab image が package pipeline に含まれる。
- metadata の文字数、copyright、絵文字、リスク語が検査される。
- fixed_ip は必要ファイルなしでは validation を通らない。
- old skills / scripts / templates / sandbox duplicate が正本から外れる。
- docs と PROJECT_MAP が現実の構造と一致する。
```

この状態になれば、`line-emoji-factory` は「改善されたドキュメント集」ではなく、少なくとも静止画LINE絵文字については、**作る・検査する・申請用に包む**ところまで安全に支援できる factory になる。
