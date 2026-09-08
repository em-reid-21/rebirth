from spirit.game.data_utils import PokemonCardDef, Attack, unimplemented
from spirit.game.attributes import PokemonStage, PokemonTypes, Rarities
from spirit.game.session.effects import EffectContext

def whirlwind_effect(ctx: EffectContext):
    """Your opponent switches the Defending Pokémon with 1 of his or her Benched Pokémon."""
    ctx.session.turn_state.switch_effects.append(
        lambda source, target: ctx.board.switch_defending_pokemon()
        if source == ctx.source else None
    )

card = PokemonCardDef(
    guid="09623014-f36d-50f0-9ac4-0a9ce2ff6efb",
    key="EX13",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Pidgeotto.Name",
    display_name="Pidgeotto δ",
    searchable_by=["Pidgeotto δ","Stage 1","Pidgeotto"],
    subtypes=["Stage 1", "Delta Species"],
    collector_number=49,
    set_code="EX13",
    rarity=Rarities.Uncommon,
    hp=70,
    elements=[PokemonTypes.LIGHTNING],
    stage=PokemonStage.STAGE1,
    retreat_cost=1,
    weakness_type=PokemonTypes.LIGHTNING,
    resistance_type=PokemonTypes.FIGHTING,
    evolves_from="com.direwolfdigital.cake.data.archetypes.pokemon.Pidgey.Name",
    abilities=[
        Attack(
            title="Whirlwind",
            game_text="Your opponent switches the Defending Pokémon with 1 of his or her Benched Pokémon.",
            cost={PokemonTypes.LIGHTNING: 1, PokemonTypes.COLORLESS: 1},
            damage=30,
            effect=whirlwind_effect,
        ),
    ],
)
