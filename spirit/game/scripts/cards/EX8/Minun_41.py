from spirit.game.card_effects.support_common import recover_from_discard
from spirit.game.data_utils import PokemonCardDef, Attack, unimplemented
from spirit.game.attributes import AttrID, PokemonStage, PokemonTypes, Rarities

def has_poke_body(pokemon) -> bool:
    abilities = pokemon.get_attribute(AttrID.PIE_ABILITIES) or []
    return any(isinstance(e, dict) and e.get("abilityType") == "PokeBody"
               for e in abilities)

async def negative_spark_effect(ctx):
    for pokemon in ctx.opponent_pokemon_in_play():
        if has_poke_body(pokemon):
            await ctx.deal_damage(
                20, target=pokemon,
                ignore_weakness=True, ignore_resistance=True,
            )

card = PokemonCardDef(
    guid="d616de21-6170-50d5-8159-bffbaab4da0c",
    key="EX8",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Minun.Name",
    display_name="Minun",
    searchable_by=["Minun","Basic","Minun"],
    subtypes=["Basic"],
    collector_number=41,
    set_code="EX8",
    rarity=Rarities.Uncommon,
    hp=60,
    elements=[PokemonTypes.LIGHTNING],
    stage=PokemonStage.BASIC,
    retreat_cost=1,
    weakness_type=PokemonTypes.FIGHTING,
    abilities=[
        Attack(
            title="Sniff Out",
            game_text="Put any 1 card from your discard pile into your hand.",
            cost={PokemonTypes.COLORLESS: 1},
            effect=recover_from_discard(count=1, minimum=1, reveal=True, to="hand"),
        ),
        Attack(
            title="Negative Spark",
            game_text="Does 20 damage to each of your opponent's Pokémon that has any Poké-Bodies. Don't apply Weakness and Resistance.",
            cost={PokemonTypes.LIGHTNING: 1},
            effect=negative_spark_effect,
        ),
    ],
)
