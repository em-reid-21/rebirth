import unittest

from spirit.game.attributes import AttrID, CardType, PokemonTypes
from spirit.game.models.board import BoardState, EnergyEntity, create_card_entity
from spirit.game.models.card import Card
from spirit.game.scripts.cards.EX1.DarknessEnergy_93 import card as darkness_energy
from spirit.game.scripts.cards.EX14.CrystalBeach_75 import card as crystal_beach
from spirit.game.scripts.cards.Free_Energy.FireEnergy_2 import card as fire_energy
from spirit.game.scripts.cards.SWSH10.DoubleTurboEnergy_216 import card as double_turbo_energy
from spirit.game.session.passives import energy_provided_options


def server_card(definition):
    archetype = definition.to_archetype_dict()
    return Card(
        archetype["guid"],
        archetype["key"],
        archetype["attributes"],
        archetype.get("display_name"),
        archetype.get("searchable_by", []),
        archetype.get("subtypes", []),
    )


def energy_entity(definition, entity_id, owner_id="player-1"):
    entity = create_card_entity(server_card(definition), owner_id, entity_id)
    if not isinstance(entity, EnergyEntity):
        entity.set_attribute(AttrID.CARD_TYPE, CardType.ENERGY.value)
        entity.__class__ = EnergyEntity
    return entity


def put_stadium_in_play(board, definition, entity_id="stadium-1", owner_id="player-1"):
    stadium = create_card_entity(server_card(definition), owner_id, entity_id)
    board.add_card_to_area(stadium, board.find_global_area("activeStadium"))
    return stadium


class CrystalBeachTests(unittest.TestCase):
    def test_caps_a_double_energy_at_one_colorless_while_in_play(self):
        board = BoardState("game-1", ["player-1", "player-2"])
        put_stadium_in_play(board, crystal_beach)
        energy = energy_entity(double_turbo_energy, "double-turbo")

        self.assertEqual(
            energy_provided_options(board, energy),
            [[PokemonTypes.COLORLESS.value]],
        )

    def test_double_energy_is_unaffected_without_the_stadium(self):
        board = BoardState("game-1", ["player-1", "player-2"])
        energy = energy_entity(double_turbo_energy, "double-turbo")

        self.assertEqual(
            energy_provided_options(board, energy),
            [[PokemonTypes.COLORLESS.value, PokemonTypes.COLORLESS.value]],
        )

    def test_special_energy_already_providing_one_is_unaffected(self):
        board = BoardState("game-1", ["player-1", "player-2"])
        put_stadium_in_play(board, crystal_beach)
        energy = energy_entity(darkness_energy, "darkness-energy")

        self.assertEqual(
            energy_provided_options(board, energy),
            [[PokemonTypes.DARKNESS.value]],
        )

    def test_basic_energy_is_unaffected(self):
        board = BoardState("game-1", ["player-1", "player-2"])
        put_stadium_in_play(board, crystal_beach)
        energy = energy_entity(fire_energy, "fire-energy")

        self.assertEqual(
            energy_provided_options(board, energy),
            [[PokemonTypes.FIRE.value]],
        )


if __name__ == "__main__":
    unittest.main()
