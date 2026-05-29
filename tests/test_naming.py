from card_builder.naming import TIME_PT, item_name, titleize


def test_item_name_strips_namespace_and_titleizes():
    assert item_name("cobblemon:water_stone") == "Water Stone"


def test_item_name_without_namespace():
    assert item_name("thunder_stone") == "Thunder Stone"


def test_titleize():
    assert titleize("level_up") == "Level Up"


def test_time_pt_labels():
    assert TIME_PT["day"] == "de dia"
    assert TIME_PT["night"] == "de noite"
