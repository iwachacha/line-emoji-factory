# factory 改善採用判断 2026-04-25

この文書は、`line-emoji-factory-improvement-proposal.md` を読んだ上で、factory に実際に採用する改善と、今回の実装範囲を固定するための記録である。

## 判断順序
採否は常に `構造 → ブランド → 商品` で見る。

- 構造: factory が壊れず、生成物を検査できるか。
- ブランド: 個別ブランドを増やしても、共通基盤とブランド固有文脈が混線しないか。
- 商品: LINE申請、審査、公開後学習まで商品運用へ落ちるか。

## 採用する中核方針
提案書のうち、次は採用する。

1. `考える factory` から、`作る / 検査する / 提出する / 学ぶ factory` へ拡張する。
2. README を入口として再構築する。
3. `scripts/` 中心の単機能運用をやめ、`tools/` に検証と scaffold を集約する。
4. brand repo manifest、submission metadata、release spec の schema を追加する。
5. 生成された brand repo を CI とローカル tool で検査できるようにする。
6. 画像仕様 validator と metadata validator を追加する。
7. `line-emoji-producer` を実務巨大 skill から router へ置き換える。
8. 監査、改善、doc audit、skill maintenance を `line-emoji-factory-auditor` に統合する。
9. 固定IP運用を、権利侵害回避だけでなく許諾済みIPの制作統制として扱う。
10. 市場調査を、気分ではなく観測証跡として残す。

## 段階化したうえで実装したもの
以下は初回P0では段階化したが、今回の追加実装で canonical path と入口を揃えた。

- `templates/` の完全階層化
  - canonical path を `templates/brand`, `templates/release`, `templates/qa`, `templates/prompts`, `templates/repo`, `templates/market`, `templates/submission`, `templates/ip`, `templates/post-release`, `templates/improvement` へ移した。
- P1 実務 skill 全量追加
  - `market-scout / brand-distiller / set-architect / production-director / release-packager` を追加した。
- release packager
  - `tools/package-release.py`, `rules/release-packaging-rules.md`, `workflows/release-packaging-workflow.md`, `skills/line-emoji-release-packager/SKILL.md` を追加した。
- P2 公開後学習
  - `post-release-analyst`, post-release templates, `workflows/post-release-learning-workflow.md` を追加した。

## 見送る、または修正して採用するもの
- `remote push 完了` を一般完了条件から外す案は、修正採用する。
  - 理由: 権限がない環境で完了不能になる運用は弱い。
  - 新判断: factory 標準では `owner file 更新 / 記録更新 / 検証 / push 状態明記` までを必須にし、push は権限がある場合だけ完了条件に含める。
- 旧 skill を単に残して別名を足す案は採らない。
  - 理由: `同じ概念を別名で増やす` 禁止に反する。
  - 新判断: router と factory-auditor へ入口を寄せる。
- LINE公式仕様の全文再掲を増やす案は採らない。
  - 理由: 公式仕様は `rules/line-platform-baseline.md` が正本であり、skill や workflow に再掲すると drift する。
  - 新判断: validator と schema から正本へ接続する。

## 今回実装する P0
今回の実装範囲は、今後の改善が積み上がるための土台に限定する。

- README quickstart 化
- 採用判断文書の追加
- `tools/` の追加
- `schemas/` の追加
- asset / metadata / brand repo validator の追加
- CI workflow の追加
- router / factory-auditor / P0 実務 skill の追加
- fixed-IP governance の入口追加
- market / submission の最小 template 追加
- factory improvement ledger の更新

## 実装完了後に残す監視点
- release packager は実画像が揃った brand repo で継続検証する。
- post-release 分析は実績データ入力後に factory improvement ledger へ戻す。
- LINE公式仕様は `rules/line-platform-baseline.md` の最終確認日を更新しながら保守する。
