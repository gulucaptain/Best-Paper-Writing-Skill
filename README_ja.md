<div align="center">

# <img src="assets/logo.svg" height="44" align="top" alt="logo"> Best-Paper-Writing-Skill

**最優秀論文の書き方に基づく、高品質な論文ドラフトを生成：アブストラクト、イントロダクション、手法、実験、図表**

🏆 CVPR / ICCV / NeurIPS の受賞論文60本から執筆パターンを抽出。Claude と Codex の両方で使えるスキル

[![project page](https://img.shields.io/badge/Project%20Page-online-3b5bdb?logo=googlechrome&logoColor=white)](https://gulucaptain.github.io/Best-Paper-Writing-Skill/) ![version](https://img.shields.io/badge/version-v1.2-blue) ![papers](https://img.shields.io/badge/papers-60-orange) ![Claude](https://img.shields.io/badge/Claude-Skill-8A63D2) ![Codex](https://img.shields.io/badge/Codex-Skill-10A37F) ![license](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey)

[🌐 プロジェクトページ](https://gulucaptain.github.io/Best-Paper-Writing-Skill/) · [中文](README.md) · [English](README_en.md) · [日本語](README_ja.md) · [論文一覧](PAPER_LIST.md) · [変更履歴](CHANGELOG.md)

</div>

---

## ✨ できること

研究内容を入力（フォームに記入、または完成したアブストラクトを貼り付け）すると、受賞論文のような論証の流れを持つドラフトを生成します。

- 📝 **アブストラクトとイントロダクション**：具体的な先行研究の貢献を認めたうえで、未解決の課題とその原因を明確にし、問題そのものに関する洞察を示す。少数の重要な数値で主張を裏付ける
- 🧩 **手法と実験**：各構成要素を「必要性 → 仕組み → 得られる性質」の順に説明し、各主張に対応するアブレーション実験を設計する
- 🖼️ **図の計画と作成**（v1.1）：各図が裏付ける主張、配置、必要な素材を整理した図の計画表を作成する。論証の流れに応じて Figure 1 の形式を選び、統一された配色とスタイルで模式図や手法の概要図を描く。実験結果が必要な図はプレースホルダーとし、キャプションに計画を記載する。レイアウトとスタイルのルールは受賞論文44本の図の統計分析に基づく
- 🧭 **論文タイプに応じた執筆方針**：8種類の論文（手法の改善、新しい能力、経験則、再検証、メカニズムの分析、理論、データセット、測定）それぞれに適した論証の流れを選ぶ
- ✅ **内蔵チェッカー**：コーパスの統計と照らし合わせ、AI特有の文体、ダッシュの多用、格言めいた表現の詰め込み、根拠のない数値を検出する。`check_figures.py` は図のキャプションの長さと冒頭文、図への参照、ベクター形式の図、未置換のプレースホルダーをチェックする
- 📋 **著者向けレポート `report.md`**：中心的な主張、主張と根拠の対応表、TODO リスト、Limitations 節に記載すべき事項をまとめる
- 🔒 **捏造しない**：与えられていない数値、ベースライン、参考文献はすべて `[TODO]` のまま残す

### なぜ単に AI に論文を書かせるだけではいけないのか？

汎用 AI が生成するドラフトは似通っています。まず一般的な背景を述べ、仕組みの説明を形容詞で済ませ、構成要素を並列に列挙し、何度も文末に「…, making X possible」を付ける。受賞論文の書き方はこれとは異なります。

| 書き方 | 一般的な AI のドラフト | 受賞論文 |
|---|---|---|
| 文末の分詞構文（", making ..."） | 約32%の文 | 約8% |
| 書き出し | 一般的な背景（"has attracted increasing attention"） | 具体的な場面や先行研究 |
| 未解決の課題（ギャップ） | 「既存手法には限界がある」 | どのような条件で失敗し、その理由は何か |
| 構成要素 | A は…、B は…、C は…（並列） | 2番目の要素が1番目の要素で残された問題を解決する |
| 限界（Limitations） | アブストラクトに書かれることが多い | Limitations 節に記載する |

ルールはコーパスを文単位でアノテーションし、統計分析した結果に基づきます。各ルールには下限と上限が設けられているため、ドラフトを単に統計的な平均値へ近づけるわけではありません。

---

## 🚀 2つの使い方

**📝 フォームに記入 / 📄 アブストラクトを貼り付け**　→　🔍 不足情報の補完　→　🧭 論文タイプの判定　→　✍️ 用例を参照して執筆　→　✅ セルフチェック　→　📦 論文ドラフト + `report.md`

### 📝 方法1：フォームに記入する

ブラウザで [`skills/bestpaper-writing/assets/intake_form.html`](skills/bestpaper-writing/assets/intake_form.html) を開いてください（オフラインで利用可能、入力内容の自動保存、JSON のエクスポートと再インポートに対応。フォームの表示言語は中国語です）。必須項目は5つだけです。**詳しい情報を入力するほど、ドラフトの品質が高まります。**

| 区分 | 内容 |
|---|---|
| ⚙️ 基本設定 | 投稿先の会議 / 年 / ページ数（ドロップダウン）、執筆するセクション（チェックボックス） |
| 🔴 必須（5項目） | 研究の主張を一文で説明、タスク、既存手法が失敗する条件、提案手法の構成要素、主要な実験結果 |
| ⭐ 推奨（8項目） | 現時点で最も強力な既存手法、その失敗の原因、中心となる洞察、最も近い先行研究、具体例、効率面での優位性、直感に反する点、研究チーム内でのアイデアの呼び名。不足している場合、スキルが一度まとめて質問する |
| 🟢 任意（折りたたみ） | その他の利点や応用、論文タイプ、対立・トレードオフの種類、副次的な結果、公開予定の成果物、限界、その他の資料、refs.bib |
| 🔵 手法と実験（折りたたみ） | 研究資料をそのまま貼り付けられる入力欄。必要に応じて数式の記号、構成要素、目的関数、データセット、評価指標、比較手法、結果表、アブレーションを個別に入力 |

エクスポートした JSON をエージェントに渡します。

> Best-Paper-Writing-Skill を使い、この入力フォームの JSON に基づいて論文の Title、Abstract、Introduction、Methods、Experiments を執筆してください。

### 📄 方法2：完成したアブストラクトを貼り付ける

スキルはアブストラクトを無条件に書き換えるわけではありません。まず上記と同じ項目に分解し、**記載済みの情報、曖昧な情報、不足している情報**を示します。不足情報について一度まとめて質問したうえで、論文ドラフトを執筆します。さらに、アブストラクトの**修正対照表**（元の文 → 修正後の文 → 修正理由）を提示するため、修正を一つずつ採用するかどうか判断できます。入力された数値と専門用語はそのまま維持し、アブストラクトにない数値、ベースライン、引用文献は [TODO] として残します。

> Best-Paper-Writing-Skill を使い、このアブストラクトに基づいて論文の Title、Abstract、Introduction、Methods、Experiments を執筆してください。

研究内容を自由記述で直接入力することもできます。出力は Markdown 形式、または CVPR の著者向けキットなどの LaTeX テンプレートに直接書き込む形式に対応しています。

---

## 📦 インストール

```bash
git clone https://github.com/gulucaptain/Best-Paper-Writing-Skill.git
cd Best-Paper-Writing-Skill

./install.sh claude     # Claude Code → ~/.claude/skills/
./install.sh codex      # Codex       → ~/.agents/skills/
./install.sh all        # 両方にインストール。--project を付けると現在のプロジェクトにインストール
```

| プラットフォーム | インストール方法 |
|---|---|
| 🟣 **Claude Code** | `./install.sh claude` を実行するか、`skills/bestpaper-writing/` を `~/.claude/skills/` に手動でコピーする |
| 🟣 **Claude.ai / Cowork** | `bestpaper-writing` フォルダを ZIP に圧縮し、Skills ページからアップロードする |
| 🟢 **Codex** | `./install.sh codex` を実行するか、`~/.agents/skills/` に手動でコピーする。`$bestpaper-writing` で明示的に呼び出せる |

両プラットフォームで共通の `SKILL.md` 形式を使用しています。インストール後にスキルが表示されない場合は、エージェントを再起動してください。補助スクリプトの実行には Python 3 が必要です。

---

## 🗂️ ディレクトリ構成

```
Best-Paper-Writing-Skill/
├── README.md / README_en.md / README_ja.md
├── PAPER_LIST.md              # 分析対象の論文60本の一覧
├── data/                      # papers.csv · figure_stats.json · figure1_types.csv
├── template/CVPR2027/         # CVPR 2027 公式 LaTeX テンプレート
├── tools/                     # コーパス中の図の統計分析スクリプト
├── install.sh                 # 一括インストール
└── skills/bestpaper-writing/
    ├── SKILL.md               # エントリーポイント：ワークフローと厳守すべきルール
    ├── references/            # アブストラクト、イントロダクション、手法、実験、図、執筆方針の選択、文体ルール、コーパス統計
    │   └── exemplars/         # 段落・文の用例集
    ├── scripts/               # check_draft.py · check_figures.py · find_exemplars.py · intake_to_brief.py · style_metrics.py
    ├── assets/                # intake_form.html · figures/（TikZ スタイル、ティーザー図・概要図・比較グリッドのテンプレート、matplotlib スタイル）
    ├── evals/                 # ホールドアウトテスト用の事例とブラインド評価基準
    └── agents/openai.yaml     # Codex の UI 設定
```

---

## 📚 コーパス：受賞論文60本

2021年から2025年までの CVPR、ICCV、NeurIPS における Best Paper、Best Student Paper、Honorable Mention の論文が対象です。

| 会議 | 論文数 |
|---|---|
| CVPR | 22 |
| ICCV | 12 |
| NeurIPS | 26 |

論文タイプ別の内訳：手法の改善26本、新しい能力7本、データセット6本、測定5本、メカニズムの分析5本、理論4本、経験則4本、再検証3本。全論文の一覧は [PAPER_LIST.md](PAPER_LIST.md) を参照してください。

> 🔬 **ホールドアウトテストについて**：文体ルールは60本のうち55本を使って策定しました。残りの5本（すべて2024年）は用例集から除外し、評価のみに使用しています。これにより、評価用データに合わせてルールを調整することを避けています。

---

## 📄 著作権とライセンス

- オリジナルのコンテンツ（説明、テンプレート、スクリプト）は [CC BY 4.0](LICENSE) で公開されています。
- `references/exemplars/` に含まれる公開論文からの短い抜粋は、解説・教育を目的として出典を明記したうえで引用しています。著作権は元の論文の著者に帰属します。新しい論文へそのままコピーしないでください。
- 本リポジトリには**論文の PDF や全文は含まれていません**。引用元の論文の著者であり、抜粋の変更や削除を希望される場合は Issue を作成してください。

本ページは本プロジェクトのコントリビューターによる [中国語版 README](README.md) および [英語版 README](README_en.md)（v1.2）を日本語に翻訳したものです。

## 🙏 謝辞

ワークフローとテンプレートは [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills)（MIT）を基にしています。そこで用いられている論文執筆の知識は、[Peng Sida（彭思达）氏の学習ノート](https://github.com/pengsida/learning_research) に由来します。詳細は [`NOTICE.md`](skills/bestpaper-writing/NOTICE.md) を参照してください。

## 🤝 コントリビュート

不具合の報告、コーパスでまだカバーされていない分野（NLP、ロボティクス、システムなど）の論文の提案、このスキルを使って執筆したドラフトの共有など、Issue でのフィードバックを歓迎します。役に立ったら、ぜひ ⭐ Star をお願いします。
