from spirit.game.data_utils import SupporterCardDef, is_pokemon_ex, unimplemented
from spirit.game.attributes import Rarities
from spirit.game.session.effects import EffectContext, full_stack

async def mr_brineys_compassion_effect(ctx: EffectContext):
    """ Choose 1 of your Pokémon in play (excluding Pokémon-ex). Return that Pokémon and all cards attached to it to your hand."""
    eligible_pokemon = [
        pokemon for pokemon in ctx.my_pokemon_in_play()
        if not is_pokemon_ex(pokemon.archetype_id)
    ]
    if not eligible_pokemon:
        return
    chosen_pokemon = await ctx.choose_pokemon(eligible_pokemon, prompt="Choose a Pokémon to return to your hand")
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

card = SupporterCardDef(
    guid="5b5fbb62-9deb-5d0f-b292-ea82dbc5d051",
    key="EX3",
    name="com.direwolfdigital.cake.data.archetypes.trainer.MrBrineysCompassion.Name",
    display_name="Mr. Briney's Compassion",
    searchable_by=["Mr. Briney's Compassion","Supporter","MrBrineysCompassion"],
    subtypes=["Supporter"],
    collector_number=87,
    set_code="EX3",
    rarity=Rarities.Uncommon,
    effect=mr_brineys_compassion_effect
)
