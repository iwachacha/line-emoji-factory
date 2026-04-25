# schema 検証ワークフロー

このファイルは、factory の機械可読成果物を schema で検証する標準手順を定義する。

## 起動条件
- brand repo を scaffold した。
- manifest、metadata、release spec の形式を変更した。
- CI で破損検知を行う。
- template から生成した成果物に placeholder や必須項目欠落の疑いがある。

## 使う正本
- schema 契約: `rules/schema-contract-rules.md`
- brand manifest: `schemas/brand-manifest.schema.json`
- submission metadata: `schemas/submission-metadata.schema.json`
- release spec: `schemas/release-spec.schema.json`

## 標準手順
1. 検証対象が factory template か、生成済み brand repo かを分ける。
2. factory template は placeholder を持ってよい。生成済み brand repo は unresolved placeholder を残さない。
3. `tools/validate-schemas.py --check-schemas schemas` で schema 自体を検査する。
4. brand repo では `tools/validate-brand-repo.ps1 <repo>` を実行する。
5. metadata は `tools/validate-metadata.py <metadata.yaml>` で文字数と禁止表現を検査する。
6. 検証失敗時は、schema の問題か、template の問題か、生成 tool の問題かを切り分ける。
7. 生成 tool が原因なら `tools/init-brand-repo.ps1` と関連 template を同時に直す。

## 完了条件
- schema が parse できる。
- 生成 manifest が schema に通る。
- generated brand repo に unresolved placeholder がない。
- CI で同じ検査を再現できる。
