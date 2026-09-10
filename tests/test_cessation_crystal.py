import unittest
from types import SimpleNamespace
from unittest.mock import patch

from spirit.game.attributes import AttrID, TrainerType
from spirit.game.models.board import BoardEntity, BoardState, CardEntity, PokemonEntity
from spirit.game.scripts.cards.EX14.CessationCrystal_74 import card as cessation_crystal
from spirit.game.session.game_session import GameSession


def make_pokemon(entity_id, owner_id, hp=100):
    pokemon = object.__new__(PokemonEntity)
    BoardEntity.__init__(
        pokemon,
        entity_id=entity_id,
        owning_player_id=owner_id,
        archetype_id=f"archetype-{entity_id}",
    )
    pokemon.card_obj = SimpleNamespace()
    pokemon.set_attribute(AttrID.HP, hp)
    pokemon.attribute_originals[AttrID.HP.value] = hp
    return pokemon


def make_tool(entity_id, owner_id):
    tool = object.__new__(CardEntity)
    BoardEntity.__init__(
        tool,
        entity_id=entity_id,
        owning_player_id=owner_id,
        archetype_id=f"archetype-{entity_id}",
    )
    tool.card_obj = SimpleNamespace()
    tool.set_attribute(AttrID.TRAINER_TYPE, TrainerType.POKEMON_TOOL.value)
    return tool


class CessationCrystalTests(unittest.TestCase):
    def test_cannot_attach_to_pokemon_ex(self):
        regular = make_pokemon("regular", "player-1")
        pokemon_ex = make_pokemon("ex", "player-1")

        with patch(
            "spirit.game.scripts.cards.EX14.CessationCrystal_74.is_pokemon_ex",
            side_effect=lambda archetype_id: archetype_id == "archetype-ex",
        ):
            self.assertTrue(cessation_crystal.attach_to(regular))
            self.assertFalse(cessation_crystal.attach_to(pokemon_ex))

    def test_locks_all_pokemon_abilities_only_while_attached_to_active(self):
        board = BoardState("game-1", ["player-1", "player-2"])
        active_area = board.find_player_area("player-1", "activePokemonArea")
        bench_area = board.find_player_area("player-1", "bench")

        active_holder = make_pokemon("active-holder", "player-1")
        bench_holder = make_pokemon("bench-holder", "player-1")
        opponent = make_pokemon("opponent-active", "player-2")

        board.add_card_to_area(active_holder, active_area)
        board.add_card_to_area(bench_holder, bench_area)

        active_tool = make_tool("active-tool", "player-1")
        active_holder.add_child(active_tool)
        bench_tool = make_tool("bench-tool", "player-1")
        bench_holder.add_child(bench_tool)

        self.assertIsNotNone(cessation_crystal.passive)
        self.assertTrue(cessation_crystal.passive.blocks_abilities(active_holder, active_tool))
        self.assertTrue(cessation_crystal.passive.blocks_abilities(opponent, active_tool))
        self.assertFalse(cessation_crystal.passive.blocks_abilities(active_holder, bench_tool))
        self.assertFalse(cessation_crystal.passive.blocks_abilities(opponent, bench_tool))


class CessationCrystalEvolutionTests(unittest.IsolatedAsyncioTestCase):
    async def test_discards_when_holder_evolves_into_pokemon_ex(self):
        session = object.__new__(GameSession)
        session.game_id = "game-1"
        session.board_state = BoardState(session.game_id, ["player-1", "player-2"])
        session.players = {"player-1": SimpleNamespace(screen_name="Player One")}
        session.turn_state = SimpleNamespace(mark_entered_play=lambda entity_id: None)
        session.reset_pokemon_damage = lambda pokemon: None
        session.clear_pokemon_effects = lambda pokemon: False

        async def no_op(*args, **kwargs):
            return None

        session.refresh_granted_abilities = no_op
        session._send_play_sequence = no_op
        session._fire_triggered_abilities = no_op
        session._fire_ally_evolved_triggers = no_op
        session.enforce_bench_capacity = no_op

        board = session.board_state
        active = board.find_player_area("player-1", "activePokemonArea")
        discard = board.find_player_area("player-1", "discard")
        basic = make_pokemon("basic", "player-1", hp=100)
        evolution = make_pokemon("evolution-ex", "player-1", hp=120)
        tool = make_tool("cessation-crystal", "player-1")
        board.add_card_to_area(basic, active)
        board.add_card_to_area(evolution, discard)
        basic.add_child(tool)
        board._register_entity(tool)

        with patch("spirit.game.session.game_session.def_for") as def_for, \
            patch(
                "spirit.game.scripts.cards.EX14.CessationCrystal_74.is_pokemon_ex",
                side_effect=lambda archetype_id: archetype_id == "archetype-evolution-ex",
            ), \
                patch("spirit.game.session.game_session.effective_max_hp", side_effect=lambda board, pokemon: pokemon.get_attribute(AttrID.HP)), \
                patch("spirit.game.session.game_session.evolve_heal_amount", return_value=0):
            def_for.side_effect = lambda archetype_id: (
                cessation_crystal if archetype_id == "archetype-cessation-crystal"
                else SimpleNamespace(abilities=[])
            )
            await session.perform_evolution("player-1", evolution, basic)

        self.assertIs(evolution.parent, active)
        self.assertIs(tool.parent, discard)


if __name__ == "__main__":
    unittest.main()
