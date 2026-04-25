# schema 契約ルール

このファイルは、factory の成果物を機械検証できる形へ接続する判断基準の正本である。

## schema を置く対象
- brand repo manifest
- release spec の機械可読版
- submission metadata
- asset validation report
- market observation
- IP style bible
- reference asset register

## schema で止めるもの
- 必須キー不足
- unknown key
- stage / status など enum の不正値
- release id の命名不正
- 参照パスの欠落
- 文字数超過
- unresolved placeholder

## schema に入れないもの
- ブランドの魅力判断
- 商品としての勝ち筋
- 具体会話での勝敗
- 目視の絵柄評価

## tool 接続
- schema 自体の妥当性と data validation は `tools/validate-schemas.py` で行う。
- brand repo 全体の検査は `tools/validate-brand-repo.ps1` で行う。
