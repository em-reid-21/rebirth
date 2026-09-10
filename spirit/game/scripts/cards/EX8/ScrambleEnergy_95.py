from itertools import combinations_with_replacement

from spirit.game.card_effects.energies import ALL_TYPES_ONE_AT_A_TIME
from spirit.game.data_utils import EnergyCardDef
from spirit.game.attributes import AttrID, PokemonStage, PokemonTypes, Rarities
from spirit.game.data_utils import is_pokemon_ex
from spirit.game.session.passives import Passive, carrier_pokemon

""" Scramble Energy can be attached only to an Evolved Pokémon (excluding Pokémon-ex). Scramble Energy provides [C] Energy. While in play, if you have more Prize cards left than your opponent, Scramble Energy provides every type of Energy but provides only 3 in any combination at a time. If the Pokémon Scramble Energy is attached to isn't an Evolved Pokémon (or evolves into Pokémon-ex), discard Scramble Energy. """

ALL_TYPES_THREE_AT_A_TIME = [
    [option[0].value, option[0].value, option[0].value] for option in ALL_TYPES_ONE_AT_A_TIME
]

def _is_evolved_non_ex(pokemon):
    return (
        pokemon.get_attribute(AttrID.STAGE, PokemonStage.BASIC.value)
        != PokemonStage.BASIC.value
        and not is_pokemon_ex(pokemon.archetype_id)
    )


class ScrambleEnergyPassive(Passive):
    def modify_energy_provided(self, options, energy, holder, board):
        if carrier_pokemon(energy) is not holder or holder is None:
            return options
        if holder.owning_player_id is None:
            return options
        owner_prizes = board.find_player_area(holder.owning_player_id, "prizePile")
        opponent_id = next(
            player_id
            for player_id in board.player_ids
            if player_id != holder.owning_player_id
        )
        opponent_prizes = board.find_player_area(opponent_id, "prizePile")
        if owner_prizes is not None and opponent_prizes is not None \
                and len(owner_prizes.children) > len(opponent_prizes.children):
            return ALL_TYPES_THREE_AT_A_TIME
        return options

card = EnergyCardDef(
    guid="5fba8084-7296-5ddc-b42b-c24c7454d384",
    key="EX8",
    name="Scramble Energy",
    display_name="Scramble Energy",
    searchable_by=["Scramble Energy","Special","ScrambleEnergy"],
    subtypes=["Special"],
    collector_number=95,
    set_code="EX8",
    rarity=Rarities.Uncommon,
    energy_type=PokemonTypes.COLORLESS,
    is_special=True,
    provides=[[PokemonTypes.COLORLESS]],
    attach_to=_is_evolved_non_ex,
    passive=ScrambleEnergyPassive(),
)
