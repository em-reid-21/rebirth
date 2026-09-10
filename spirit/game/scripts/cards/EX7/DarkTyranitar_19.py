from spirit.game.data_utils import PokemonCardDef, Attack, is_pokemon_ex, unimplemented
from spirit.game.attributes import PokemonStage, PokemonTypes, Rarities
from spirit.game.session.effects import EffectContext
from spirit.game.card_effects.attacks_common import damage_all_opponents, damage_per, count_energy

async def bite_off_effect(ctx: EffectContext):
    """If the Defending Pokémon is Pokémon-ex, this attack does 70 damage plus 50 more damage."""
    defender = ctx.defender
    if defender is None:
        return
    if is_pokemon_ex(defender.archetype_id):
        await ctx.deal_damage(70 + 50, defender)
    else:
        await ctx.deal_damage()

card = PokemonCardDef(
    guid="fdfdd40a-1cb5-5ffa-bf78-a0a5303cc0cc",
    key="EX7",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.DarkTyranitar.Name",
    display_name="Dark Tyranitar",
    searchable_by=["Dark Tyranitar","Stage 2","DarkTyranitar"],
    subtypes=["Stage 2"],
    collector_number=19,
    set_code="EX7",
    rarity=Rarities.Rare,
    hp=120,
    elements=[PokemonTypes.DARKNESS],
    stage=PokemonStage.STAGE2,
    retreat_cost=2,
    weakness_type=PokemonTypes.FIGHTING,
    resistance_type=PokemonTypes.PSYCHIC,
    evolves_from="com.direwolfdigital.cake.data.archetypes.pokemon.DarkPupitar.Name",
    abilities=[
        Attack(
            title="Grind",
            game_text="Does 10 damage plus 10 more damage for each Energy attached to Dark Tyranitar.",
            cost={PokemonTypes.COLORLESS: 1},
            damage=10,
            damage_operator="+",
            effect=damage_per(count_energy("self"), 10, base=10),
        ),
        Attack(
            title="Spinning Tail",
            game_text="Does 20 damage to each of your opponent's Pokémon. (Don't apply Weakness and Resistance for Benched Pokémon.)",
            cost={PokemonTypes.DARKNESS: 1, PokemonTypes.COLORLESS: 2},
            effect=damage_all_opponents(20),
        ),
        Attack(
            title="Bite Off",
            game_text="If the Defending Pokémon is Pokémon-ex, this attack does 70 damage plus 50 more damage.",
            cost={PokemonTypes.DARKNESS: 2, PokemonTypes.COLORLESS: 3},
            damage=70,
            damage_operator="+",
            effect=bite_off_effect,
        ),
    ],
)
