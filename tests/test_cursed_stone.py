import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from spirit.game.attributes import AttrID
from spirit.game.models.board import BoardEntity, BoardState, CardEntity, PokemonEntity
from spirit.game.scripts.cards.EX12.CursedStone_72 import card, cursed_stone_targets
from spirit.game.scripts.cards.EX14.CessationCrystal_74 import card as cessation_crystal
from spirit.game.session.effects import resolve_triggered_ability
from spirit.game.session.game_session import GameSession


def make_entity(entity_class, entity_id, owner_id):
    entity = object.__new__(entity_class)
    BoardEntity.__init__(
        entity,
        entity_id=entity_id,
        owning_player_id=owner_id,
        archetype_id=f"archetype-{entity_id}",
    )
    entity.card_obj = SimpleNamespace()
    return entity


class CursedStoneTests(unittest.TestCase):
    def test_cursed_stone_targets_poke_ability_and_poke_power_pokemon(self):
        self.assertTrue(card.abilities)

        class DummyPokemon:
            def __init__(self, ability_types):
                self._abilities = [{"abilityType": ability_type} for ability_type in ability_types]

            def get_attribute(self, key):
                if key == AttrID.PIE_ABILITIES:
                    return self._abilities
                return None

        targets = [
            DummyPokemon(["PokePower"]),
            DummyPokemon(["PokeAbility"]),
            DummyPokemon(["PokeAbility"]),
            DummyPokemon(["PokeBody", "PokePower"]),
            DummyPokemon([]),
        ]
        self.assertEqual(
            cursed_stone_targets(targets),
            [targets[0], targets[1], targets[2], targets[3]],
        )


class CursedStoneInteractionTests(unittest.IsolatedAsyncioTestCase):
    async def test_cursed_stone_triggers_with_cessation_crystal_active(self):
        board = BoardState("game-1", ["player-1", "player-2"])
        active_area = board.find_player_area("player-1", "activePokemonArea")
        stadium_area = board.find_global_area("activeStadium")
        active = make_entity(PokemonEntity, "active", "player-1")
        active.set_attribute(AttrID.PIE_ABILITIES, [{"abilityType": "PokeAbility"}])
        crystal = make_entity(CardEntity, "crystal", "player-1")
        stadium = make_entity(CardEntity, "cursed-stone", "player-1")
        board.add_card_to_area(active, active_area)
        active.add_child(crystal)
        board.add_card_to_area(stadium, stadium_area)

        session = SimpleNamespace(
            board_state=board,
            game_id="game-1",
            _turn_order=lambda: ["player-1", "player-2"],
            _opponent_id=lambda player_id: "player-2" if player_id == "player-1" else "player-1",
        )
        damage = AsyncMock()
        with patch(
            "spirit.game.session.effects.def_for",
            side_effect=lambda archetype_id: (
                cessation_crystal if archetype_id == "archetype-crystal"
                else card if archetype_id == "archetype-cursed-stone"
                else None
            ),
        ), patch(
            "spirit.game.session.effects._send_ability_brackets",
            new=AsyncMock(),
        ), patch(
            "spirit.game.session.effects.EffectContext.deal_damage",
            new=damage,
        ):
            result = await resolve_triggered_ability(
                session, "player-1", stadium, card.abilities[0]
            )

        self.assertIsNotNone(result)
        damage.assert_awaited_once_with(
            10, target=active, apply_modifiers=False, as_counters=True
        )


if __name__ == "__main__":
    unittest.main()
