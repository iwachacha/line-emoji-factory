# [RELEASE_ID] 販売直前パッケージ manifest テンプレート

このテンプレートは、ユーザーが手作業で LINE Creators Market へ登録できる直前状態を残す正本である。
実際の申請操作は行わず、提出に必要な asset、metadata、確認結果をまとめる。

## 1. Meta
- ブランド名:
- release:
- 作成日:
- package type:
- 商品種別: `静止絵文字 / アニメーション絵文字`
- 参照する release spec:
- 参照する fixed IP bible: （固定IPを使う場合のみ）
- 参照する release checklist:
- export-ready directory:
- ZIP package path:

## 2. Asset Inventory
- トークルームタブ画像:
  - file:
  - size:
  - format:
  - transparent:
  - file size:
- コンテンツ画像:
  - expected count:
  - actual count:
  - filename range:
  - missing:
  - extra:

## 3. Per-Asset Check
- ID:
- file:
- 用途:
- size:
- format:
- transparent:
- color mode:
- dpi:
- file size:
- filename rule:
- visual QA:
- IP drift:
- review risk:
- status: `Ready / Revise / Hold`

## 4. Metadata
- クリエイター名:
- 絵文字タイトル:
- 絵文字説明文:
- Copyright:
- サジェスト表示タグ候補:
- 文字数確認:
- 絵文字 / 機種依存文字の混入:
- URL / 告知文言:
- 画像内容との整合:

## 5. Rights / IP
- 完全オリジナル性:
- 権利者:
- 参考元 / 素材:
- 許諾が必要な要素:
- 許諾証跡:
- 固定IPバイブルとの差分: （固定IPを使う場合のみ）
- Hard NG の有無:

## 6. Manual Submission Notes
- 登録時に選ぶ商品種別:
- 登録時に選ぶパッケージタイプ:
- アップロードする asset:
- 手入力する metadata:
- 提出前にユーザーが見る項目:
- 審査提出後に release log へ記録する項目:

## 7. Final Gate
- [ ] 必須画像が揃っている
- [ ] 公式サイズに合っている
- [ ] 形式、透過、容量に問題がない
- [ ] ファイル名が package type に合っている
- [ ] metadata が仕様に収まっている
- [ ] metadata と画像内容が矛盾していない
- [ ] 固定IPの権利と出自が説明できる
- [ ] Hard NG がない
- [ ] blocking Revise がない
- [ ] release log 更新先が決まっている

## 8. Result
- Status: `Ready / Revise / Hold`
- 残る Watch:
- ユーザーへの引き渡しメモ:
- 次に更新するファイル:
