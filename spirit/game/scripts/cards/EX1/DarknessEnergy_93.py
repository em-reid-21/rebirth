from spirit.game.data_utils import EnergyCardDef
from spirit.game.attributes import AttrID, PokemonTypes, Rarities
from spirit.game.session.passives import Passive, carrier_pokemon


class DarknessEnergyPassive(Passive):
    def modify_damage_dealt(self, calc, carrier):
        if not (calc.is_attack and calc.is_opposing and calc.to_active):
            return
        holder = carrier_pokemon(carrier)
        if holder is None:
            return
        if holder is not calc.attacker:
            return
        types = holder.get_attribute(AttrID.POKEMON_TYPES) or []
        if PokemonTypes.DARKNESS.value in types:
            calc.amount += 10

"""If the Pokémon Darkness Energy is attached to attacks, the attack does 10 more damage to the Active Pokémon (before applying Weakness and Resistance). Ignore this effect if the Pokémon that Darkness Energy is attached to isn't [D]. Darkness Energy provides [D] Energy. (Doesn't count as a basic Energy card.)"""

card = EnergyCardDef(
    guid="9aa84bd8-c64d-5e0a-9dc4-ff9a09a9f0c1",
    key="EX1",
    name="Darkness Energy",
    display_name="Darkness Energy",
    searchable_by=["Darkness Energy","Special","DarknessEnergy"],
    subtypes=["Special"],
    collector_number=93,
    set_code="EX1",
    rarity=Rarities.Rare,
    energy_type=PokemonTypes.DARKNESS,
    is_special=True,
    passive=DarknessEnergyPassive(),
)
