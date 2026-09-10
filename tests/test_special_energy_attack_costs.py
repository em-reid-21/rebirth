import unittest

from spirit.game.attributes import AttrID, CardType, PokemonTypes
from spirit.game.models.board import BoardState, EnergyEntity, create_card_entity
from spirit.game.models.card import Card, PokemonCard
from spirit.game.scripts.cards.EX10.Meganiumex_106 import card as meganium
from spirit.game.scripts.cards.EX1.DarknessEnergy_93 import card as darkness_energy
from spirit.game.scripts.cards.EX11.HolonEnergyFF_104 import card as holon_energy_ff
from spirit.game.scripts.cards.EX11.HolonsVoltorb_71 import card as holons_voltorb
from spirit.game.scripts.cards.EX13.HolonsCastform_44 import card as holons_castform
from spirit.game.scripts.cards.EX2.MultiEnergy_93 import card as multi_energy
from spirit.game.scripts.cards.EX5.Jirachi_8 import card as jirachi
from spirit.game.scripts.cards.Free_Energy.FireEnergy_2 import card as fire_energy
from spirit.game.scripts.cards.Free_Energy.GrassEnergy_1 import card as grass_energy
from spirit.game.session.legal_actions import (
    ACTION_USE_ATTACK,
    TurnState,
    attack_cost_satisfied,
    compute_legal_actions,
)
from spirit.game.session.passives import compute_damage, energy_provided_options


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


def energy_entity(definition, entity_id):
    entity = create_card_entity(server_card(definition), "player-1", entity_id)
    if not isinstance(entity, EnergyEntity):
        entity.set_attribute(AttrID.CARD_TYPE, CardType.ENERGY.value)
        entity.__class__ = EnergyEntity
    return entity


class SpecialEnergyAttackCostTests(unittest.TestCase):
    def test_darkness_special_energy_does_not_pay_jirachi_mind_bend(self):
        mind_bend = next(attack for attack in jirachi.abilities if attack.title == "Mind Bend")

        self.assertFalse(
            attack_cost_satisfied(
                mind_bend.cost,
                [energy_entity(darkness_energy, "darkness-energy")],
            )
        )

    def test_darkness_special_energy_does_not_offer_jirachi_mind_bend(self):
        board = BoardState("game-1", ["player-1", "player-2"])
        attacker = create_card_entity(server_card(jirachi), "player-1", "jirachi")
        board.add_card_to_area(
            attacker,
            board.find_player_area("player-1", "activePokemonArea"),
        )
        attacker.add_child(energy_entity(darkness_energy, "darkness-energy"))
        state = TurnState(turn_number=2, active_player_id="player-1")

        offered_actions = compute_legal_actions(
            board, state, "player-1", "game-1"
        )

        self.assertFalse(
            any(
                entry["selectableAction"]["description"] == ACTION_USE_ATTACK
                for entry in offered_actions
            )
        )

    def test_holons_voltorb_does_not_pay_jirachi_mind_bend(self):
        mind_bend = next(attack for attack in jirachi.abilities if attack.title == "Mind Bend")

        self.assertFalse(
            attack_cost_satisfied(
                mind_bend.cost,
                [energy_entity(holons_voltorb, "holons-voltorb")],
            )
        )

    def test_holons_castform_and_multi_energy_pay_meganium_power_poison(self):
        power_poison = next(attack for attack in meganium.abilities if attack.title == "Power Poison")
        board = BoardState("game-1", ["player-1", "player-2"])
        attacker = create_card_entity(server_card(meganium), "player-1", "meganium")
        board.add_card_to_area(
            attacker,
            board.find_player_area("player-1", "activePokemonArea"),
        )
        attached = [
            energy_entity(grass_energy, "grass-1"),
            energy_entity(grass_energy, "grass-2"),
            energy_entity(multi_energy, "multi-energy"),
            energy_entity(holons_castform, "holons-castform"),
        ]
        for energy in attached:
            attacker.add_child(energy)

        self.assertTrue(attack_cost_satisfied(power_poison.cost, attached, board))
        self.assertEqual(
            energy_provided_options(board, attached[2]),
            [[PokemonTypes.COLORLESS.value]],
        )

    def test_holon_ff_and_basic_fire_energy_remove_weakness(self):
        board = BoardState("game-1", ["player-1", "player-2"])
        holder = create_card_entity(server_card(jirachi), "player-1", "holder")
        attacker = create_card_entity(server_card(jirachi), "player-2", "attacker")
        board.add_card_to_area(
            holder,
            board.find_player_area("player-1", "activePokemonArea"),
        )
        board.add_card_to_area(
            attacker,
            board.find_player_area("player-2", "activePokemonArea"),
        )
        holder.set_attribute(AttrID.WEAKNESS_TYPES, [PokemonTypes.FIRE.value])
        attacker.set_attribute(AttrID.POKEMON_TYPES, [PokemonTypes.FIRE.value])

        baseline = compute_damage(board, attacker, holder, 30)
        self.assertEqual(baseline.amount, 60)
        self.assertTrue(baseline.weakness_hit)

        holon = energy_entity(holon_energy_ff, "holon-energy-ff")
        fire = energy_entity(fire_energy, "fire-energy")
        holder.add_child(holon)
        holder.add_child(fire)

        protected = compute_damage(board, attacker, holder, 30)
        self.assertEqual(protected.amount, 30)
        self.assertFalse(protected.weakness_hit)


if __name__ == "__main__":
    unittest.main()