# CI保守ワークフロー

このファイルは、factory の破損検知をCIへ接続する標準手順を定義する。

## 起動条件
- schema、tool、template、scaffold を変更した。
- generated brand repo の構造を変えた。
- validator の仕様を変えた。

## 使う正本
- schema 契約: `rules/schema-contract-rules.md`
- schema 検証: `workflows/schema-validation-workflow.md`
- workflow: `.github/workflows/validate.yml`

## 標準手順
1. schema 自体の検証を入れる。
2. PowerShell 構文チェックを入れる。
3. scaffold smoke test を入れる。
4. generated brand repo validation を入れる。
5. metadata validation を入れる。
6. asset validator の最小正常系を入れる。
7. `git diff --check` 相当で whitespace 破損を確認する。

## 完了条件
- ローカルでCI相当コマンドが再現できる。
- main に broken scaffold が入らない。
