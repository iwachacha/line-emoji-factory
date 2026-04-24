# 販売直前パッケージ ワークフロー

このファイルは、完成した絵文字を、ユーザーが手作業で LINE Creators Market へ登録できる
直前の状態まで整える標準手順を定義する。

この workflow は実際の申請操作を代行しない。
目的は、提出者が迷わず手作業できる asset、metadata、確認記録を揃えることである。

## 起動条件
- final asset が揃った。
- `release-checklist` の blocking 問題が解消した。
- ユーザーが手作業で登録・審査提出する前に、販売用パッケージを渡したい。
- 審査差し戻し後に、再提出用パッケージを作り直す。

## 使う正本
- 公式仕様: `rules/line-platform-baseline.md`
- 審査・権利リスク: `rules/review-risk-rules.md`
- 品質管理: `workflows/quality-control-workflow.md`
- release 設計: `templates/release-spec-template.md`
- release checklist: `templates/release-checklist-template.md`
- 販売直前パッケージ manifest: `templates/sales-package-manifest-template.md`
- release log: `templates/release-log-template.md`

## 標準手順
1. 対象 release とパッケージタイプを確認する。
2. 必須画像を揃える。
   - トークルームタブ画像。
   - 選択したパッケージタイプに対応するコンテンツ画像。
3. 各画像の仕様を確認する。
   - サイズ。
   - PNG / APNG。
   - 透過。
   - RGB。
   - 72dpi以上。
   - 1画像あたり容量。
   - ZIP化する場合の容量。
4. 公式のファイル名ルールに沿って、パッケージタイプごとの番号を割り当てる。
5. metadata を整える。
   - クリエイター名。
   - 絵文字タイトル。
   - 説明文。
   - Copyright。
   - サジェスト表示タグ候補。
6. metadata と画像内容の矛盾を確認する。
7. 固定IPバイブルがある場合、IP固定条件と権利メモを確認する。
8. `sales-package-manifest` を埋める。
9. `release-checklist` の販売直前 gate を更新する。
10. 実際の登録、審査提出、リリース操作はユーザーが手作業で行う前提で、手作業メモを残す。
11. 提出後、結果を `release-log` に記録する。

## Export-ready の最低構成
- `production/export-ready/`
  - 公式仕様に合わせた提出候補画像。
  - ファイル名は package type の番号に従う。
  - タブ画像は本文絵文字と混同しない名前で管理する。
- `submissions/sales-package-manifest.md`
  - 画像、metadata、権利、審査、手作業メモの一覧。
- `submissions/release-log.md`
  - 実際の提出、差し戻し、再提出、公開履歴。

## Gate
次のどれかが欠ける場合、販売直前パッケージ完了とは扱わない。
- 必須画像が揃っている。
- サイズ、形式、透過、容量、ファイル名が仕様に合っている。
- タイトル、説明文、クリエイター名、Copyright が仕様に合っている。
- 画像と metadata が矛盾していない。
- 固定IPの権利と出自が説明できる。
- `Hard NG` がない。
- blocking `Revise` が残っていない。
- 手作業で何を登録すればよいかが manifest から分かる。

## 出力原則
- 審査提出前に迷う情報を manifest へ寄せる。
- final asset と export-ready asset を混ぜない。
- 修正後は manifest と release log の両方を更新する。
- 手作業提出後の結果は、次 release の品質学習へ戻す。
