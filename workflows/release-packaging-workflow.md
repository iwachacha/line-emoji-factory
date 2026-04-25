# release packaging ワークフロー

このファイルは、申請用 package を作る標準手順を定義する。

## 起動条件
- final assets が揃った。
- metadata が確定した。
- 申請前監査を通した。

## 使う正本
- package 判断: `rules/release-packaging-rules.md`
- 申請前監査: `workflows/submission-audit-workflow.md`
- tool: `tools/package-release.py`

## 標準手順
1. release spec の count と final assets の数を確認する。
2. final assets を submission images へコピーする。
3. metadata validator を実行する。
4. asset validator を実行する。
5. `package.zip` を作る。
6. checksum を生成する。
7. release log に package 作成を記録する。

## 完了条件
- package zip と checksum が存在する。
- validation が通っている。
- release log が更新されている。
