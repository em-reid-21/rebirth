from spirit.game.card_effects.energies import ALL_TYPES_ONE_AT_A_TIME
from spirit.game.data_utils import EnergyCardDef, def_for
from spirit.game.attributes import PokemonTypes, Rarities
from spirit.game.session.passives import Passive, carrier_pokemon

""" δ Rainbow Energy provides [C] Energy. While attached to a Pokémon that has δ on its card, δ Rainbow Energy provides every type of Energy but provides only 1 Energy at a time. (Has no effect other than providing Energy.) """


class DeltaRainbowEnergyPassive(Passive):
    """Provides every type when attached to a Delta Species Pokémon."""

    def modify_energy_provided(self, options, energy, holder, board):
        if carrier_pokemon(energy) is not holder or holder is None:
            return options
        definition = def_for(holder.archetype_id)
        if definition is not None and "Delta Species" in definition.subtypes:
            return [[option[0].value] for option in ALL_TYPES_ONE_AT_A_TIME]
        return options

card = EnergyCardDef(
    guid="18e07f45-2ba3-57eb-a0d1-17e0845c4c39",
    key="EX13",
    name="δ Rainbow Energy",
    display_name="δ Rainbow Energy",
    searchable_by=["δ Rainbow Energy","Special","RainbowEnergy"],
    subtypes=["Special"],
    collector_number=98,
    set_code="EX13",
    rarity=Rarities.Uncommon,
    energy_type=PokemonTypes.COLORLESS,
    is_special=True,
    passive=DeltaRainbowEnergyPassive(),
)
