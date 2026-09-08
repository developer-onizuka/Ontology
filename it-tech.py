from owlready2 import ObjectProperty, Thing, get_ontology, sync_reasoner
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent

# ==================================================
# 1. オントロジーのセットアップ (IT / プログラミング領域)
# ==================================================
USE_REASONER = True
#USE_REASONER = False

it_onto = get_ontology("http://example.org/technology.owl")

with it_onto:
    class Language(Thing):
        pass

    class OperatingSystem(Thing):
        pass

    class runsOn(ObjectProperty):
        domain = [Language]
        range = [OperatingSystem]

    # インスタンス名は意味を持たない ABC / XYZ に設定
    somethingA = Thing("ABC")
    somethingB = Thing("XYZ")

    if USE_REASONER:
        somethingA.runsOn.append(somethingB)
        sync_reasoner(it_onto)
        print(">>> [SYSTEM] オントロジー推論（sync_reasoner）を実行しました。")
    else:
        print(">>> [SYSTEM] オントロジー推論を実行せず、素のデータで処理します。")


# ==================================================
# 2. ツール定義（リスト形式引数対応）
# ==================================================
@tool
def get_multiple_entities_info(entity_names: list[str]) -> str:
    """指定された複数の個体名リスト（例: ['ABC', 'XYZ']）の情報を一括で取得します。"""
    results = []
    for name in entity_names:
        entity = it_onto.search_one(iri=f"*{name}")
        if not entity:
            results.append(f"個体名: {name} | オントロジー内に見つかりませんでした。")
            continue

        # 所属クラス（型）の抽出
        classes = []
        for c in entity.is_a:
            classes.append(c.name)

        # runsOn 関係の抽出
        runs_on_relations = []
        for os in getattr(entity, "runsOn", []):
            runs_on_relations.append(os.name)

        info = f"個体名: {entity.name} | 所属クラス: {classes}"
        if runs_on_relations:
            info += f" | 動作対象(runsOn): {runs_on_relations}"
        results.append(info)

    output_text = "\n".join(results)

    # --------------------------------------------------
    # LLMに渡されるツール出力の生データをターミナルに表示
    # --------------------------------------------------
    print("\n[TOOL OUTPUT START]")
    print(output_text)
    print("[TOOL OUTPUT END]\n")

    return output_text


tools = [get_multiple_entities_info]


# ==================================================
# 3. K8s 上の svc-ollama 接続 & LangGraph エージェント構築
# ==================================================
llm = ChatOllama(
    model="llama3.2:3b",
    base_url="http://svc-ollama:11434",
    temperature=0
)

# snake-food.py と完全に同一のシステムプロンプト
agent_executor = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "あなたはオントロジーを参照して回答するAIアシスタントです。"
        "必要に応じて 'get_multiple_entities_info' ツールを使い、得られたデータのみに基づいて自然な文章を作成してください。"
        "検索対象が複数ある場合は、個体名をリスト形式（例: ['ABC', 'XYZ']）で一度にツールに渡してください。"
    )
)

# 実行（対象個体名も ABC と XYZ に統一）
user_input = "ABCとXYZという個体について、オントロジーの情報を調べて100字程度の子供向け物語を作成してください。"
response = agent_executor.invoke({"messages": [("user", user_input)]})

print("\n=== エージェントが生成した文章 ===")
print(response["messages"][-1].content)
