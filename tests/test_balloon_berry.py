import unittest

from spirit.game.attributes import AttrID, CardType
from spirit.game.models.board import BoardState, EnergyEntity, create_card_entity
from spirit.game.models.card import Card, PokemonCard
from spirit.game.scripts.cards.CEL25.Pikachu_5 import card as pikachu
from spirit.game.scripts.cards.EX3.BalloonBerry_82 import card as balloon_berry
from spirit.game.scripts.cards.Free_Energy.FireEnergy_2 import card as fire_energy
from spirit.game.session.legal_actions import SelectionKind, TurnState, _retreat_entry
from spirit.game.session.passives import active_passives, effective_retreat_cost, on_retreat_discards


def server_card(definition):
    archetype = definition.to_archetype_dict()
    card_type = archetype["attributes"][str(AttrID.CARD_TYPE.value)]["value"]
    card_class = PokemonCard if card_type == CardType.POKEMON.value else Card
    return card_class(
        archetype["guid"],
        archetype["key"],
        archetype["attributes"],
        archetype.get("display_name"),
        archetype.get("searchable_by", []),
        archetype.get("subtypes", []),
    )


def make_entity(definition, entity_id, owner_id="player-1"):
    return create_card_entity(server_card(definition), owner_id, entity_id)


def make_energy(entity_id, owner_id="player-1"):
    entity = make_entity(fire_energy, entity_id, owner_id)
    if not isinstance(entity, EnergyEntity):
        entity.set_attribute(AttrID.CARD_TYPE, CardType.ENERGY.value)
        entity.__class__ = EnergyEntity
    return entity


class BalloonBerryTests(unittest.TestCase):
    def test_makes_holders_retreat_cost_zero_and_discards_on_retreat(self):
        board = BoardState("game-1", ["player-1", "player-2"])
        active_area = board.find_player_area("player-1", "activePokemonArea")
        holder = make_entity(pikachu, "holder")
        board.add_card_to_area(holder, active_area)
        tool = make_entity(balloon_berry, "balloon-berry")
        holder.add_child(tool)

        self.assertEqual(effective_retreat_cost(board, holder), 0)
        discards = on_retreat_discards(board, holder)
        self.assertEqual(discards, [tool])

    def test_does_not_apply_to_a_pokemon_without_balloon_berry_attached(self):
        board = BoardState("game-1", ["player-1", "player-2"])
        active_area = board.find_player_area("player-1", "activePokemonArea")
        holder = make_entity(pikachu, "holder")
        board.add_card_to_area(holder, active_area)

        self.assertEqual(effective_retreat_cost(board, holder), 1)
        self.assertEqual(on_retreat_discards(board, holder), [])

    def test_does_not_apply_to_a_different_pokemon(self):
        board = BoardState("game-1", ["player-1", "player-2"])
        active_area = board.find_player_area("player-1", "activePokemonArea")
        bench_area = board.find_player_area("player-1", "bench")
        holder = make_entity(pikachu, "holder")
        other = make_entity(pikachu, "other")
        board.add_card_to_area(holder, active_area)
        board.add_card_to_area(other, bench_area)
        tool = make_entity(balloon_berry, "balloon-berry")
        holder.add_child(tool)

        self.assertEqual(effective_retreat_cost(board, other), 1)
        self.assertEqual(on_retreat_discards(board, other), [])

    def test_registers_as_an_active_passive_while_attached(self):
        board = BoardState("game-1", ["player-1", "player-2"])
        active_area = board.find_player_area("player-1", "activePokemonArea")
        holder = make_entity(pikachu, "holder")
        board.add_card_to_area(holder, active_area)
        tool = make_entity(balloon_berry, "balloon-berry")
        holder.add_child(tool)

        carriers = [carrier for _, carrier in active_passives(board)]

        self.assertIn(tool, carriers)

    def test_retreat_offer_skips_the_pay_retreat_cost_prompt(self):
        board = BoardState("game-1", ["player-1", "player-2"])
        active_area = board.find_player_area("player-1", "activePokemonArea")
        bench_area = board.find_player_area("player-1", "bench")
        holder = make_entity(pikachu, "holder")
        bench_pokemon = make_entity(pikachu, "bench")
        board.add_card_to_area(holder, active_area)
        board.add_card_to_area(bench_pokemon, bench_area)
        holder.add_child(make_energy("fire-energy"))
        tool = make_entity(balloon_berry, "balloon-berry")
        holder.add_child(tool)

        entries = _retreat_entry(board, TurnState(turn_number=2), "player-1", "game-1")

        self.assertEqual(len(entries), 1)
        kinds = {info.get("name") for info in entries[0]["targetInfoLst"]}
        self.assertNotIn(SelectionKind.RETREAT_COST_ENTITY_LIST.value, kinds)
        self.assertIn(SelectionKind.RETREAT_NEW_ACTIVE.value, kinds)

    def test_retreat_offer_keeps_the_prompt_without_balloon_berry(self):
        board = BoardState("game-1", ["player-1", "player-2"])
        active_area = board.find_player_area("player-1", "activePokemonArea")
        bench_area = board.find_player_area("player-1", "bench")
        holder = make_entity(pikachu, "holder")
        bench_pokemon = make_entity(pikachu, "bench")
        board.add_card_to_area(holder, active_area)
        board.add_card_to_area(bench_pokemon, bench_area)
        holder.add_child(make_energy("fire-energy"))

        entries = _retreat_entry(board, TurnState(turn_number=2), "player-1", "game-1")

        self.assertEqual(len(entries), 1)
        kinds = {info.get("name") for info in entries[0]["targetInfoLst"]}
        self.assertIn(SelectionKind.RETREAT_COST_ENTITY_LIST.value, kinds)


if __name__ == "__main__":
    unittest.main()
