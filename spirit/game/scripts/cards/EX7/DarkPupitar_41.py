from spirit.game.data_utils import PokemonCardDef, Attack, unimplemented
from spirit.game.attributes import PokemonStage, PokemonTypes, Rarities, SpecialConditions
from spirit.game.card_effects.attacks_common import condition_attack, flip_damage
from spirit.game.session.effects import EffectContext

async def rock_tumble(ctx: EffectContext):
    await ctx.deal_damage(ignore_resistance=True)

card = PokemonCardDef(
    guid="a9ee1159-674e-517c-be7b-780be8e27f8a",
    key="EX7",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.DarkPupitar.Name",
    display_name="Dark Pupitar",
    searchable_by=["Dark Pupitar","Stage 1","DarkPupitar"],
    subtypes=["Stage 1"],
    collector_number=41,
    set_code="EX7",
    rarity=Rarities.Uncommon,
    hp=80,
    elements=[PokemonTypes.FIGHTING, PokemonTypes.DARKNESS],
    stage=PokemonStage.STAGE1,
    retreat_cost=2,
    weakness_type=PokemonTypes.GRASS,
    evolves_from="com.direwolfdigital.cake.data.archetypes.pokemon.Larvitar.Name",
    abilities=[
        Attack(
            title="Dark Streak",
            game_text="Flip a coin. If heads, each Defending Pokémon is now Paralyzed.",
            cost={PokemonTypes.COLORLESS: 2},
            damage=20,
            effect=condition_attack(SpecialConditions.PARALYZED, flip=True),
        ),
        Attack(
            title="Rock Tumble",
            game_text="This attack's damage is not affected by Resistance.",
            cost={PokemonTypes.FIGHTING: 1, PokemonTypes.COLORLESS: 2},
            damage=40,
            effect=rock_tumble,
        ),
    ],
)
