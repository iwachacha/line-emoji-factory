# release packaging ルール

このファイルは、LINE申請用 package を作るときの判断基準の正本である。

## package 前提
- release spec と final assets が対応している。
- submission metadata が schema と metadata validator に通る。
- content images が asset validator に通る。
- submission checklist と submission audit report が更新されている。

## 必須構造
```text
releases/<release-id>/submission/
  metadata.yaml
  images/
  package.zip
  package-checksums.txt
  submission-checklist.md
  submission-audit-report.md
```

## Hard NG
- final asset が release spec の count と一致しない。
- content image が `180 x 180 px` ではない。
- metadata が文字数・copyright 条件を満たさない。
- `package.zip` が 20MB を超える。
- 審査前 checklist の blocking 項目が未解決。

## 完了条件
- `tools/package-release.py` が成功する。
- `package.zip` と checksum が生成される。
- `release-log.md` に package 作成日と対象 release が残る。
