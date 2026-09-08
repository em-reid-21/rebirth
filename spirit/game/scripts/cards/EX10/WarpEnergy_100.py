from spirit.game.data_utils import EnergyCardDef
from spirit.game.attributes import PokemonTypes, Rarities
from spirit.game.session.effects import EffectContext

async def warp_energy_effect(ctx: EffectContext):
    """When you attach this card from your hand to your Active Pokémon, switch that Pokémon with 1 of your Benched Pokémon. ."""
    if ctx.attached_to is not ctx.my_active():
        return
    bench = ctx.my_bench()
    if not bench:
        return

    target = await ctx.choose_pokemon(
        bench, "Choose your new Active Pokémon"
    )
    if target is not None:
        await ctx.switch_active(ctx.player_id, target)

card = EnergyCardDef(
    guid="560dcc4a-a751-55f6-bda6-38db04a83eeb",
    key="EX10",
    name="Warp Energy",
    display_name="Warp Energy",
    searchable_by=["Warp Energy","Special","WarpEnergy"],
    subtypes=["Special"],
    collector_number=100,
    set_code="EX10",
    rarity=Rarities.Uncommon,
    energy_type=PokemonTypes.COLORLESS,
    is_special=True,
    on_attach=warp_energy_effect,
)
