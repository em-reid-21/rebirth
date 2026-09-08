from spirit.game.data_utils import ItemCardDef
from spirit.game.attributes import Rarities
from spirit.game.card_effects.trainers import someone_has_bench
from spirit.game.session.effects import EffectContext
from spirit.game.models.board import BoardState

"""Your opponent switches 1 of his or her Defending Pokemon with 1 of his or her Benched Pokemon, if any. You switch 1 of your Active Pokemon with 1 of your Benched Pokemon, if any."""

def warp_point_condition(board: BoardState, player_id: str, card=None) -> bool:
    """Check if there are any Benched Pokémon for either player to switch with."""
    return someone_has_bench(board, player_id)


async def warp_point_effect(ctx: EffectContext):
    """Switch the opponent's Active, then your Active, with a benched Pokémon if possible."""
    opponent_bench = ctx.opponent_bench()
    if opponent_bench:
        target = await ctx.choose_pokemon(
            opponent_bench, "Choose your new Active Pokémon", ctx.opponent_id
        )
        if target is not None:
            await ctx.switch_active(ctx.opponent_id, target)
            # Flush the opponent's swap so both clients see it land before
            # the Warp Point player is prompted for their own switch.
            await ctx.flush_choreography()

    my_bench = ctx.my_bench()
    if my_bench:
        target = await ctx.choose_pokemon(
            my_bench, "Choose your new Active Pokémon", ctx.player_id
        )
        if target is not None:
            await ctx.switch_active(ctx.player_id, target)

card = ItemCardDef(
    guid="f547b3da-a516-5663-91ef-7b624b6ec279",
    key="EX4",
    name="com.direwolfdigital.cake.data.archetypes.trainer.WarpPoint.Name",
    display_name="Warp Point",
    searchable_by=["Warp Point","Item","WarpPoint"],
    subtypes=["Item"],
    collector_number=85,
    set_code="EX4",
    rarity=Rarities.Uncommon,
    effect=warp_point_effect
)
