from spirit.game.data_utils import PokemonToolCardDef, is_pokemon_ex
from spirit.game.attributes import Rarities
from spirit.game.card_effects.passives_common import ability_lock_passive, is_in_active_spot
from spirit.game.models.board import PokemonEntity
from spirit.game.session.passives import carrier_pokemon

"""As long as Cessation Crystal is attached to an Active Pokémon, each player's Pokémon (both yours and your opponent's) can't use any Poké-Powers or Poké-Bodies."""
"""Attach Cessation Crystal to 1 of your pokemon (excluding pokemon ex) that doesn't already have a tool attached to it. If the Pokémon Cessation Crystal is attached to is a pokemon ex, discard this cards"""

def _cessation_crystal_target(pokemon: PokemonEntity, carrier: PokemonEntity) -> bool:
    holder = carrier_pokemon(carrier)
    return holder is not None and is_in_active_spot(holder)


def _cessation_crystal_attach_to(pokemon: PokemonEntity):
    return not is_pokemon_ex(pokemon.archetype_id)


card = PokemonToolCardDef(
    passive=ability_lock_passive(_cessation_crystal_target),
    guid="bb431f97-354d-50ef-861f-38d9c248a1e2",
    key="EX14",
    name="com.direwolfdigital.cake.data.archetypes.trainer.CessationCrystal.Name",
    display_name="Cessation Crystal",
    searchable_by=["Cessation Crystal","Pokémon Tool","Tool","CessationCrystal"],
    subtypes=["Pokémon Tool","Tool"],
    collector_number=74,
    set_code="EX14",
    rarity=Rarities.Uncommon,
    attach_to=_cessation_crystal_attach_to,
)
