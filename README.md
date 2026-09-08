# 1. Goal
HermiT 理由付けエンジン（Owlready2）による OWL オントロジーの論理推論と、LangGraph / Ollama（`llama3.2:3b`）によるテキスト記述・生成を組み合わせた **Neuro-Symbolic AI エージェント** の実験リポジトリです。

シンボリックAI（論理推論）によって未定義の個体（`Thing`）の概念（クラス）を動的に確定させ、その分類情報に基づいて LLM がコンテキストに沿った表現を自動生成します。

---

# 2. Overview

本プロジェクトでは、以下の2つのドメインにおける論理推論（`sync_reasoner`）の有無による LLM の生成結果の挙動・変化を検証します。

1. **生物領域 (`snake-food.py`)**: `Snake` / `Food` / `eats` 関係の推論
2. **IT/技術領域 (`it-tech.py`)**: `Language` / `OperatingSystem` / `runsOn` 関係の推論

### 推論による概念変化のメカニズム

| スクリプト | 関連定義 (Domain/Range) | 推論なし (`USE_REASONER=False`) | 推論あり (`USE_REASONER=True`) |
| :--- | :--- | :--- | :--- |
| **`snake-food.py`** | `eats` (domain: `Snake`, range: `Food`) | `ABC`: `Thing`<br>`XYZ`: `Thing` | `ABC`: **`Snake`**<br>`XYZ`: **`Food`** |
| **`it-tech.py`** | `runsOn` (domain: `Language`, range: `OperatingSystem`) | `ABC`: `Thing`<br>`XYZ`: `Thing` | `ABC`: **`Language`**<br>`XYZ`: **`OperatingSystem`** |

---

# 3. Setup

### 3-1. 必要パッケージのインストール

HermiT 推論器の実行には Java Runtime Environment (JRE) が必要です。

```bash
# OSレベルの依存パッケージインストール
apt-get update && apt-get install -y default-jre

# Python ライブラリのインストール
pip install owlready2 langchain-ollama langchain-core langchain langgraph
```

### 3-2. 前提環境

* Kubernetes クラスタ内、またはローカル環境で `svc-ollama`（Port: 11434）が稼働していること。
* Ollama に `llama3.2:3b` モデルがロードされていること。

# 4. Usage

#### コード構成 (Code Structure)
- snake-food.py: 生物学的な捕食関係（Snake - eats -> Food）の記述・推論サンプル。

- it-tech.py: ソフトウェアの動作関係（Language - runsOn -> OperatingSystem）の記述・推論サンプル。


#### 生物オントロジーの検証
```bash
python3 snake-food.py
```
#### IT/技術オントロジーの検証
```bash
python3 it-tech.py
```
※ スクリプト内の USE_REASONER = True / False フラグを切り替えることで、推論の有無による比較が可能です。


# 5. Execution Results
### 5-1. snake-food.py (生物ドメイン)
#### 推論あり (USE_REASONER = True)
HermiT により ABC が Snake、XYZ が Food に再分類（Reparenting）され、LLM はヘビと食物の関係性として文章を生成します。
```
* Owlready2 * Running HermiT...
    java -Xmx2000M -cp /usr/local/lib/python3.11/site-packages/owlready2/hermit:/usr/local/lib/python3.11/site-packages/owlready2/hermit/HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:////tmp/tmpajqumydy
* Owlready2 * HermiT took 0.3687553405761719 seconds
* Owlready * Reparenting biology.ABC: {owl.Thing} => {biology.Snake}
* Owlready * Reparenting biology.XYZ: {owl.Thing} => {biology.Food}
* Owlready * (NB: only changes on entities loaded in Python are shown, other changes are done but not listed)
>>> [SYSTEM] オントロジー推論（sync_reasoner）を実行しました。

[TOOL OUTPUT START]
個体名: ABC | 所属クラス: ['Snake'] | 食べているもの: ['XYZ']
個体名: XYZ | 所属クラス: ['Food']
[TOOL OUTPUT END]


=== エージェントが生成した文章 ===
ABCとXYZは、仲が良く一緒に生活している two 個体です。

ABCは、XYZを食べることができる大きな蛇です。XYZは、ABCの好きな食べ物です。

いつもABCがXYZを食べるのを楽しみにしています。ABCは、XYZを食べるのを楽しみにしています。XYZは、ABCの友達です。

どちらも、仲が良く一緒に生活していることが大切です。
```
#### 推論なし (USE_REASONER = False)
クラスが Thing（未定義）のままであるため、LLM は具体的な概念を用いず汎用的な表現で記述します。
```
>>> [SYSTEM] オントロジー推論を実行せず、素のデータで処理します。

[TOOL OUTPUT START]
個体名: ABC | 所属クラス: ['Thing'] | 食べているもの: ['XYZ']
個体名: XYZ | 所属クラス: ['Thing']
[TOOL OUTPUT END]


=== エージェントが生成した文章 ===
ABCとXYZは、世界の素敵なものたちです。

ABCは、XYZを食べることができます。XYZは、ABCの友達です。

ABCとXYZは、一緒に遊びます。ABCはXYZを楽しみます。

ABCとXYZは、世界を楽しみます。
```

### 5-2. it-tech.py (IT/技術ドメイン)
#### 推論あり (USE_REASONER = True)
HermiT により ABC が Language、XYZ が OperatingSystem に分類されます。
```
* Owlready2 * Running HermiT...
    java -Xmx2000M -cp /usr/local/lib/python3.11/site-packages/owlready2/hermit:/usr/local/lib/python3.11/site-packages/owlready2/hermit/HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:////tmp/tmpcavdcpho
* Owlready2 * HermiT took 0.3718221187591553 seconds
* Owlready * Reparenting technology.ABC: {owl.Thing} => {technology.Language}
* Owlready * Reparenting technology.XYZ: {owl.Thing} => {technology.OperatingSystem}
* Owlready * (NB: only changes on entities loaded in Python are shown, other changes are done but not listed)
>>> [SYSTEM] オントロジー推論（sync_reasoner）を実行しました。

[TOOL OUTPUT START]
個体名: ABC | 所属クラス: ['Language'] | 動作対象(runsOn): ['XYZ']
個体名: XYZ | 所属クラス: ['OperatingSystem']
[TOOL OUTPUT END]


=== エージェントが生成した文章 ===
ABCとXYZは、世界のさまざまな場所で活躍しています。

ABCは、言語の世界で活躍しています。人々はABCを通して、様々な言語を学び、交流することができます。ABCは、人々の間の理解と交流を促進するために、非常に重要な役割を果たしています。

XYZは、コンピュータの世界で活躍しています。XYZは、コンピュータシステムを管理し、人々の間のコミュニケーションを可能にするために使用されています。XYZは、コンピュータの世界で人々の生活をサポートするために、非常に重要な役割を果たしています。

ABCとXYZは、世界のさまざまな場所で活躍しています。人々は、どちらも通して様々なものを学び、交流することができます。
```

#### 推論なし (USE_REASONER = False)
```
>>> [SYSTEM] オントロジー推論を実行せず、素のデータで処理します。

[TOOL OUTPUT START]
個体名: ABC | 所属クラス: ['Thing'] | 動作対象(runsOn): ['XYZ']
個体名: XYZ | 所属クラス: ['Thing']
[TOOL OUTPUT END]


=== エージェントが生成した文章 ===
ABCとXYZは、世界の素晴らしいものたちです。

ABCは、XYZと一緒に遊んで楽しいです。ABCは、XYZを友達と呼んでいます。

XYZは、ABCと一緒に遊ぶことが大好きです。XYZは、ABCを友達と呼んでいます。

ABCとXYZは、世界をより素晴らしいものにします。
```
