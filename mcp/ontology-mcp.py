from owlready2 import get_ontology, sync_reasoner, Thing, ObjectProperty
from fastmcp import FastMCP

# FastMCP の初期化
mcp = FastMCP(name="Ontology Reasoner MCP")

def build_and_reason(domain: str, entity_names: list[str]) -> str:
    """オントロジーを構築し、HermiT 推論を実行する共通ロジック"""
    if domain == "biology":
        onto = get_ontology("http://example.org/biology.owl")
        with onto:
            class Snake(Thing): pass
            class Food(Thing): pass
            class eats(ObjectProperty):
                domain = [Snake]
                range = [Food]
            
            somethingA = Thing("ABC", namespace=onto)
            somethingB = Thing("XYZ", namespace=onto)
            somethingA.eats.append(somethingB)

    elif domain == "technology":
        onto = get_ontology("http://example.org/technology.owl")
        with onto:
            class Language(Thing): pass
            class OperatingSystem(Thing): pass
            class runsOn(ObjectProperty):
                domain = [Language]
                range = [OperatingSystem]
            
            somethingA = Thing("ABC", namespace=onto)
            somethingB = Thing("XYZ", namespace=onto)
            somethingA.runsOn.append(somethingB)
    else:
        return f"エラー: 未対応のドメイン '{domain}' です。"

    # HermiT 推論器の実行
    sync_reasoner(onto)

    # 結果の整形
    results = []
    for name in entity_names:
        entity = onto.search_one(iri=f"*{name}")
        if not entity:
            continue
        
        classes = [c.name for c in entity.is_a if hasattr(c, "name")]
        
        relations = {}
        for prop in onto.object_properties():
            prop_name = prop.name
            targets = getattr(entity, prop_name, [])
            if targets:
                relations[prop_name] = [t.name for t in targets]
        
        info = f"個体名: {entity.name} | 所属クラス: {classes}"
        if relations:
            info += f" | 関係性: {relations}"
        results.append(info)

    return "\n".join(results)


@mcp.tool()
def get_ontology_reasoning(domain: str, entity_names: list[str]) -> str:
    """
    指定されたドメイン（biology または technology）のオントロジーに対して HermiT 推論を実行し、
    推論によって動的に割り当てられたクラス（型）と関係性の情報を返します。
    """
    try:
        return build_and_reason(domain, entity_names)
    except Exception as e:
        return f"推論中にエラーが発生しました: {str(e)}"


if __name__ == "__main__":
    # fastmcp を使用しているため、run() に host / port を直接渡せます
    mcp.run(transport="sse", host="0.0.0.0", port=5001)
