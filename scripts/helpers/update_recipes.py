def update_recipes(fs_recipes: list[dict[str, str]], current: list[dict[str, str]]) -> list[dict[str, str]]:
    curr_map: dict[tuple[str, str], dict[str, str]] = {(r["name"], r["category"]): r for r in current}
    fs_keys = {(r["name"], r["category"]) for r in fs_recipes}
    for r in fs_recipes:
        key = (r["name"], r["category"])
        if key in curr_map:
            merged = curr_map[key].copy()
            merged.update(r)
            merged.setdefault("formatted", False)
            curr_map[key] = merged
        else:
            new_r = r.copy()
            new_r.setdefault("formatted", False)
            curr_map[key] = new_r
    return [curr_map[k] for k in curr_map if k in fs_keys]
