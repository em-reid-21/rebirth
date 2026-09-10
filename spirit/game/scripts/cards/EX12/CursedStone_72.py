from spirit.game.attributes import AttrID, Rarities
from spirit.game.data_utils import Ability, StadiumCardDef, Triggers
from spirit.game.models.board import PokemonEntity
from spirit.game.session.effects import EffectContext

"""At any time between turns, each player puts 1 damage counter on his or her Pokémon that has a Poké-Power."""

def cursed_stone_targets(pokemon_list: list[PokemonEntity]) -> list[PokemonEntity]:
    targets = []
    for pokemon in pokemon_list:
        entries = pokemon.get_attribute(AttrID.PIE_ABILITIES) or []
        if any(
            isinstance(entry, dict)
            and entry.get("abilityType") in ("PokeAbility", "PokePower")
            for entry in entries
        ):
            targets.append(pokemon)
    return targets


async def cursed_stone(ctx: EffectContext):
    for player_id in ctx.session._turn_order():
        for pokemon in cursed_stone_targets(ctx.session.board_state.pokemon_in_play(player_id)):
            await ctx.deal_damage(10, target=pokemon, apply_modifiers=False, as_counters=True)


card = StadiumCardDef(
    guid="e8bf4f78-75fa-56e8-8cf1-386a6fe3710a",
    key="EX12",
    name="com.direwolfdigital.cake.data.archetypes.trainer.CursedStone.Name",
    display_name="Cursed Stone",
    searchable_by=["Cursed Stone","Stadium","CursedStone"],
    subtypes=["Stadium"],
    collector_number=72,
    set_code="EX12",
    rarity=Rarities.Uncommon,
    abilities=[
        Ability(
            title="Cursed Stone",
            game_text="At any time between turns, each player puts 1 damage counter on his or her Pokémon that has a Poké-Power.",
            trigger=Triggers.BETWEEN_TURNS,
            effect=cursed_stone,
        ),
    ],
)
