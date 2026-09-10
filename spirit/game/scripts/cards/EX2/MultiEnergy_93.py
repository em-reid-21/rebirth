from spirit.game.card_effects.energies import ALL_TYPES_ONE_AT_A_TIME
from spirit.game.data_utils import EnergyCardDef, def_for
from spirit.game.attributes import PokemonTypes, Rarities
from spirit.game.session.effects import is_special_energy
from spirit.game.session.passives import Passive, carrier_pokemon

"""Attach Multi Energy to 1 of your Pokémon. While in play, Multi Energy provides every type of Energy but provides only 1 Energy at a time. (Doesn't count as a basic Energy card when not in play.) Multi energy provides [C] Energy when attached to a Pokémon that already has Special Energy cards attached to it."""


class MultiEnergyPassive(Passive):
    """Multi Energy becomes Colorless when another Special Energy shares its carrier."""

    def modify_energy_provided(self, options, energy, holder, board):
        definition = def_for(energy.archetype_id)
        if definition is None or definition.passive is not self \
                or carrier_pokemon(energy) is not holder or holder is None:
            return options
        has_other_special = any(
            attached is not energy
            and is_special_energy(attached)
            for attached in board.attached_energies(holder)
        )
        if has_other_special:
            return [[PokemonTypes.COLORLESS.value]]
        return options

card = EnergyCardDef(
    guid="b5e37251-ca98-54ae-9523-71a9cc154292",
    key="EX2",
    name="Multi Energy",
    display_name="Multi Energy",
    searchable_by=["Multi Energy","Special","MultiEnergy"],
    subtypes=["Special"],
    collector_number=93,
    set_code="EX2",
    rarity=Rarities.Rare,
    energy_type=PokemonTypes.COLORLESS,
    is_special=True,
    provides=ALL_TYPES_ONE_AT_A_TIME,
    passive=MultiEnergyPassive(),
)
