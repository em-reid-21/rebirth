from spirit.game.data_utils import SupporterCardDef
from spirit.game.attributes import Rarities
from spirit.game.session.effects import EffectContext


async def rockets_admin_effect(ctx: EffectContext):
    """Each player shuffles his or her hand into his or her deck. Then,
    each player counts his or her Prize cards left and chooses to draw up to
    that many cards. (You draw your cards first.)"""
    player_prizes = len(ctx.board.find_player_area(ctx.player_id, "prizePile").children)
    opponent_prizes = len(ctx.board.find_player_area(ctx.opponent_id, "prizePile").children)

    await ctx.shuffle_into_deck(ctx.hand(), ctx.player_id)
    player_draw = await ctx.choose(
        "Choose how many cards to draw.",
        [str(i) for i in range(1, player_prizes + 1)],
        player_id=ctx.player_id,
        use_panel=False,
    )
    # ctx.choose returns the index of the selected option, so add 1 to get the actual number of cards to draw.
    await ctx.draw_cards(player_draw + 1, ctx.player_id)

    await ctx.flush_choreography()

    await ctx.shuffle_into_deck(ctx.hand(ctx.opponent_id), ctx.opponent_id)
    opponent_draw = await ctx.choose(
        "Choose how many cards to draw.",
        [str(i) for i in range(1, opponent_prizes + 1)],
        player_id=ctx.opponent_id,
        use_panel=False,
    )
    await ctx.draw_cards(opponent_draw + 1, ctx.opponent_id)

card = SupporterCardDef(
    guid="c3c090b0-c699-54e5-ab59-60890a9c6fd6",
    key="EX7",
    name="com.direwolfdigital.cake.data.archetypes.trainer.RocketsAdmin.Name",
    display_name="Rocket's Admin.",
    searchable_by=["Rocket's Admin.","Supporter","RocketsAdmin"],
    subtypes=["Supporter"],
    collector_number=86,
    set_code="EX7",
    rarity=Rarities.Uncommon,
    effect=rockets_admin_effect
)
