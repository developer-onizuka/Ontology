from owlready2 import World, Thing, ObjectProperty, sync_reasoner
from fastmcp import FastMCP

mcp = FastMCP(name="Ontology Reasoner MCP")

@mcp.tool()
def build_and_reason(domain: str, entity_names: list[str]) -> str:
    # リクエストごとに新しい World インスタンスを作成し、分離する
    world = World()
    
    if domain == "biology":
        onto = world.get_ontology("http://example.org/biology.owl")
        
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
        onto = world.get_ontology("http://example.org/technology.owl")
        
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
        world.close()
        return f"エラー: 未対応のドメイン '{domain}' です。"

    # キーワード引数 x= を外し、位置引数としてシンプルに渡す
    sync_reasoner(world)

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

    # World のクリーンアップ
    world.close()

    return "\n".join(results)

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=5001)
