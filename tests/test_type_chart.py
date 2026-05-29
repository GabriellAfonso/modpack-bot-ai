from card_builder.type_chart import TYPE_PT, weaknesses


def test_dual_type_stacks_to_4x():
    # fire/flying is doubly weak to rock.
    assert weaknesses(["fire", "flying"])["rock"] == 4.0


def test_single_type_2x():
    weak = weaknesses(["water"])
    assert weak["grass"] == 2.0
    assert weak["electric"] == 2.0


def test_only_multipliers_above_one_returned():
    # nothing resisted/neutral leaks in.
    assert all(m > 1 for m in weaknesses(["normal"]).values())
    assert weaknesses(["normal"]) == {"fighting": 2.0}


def test_type_pt_has_all_18_types():
    assert len(TYPE_PT) == 18
    assert TYPE_PT["fire"] == "Fogo"
