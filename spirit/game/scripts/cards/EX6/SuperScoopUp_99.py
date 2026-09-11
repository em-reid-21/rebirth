from spirit.game.data_utils import ItemCardDef, is_pokemon_ex, unimplemented
from spirit.game.attributes import Rarities
from spirit.game.session.effects import EffectContext, full_stack

async def super_scoop_up_effect(ctx: EffectContext):
    results = await ctx.flip_coins(1, "Super Scoop Up")
    if not results or not results[0]:
        return
    chosen_pokemon = await ctx.choose_pokemon(ctx.my_pokemon_in_play(), prompt="Choose a Pokémon to return to your hand")
    if chosen_pokemon is None:
        return
    was_active = chosen_pokemon is ctx.my_active()
    await ctx.put_in_hand(full_stack(chosen_pokemon), reveal=False)
    if was_active:
        async def _promote():
            if not await ctx.session._promote_new_active(ctx.player_id):
                screen_name = ctx.session.players[ctx.player_id].screen_name
                await ctx.session.end_game(
                    ctx.opponent_id, f"{screen_name} has no Pokémon left"
                )
        ctx.deferred_actions.append(_promote)

card = ItemCardDef(
    guid="841eb7e9-b705-5ba1-a513-5f592b470660",
    key="EX6",
    name="com.direwolfdigital.cake.data.archetypes.trainer.SuperScoopUp.Name",
    display_name="Super Scoop Up",
    searchable_by=["Super Scoop Up","Item","SuperScoopUp"],
    subtypes=["Item"],
    collector_number=99,
    set_code="EX6",
    rarity=Rarities.Uncommon,
    effect=super_scoop_up_effect
)
