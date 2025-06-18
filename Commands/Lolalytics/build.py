def get_build(champion):
    from Commands.Lolalytics.skillOrder import get_skill_order
    from Commands.Lolalytics.startingItems import get_starting_items
    from Commands.Lolalytics.coreBuild import get_core_build
    from Commands.Lolalytics.runes import get_runes
    from Commands.Lolalytics.lateGameItems import get_late_game_items
    from Commands.Lolalytics.summoners import get_summoner

    skill_order = get_skill_order(champion)
    starting_items = get_starting_items(champion)
    core_build = get_core_build(champion)
    runes = get_runes(champion)
    late_game_items = get_late_game_items(champion)
    summoner = get_summoner(champion)

    return {
        "skill_order": skill_order,
        "starting_items": starting_items,
        "core_build": core_build,
        "late_game_items": late_game_items,
        "runes": runes,
        "summoner": summoner
    }
if __name__ == "__main__":
    print(get_build("ahri"))