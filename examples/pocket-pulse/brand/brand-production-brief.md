# Pocket Pulse 制作基盤

## 1. 基本情報
- ブランド名: Pocket Pulse
- 参照するブランド設定: `brand/brand-setting.md`
- 判定状態: `Design Ready`
- 商品化の目的: static emoji と static sticker の両方で、同じブランド核を release 単位に変換できることを監査する。
- 商品コンセプト: 低圧の状態共有を、丸い信号体で短く伝える。
- ブランド内での役割: `release-001` は小表示適性、`release-002` は発話ブロック適性を検査する。

## 2. 公式仕様の確定
- 商品種別: `静止絵文字 / 静止スタンプ`
- パッケージタイプ: `emoji / sticker`
- brand として対応可能な item type: `static-emoji`, `static-sticker`
- この release で採る item type: release spec に従う
- 初期セット個数: 8
- 初期セット個数の根拠: 主要状態8語で差分軸を検査でき、重複を避けやすい。
- 必須画像: emoji は content 8枚 + tab。sticker は content 8枚 + main + tab。
- 画像形式: PNG
- 画像サイズ: emoji `180x180`、sticker content 最大 `370x320`、main `240x240`、tab `96x74`
- 容量制約: 1画像1MB以下。emoji ZIP 20MB以下、sticker ZIP 60MB以下。
- 背景透過: 必須
- メタデータ制約: creator 50、title 40、description 160、copyright 50、copyright は英数字のみ。
- 販売運用制約: 審査通過後に販売開始。価格はLINE側の選択肢からrelease前に確認する。

## 3. 固定制作パイプライン
- rough stage の目的: 丸信号体、中央サイン、状態語の対応を見る。
- rough stage で先に固定するもの: 外周線、コア色、中央サイン、上位4語。
- rough board / 全体図の最小構成: 8個一覧、白背景プレビュー、小表示プレビュー。
- rough stage の成功条件: 8個が用途で見分けられ、単なる色違いに見えない。
- ClaudeDesign へ渡す単位: release 全体条件 + 個別アイテム表。
- ClaudeDesign で仕上げる範囲: 線幅、余白、文字位置、サインの視認性。
- 仕上げで変えてよいもの: 色の微調整、影、手の位置。
- 仕上げで変えてはいけないもの: 丸信号体、状態語、中央サインの意味。
- 差し戻しルール: 用途差が色だけになったら release spec へ戻す。

## 4. 表示前提
- 単体送信時の役割: 状態を1反応で返す。
- 文中使用時の役割: emoji では短文の前後に軽く添える。
- 複数絵文字連続時の役割: 2個までの状態遷移に限る。
- スタンプ送信時の発話ブロックとしての役割: 短い一言として会話を前へ進める。
- 余白方針: emoji は余白を少なめ、sticker は10px前後を目安。
- アウトライン方針: 濃紺の太線。
- 装飾方針: 発光点と影だけ。集中線や広告風バッジは禁止。

## 5. セット構成
- 最上段に置く高頻度アイテム: OK, WAIT, DONE, THX
- 基本反応語彙: OK, WAIT, DONE, THX, FYI, SOON, SOS, LATER
- 差分の軸: 状態語、中央サイン、色、目の形。
- 主力枠と補助枠の配分: 8枠すべて主力。補助専用枠なし。
- バリエーション方針: 同一形状を維持しながら、中央サインで差を作る。
- 並び順方針: 高頻度4語を先頭、注意や保留は後半。
- 重複禁止ルール: OK/DONE、WAIT/LATER、FYI/SOON が混ざらないようサインを分ける。

## 6. stage 別制作ルール
- 初期 release spec の作成ルール: 各アイテムに用途、単体意味、item type別役割を書く。
- rough stage で使う視覚 anchor: 丸コア、アンテナ線、中央サイン。
- rough stage で未確定にしてよい点: 影の強さ、手の角度。
- ClaudeDesign に必ず渡す共通条件: 太線、透過、単体意味、広告風NG。
- 1アイテムごとの完成条件: 24px相当でも状態語かサインが読める。
- ファイル命名 / バージョン方針: production は任意名、submission は package tool で正規化。
- release handoff の作成ルール: keep / trim / risk を個別に書く。

## 7. 登録・販売運用
- タブ画像方針: 丸信号体1個に `PP` 相当の短い印。
- タイトル方針: item type に合わせて用途を短く示す。
- 説明文方針: 低圧の状態共有を明示し、広告語を入れない。
- コピーライト表記: `PocketPulse`
- サジェスト表示タグ候補: ok, thanks, wait, done, later
- リリース前チェック: asset validation、metadata validation、package validation、contact sheet。

## 8. 審査注意
- Hard NG 回避項目: 企業ロゴ風、広告文言、外部サービス連想、個人専用名。
- Revise になりやすい項目: 淡色だけ、似た差分、文字が小さすぎる。
- Watch 項目: 通知UI風に見えすぎないか。
- 品質台帳へ残すべき論点: OK/DONE と WAIT/LATER の差分。
- 継続監査で確認する仮説: static sticker でも同じ丸信号体が発話として成立するか。
