from spirit.game.data_utils import EnergyCardDef
from spirit.game.attributes import AttrID, PokemonTypes, Rarities
from spirit.game.card_effects.pokemon import energy_provides_type
from spirit.game.data_utils import is_pokemon_ex
from spirit.game.session.passives import Passive, carrier_pokemon

""" Holon Energy FF provides [C] Energy.
If the Pokémon that Holon Energy FF is attached to also has a basic [R] Energy card attached to it, that Pokémon has no Weakness. If the Pokémon that Holon Energy FF is attached to also has a basic [F] Energy card attached to it, damage done by that Pokémon's attack isn't affected by Resistance. Ignore these effects if Holon Energy FF is attached to Pokémon-ex. """


def _has_basic_energy(holder, energy_type):
    return any(
        not energy.get_attribute(AttrID.IS_SPECIAL_ENERGY)
        and energy_provides_type(energy, energy_type.value)
        for energy in holder.children
    )


class HolonEnergyFFPassive(Passive):
    def _active_for(self, carrier):
        holder = carrier_pokemon(carrier)
        if holder is None or is_pokemon_ex(holder.archetype_id):
            return None
        return holder

    def modify_weakness(self, calc, carrier):
        holder = self._active_for(carrier)
        if holder is calc.target and _has_basic_energy(
            holder, PokemonTypes.FIRE
        ):
            calc.weakness_applies = False

    def modify_resistance(self, calc, carrier):
        holder = self._active_for(carrier)
        if holder is not calc.attacker or not calc.is_attack or not calc.is_opposing:
            return
        if _has_basic_energy(holder, PokemonTypes.FIGHTING):
            calc.resistance_applies = False

card = EnergyCardDef(
    guid="0f2eb03f-7fb1-5ac2-be23-cfd5facb9a59",
    key="EX11",
    name="Holon Energy FF",
    display_name="Holon Energy FF",
    searchable_by=["Holon Energy FF","Special","HolonEnergyFF"],
    subtypes=["Special"],
    collector_number=104,
    set_code="EX11",
    rarity=Rarities.Rare,
    energy_type=PokemonTypes.COLORLESS,
    is_special=True,
    provides=[[PokemonTypes.COLORLESS]],
    passive=HolonEnergyFFPassive(),
)
