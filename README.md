# 1. Goal
HermiT 理由付けエンジン（Owlready2）による OWL オントロジーの論理推論と、Model Context Protocol (MCP) / LangGraph / Ollama（`llama3.2:3b`）を組み合わせた **Neuro-Symbolic AI エージェントおよび MCP サーバー** の総合的な実験・実用リポジトリです。

シンボリックAI（論理推論）によって未定義の個体（`Thing`）の概念（クラス）を動的に確定させ、その分類情報を LLM や外部の MCP クライアント（Claude Desktop / MCP Inspector）へ提供します。
リクエストごとに独立した `World` を動的に生成・破棄するマルチワールド・アーキテクチャを採用することで、複数ドメイン（生物・IT技術など）間における完全なデータ分離とスケーラブルな推論環境を実現しています。


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
個体名: ABC | 所属クラス: ['Thing']
個体名: XYZ | 所属クラス: ['Thing']
[TOOL OUTPUT END]


=== エージェントが生成した文章 ===
ABCとXYZは、世界の物体です。

ABCは、すばらしい赤い車です。ABCは、子どもたちを楽しませるために、遊びに来ます。

XYZは、美しい緑の花です。XYZは、空気を浄化して、地球を守ります。

ABCとXYZは、どちらも世界の物体です。どちらも、子どもの心に喜びをもたらします。
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
個体名: ABC | 所属クラス: ['Thing']
個体名: XYZ | 所属クラス: ['Thing']
[TOOL OUTPUT END]


=== エージェントが生成した文章 ===
ABCとXYZは、世界の物体です。

ABCは、すばらしい赤い車です。ABCは、子どもたちを楽しませるために、遊びに来ます。

XYZは、美しい緑の花です。XYZは、空気を浄化して、地球を守ります。

ABCとXYZは、どちらも世界の物体です。どちらも、子どもの心に喜びをもたらします。
```

# 6. MCP Server for Ontology
本リポジトリの推論ロジックを、MCP を介して Claude Desktop や npx @modelcontextprotocol/inspector からリモートツールとして利用できる MCP サーバー（ontology-mcp.py）を実装しています。リクエストごとに独立した World() インスタンスを動的に生成・破棄するマルチワールド・アーキテクチャを採用しており、複数ドメイン間のデータ汚染や推論結果の混同を完全に防止しています。

### 6-1. MCP　サーバーの実装について
- 完全なドメイン分離: リクエストごとに World() を生成するため、biology と technology の世界がメモリ上で完全に隔離されます。

- FastMCP による迅速な実装: 高速な SSE（Server-Sent Events）トランスポートに対応し、外部クライアントからのツール呼び出しをシームレスに処理します。

### 6-2. MCP　サーバーをKubernetesで実行
```
git clone https://github.com/developer-onizuka/Ontology
cd Ontology
kubectl apply -f ontology-mcp.yaml
```
```
vagrant@master:~/Ontology/mcp$ kubectl get svc
NAME                 TYPE           CLUSTER-IP       EXTERNAL-IP    PORT(S)             AGE
svc-ontology-mcp     LoadBalancer   10.99.239.145    192.168.33.4   5001:32133/TCP      14m
```
LoadBalancerで取得した外部IPを以下コマンドに与えてInspectorを起動します。
```
npx @modelcontextprotocol/inspector http://192.168.33.4:5001/sse
```
以下に示すようなJson形式の入力を与えて、動作が妥当なものかを検証します。
```
{
  "domain": "biology",
  "entity_names": ["ABC", "XYZ"]
}
```
```
{
  "domain": "technology",
  "entity_names": ["ABC", "XYZ"]
}
```
<img src="https://github.com/developer-onizuka/Ontology/blob/main/biology.png" width="720"><br>

<img src="https://github.com/developer-onizuka/Ontology/blob/main/technology.png" width="720"><br>

### 6-3. ClaudeDesktopとの連携
claude_desktop_config.jsonに以下を追加し、ClaudeDesktopを再起動します。
```
  "mcpServers": {
    "ontology": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "http://192.168.33.4:5001/sse",
        "--allow-http"
      ]
    }
  },
```
以下のようなプロンプトを与えて、動作を確認します。
```
ABCとXYZという個体について、オントロジーの情報を調べて100字程度の子供向け物語を作成してください。ただしドメインはbiologyとします。
```
```
ABCとXYZという個体について、オントロジーの情報を調べて100字程度の子供向け物語を作成してください。ただしドメインはtechnologyとします。
```
<img src="https://github.com/developer-onizuka/Ontology/blob/main/claudeDesktop.png" width="720"><br>

