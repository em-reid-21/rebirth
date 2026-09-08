from spirit.game.card_effects.attacks_common import self_energy_discard_attack
from spirit.game.data_utils import PokemonCardDef, Attack
from spirit.game.attributes import PokemonStage, PokemonTypes, Rarities
from spirit.game.models.board import PokemonEntity
from spirit.game.session.effects import EffectContext, is_stage2_pokemon
from typing import cast

async def miraculous_light_effect(ctx: EffectContext):
    """Remove 1 damage counter and all Special Conditions from Latios Star."""
    attacker = cast(PokemonEntity, ctx.attacker)
    await ctx.heal(10, attacker)
    await ctx.cure_all_conditions(attacker)

async def shining_star_effect(ctx: EffectContext):
    """If the Defending Pokémon is a Stage 2 Evolved Pokémon, discard all Energy cards attached to Latios Star and this attack does 50 damage plus 100 more damage."""
    defender = ctx.defender
    if defender is None:
        return
    if not is_stage2_pokemon(defender):
        await ctx.deal_damage(50, defender)
        return
    await self_energy_discard_attack(
        all_energy=True, before_damage=True, then_damage=50,
    )(ctx)
    await ctx.deal_damage(100, defender)

card = PokemonCardDef(
    guid="14aee23b-35f0-5da5-b738-e16c0b3aef1d",
    key="EX8",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Latios.Name",
    display_name="Latios ★",
    searchable_by=["Latios ★","Basic","Latios"],
    subtypes=["Basic", "Star"],
    collector_number=106,
    set_code="EX8",
    rarity=Rarities.RareHolo,
    hp=80,
    elements=[PokemonTypes.COLORLESS],
    stage=PokemonStage.BASIC,
    retreat_cost=1,
    weakness_type=PokemonTypes.COLORLESS,
    resistance_type=PokemonTypes.GRASS,
    abilities=[
        Attack(
            title="Miraculous Light",
            game_text="Remove 1 damage counter and all Special Conditions from Latios Star.",
            cost={PokemonTypes.COLORLESS: 1},
            damage=10,
            effect=miraculous_light_effect
        ),
        Attack(
            title="Shining Star",
            game_text="If the Defending Pokémon is a Stage 2 Evolved Pokémon, discard all Energy cards attached to Latios Star and this attack does 50 damage plus 100 more damage.",
            cost={PokemonTypes.GRASS: 1, PokemonTypes.LIGHTNING: 1, PokemonTypes.PSYCHIC: 1},
            damage=50,
            damage_operator="+",
            effect=shining_star_effect,
        ),
    ],
)
