import unittest

from spirit.game.attributes import AttrID, CardType
from spirit.game.session.effects import is_baby_pokemon


class DummyCard:
    def __init__(self, attributes):
        self._attributes = attributes

    def get_attribute(self, key):
        return self._attributes.get(key)


def pokemon_card(pie_abilities=None):
    return DummyCard({
        AttrID.CARD_TYPE: CardType.POKEMON.value,
        AttrID.PIE_ABILITIES: pie_abilities or [],
    })


class IsBabyPokemonTests(unittest.TestCase):
    def test_true_for_a_pokemon_with_the_baby_rule_ability_id(self):
        card = pokemon_card([{"abilityID": "baby_rule"}])

        self.assertTrue(is_baby_pokemon(card))

    def test_true_for_a_pokemon_with_a_baby_rule_title_id(self):
        card = pokemon_card([{"title": {"id": "baby_rule"}}])

        self.assertTrue(is_baby_pokemon(card))

    def test_false_for_a_pokemon_without_the_baby_rule_ability(self):
        card = pokemon_card([{"abilityID": "some_other_ability"}])

        self.assertFalse(is_baby_pokemon(card))

    def test_false_for_a_pokemon_with_no_abilities(self):
        card = pokemon_card()

        self.assertFalse(is_baby_pokemon(card))

    def test_false_for_a_non_pokemon_card(self):
        card = DummyCard({
            AttrID.CARD_TYPE: CardType.TRAINER.value,
            AttrID.PIE_ABILITIES: [{"abilityID": "baby_rule"}],
        })

        self.assertFalse(is_baby_pokemon(card))

    def test_ignores_malformed_ability_entries(self):
        card = pokemon_card(["not-a-dict", {"abilityID": "baby_rule"}])

        self.assertTrue(is_baby_pokemon(card))


if __name__ == "__main__":
    unittest.main()
