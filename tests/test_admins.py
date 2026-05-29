from modpack_bot.admins import admins_message


def test_admins_message_lists_mentions_pt():
    assert admins_message(["<@1>", "<@2>"], "pt") == "Você pode falar com a staff aqui: <@1>, <@2>"


def test_admins_message_lists_mentions_en():
    assert admins_message(["<@1>"], "en") == "You can reach the staff here: <@1>"


def test_admins_message_empty_returns_fallback_pt():
    assert "cargo Admin" in admins_message([], "pt")


def test_admins_message_empty_returns_fallback_en():
    assert "Admin role" in admins_message([], "en")
