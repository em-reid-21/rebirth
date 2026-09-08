from spirit.game.data_utils import SupporterCardDef
from spirit.game.attributes import Rarities
from spirit.game.models.board import BoardState
from spirit.game.session.effects import EffectContext

def holon_scientist_condition(board: BoardState, player_id: str, card=None) -> bool:
    """Check if the player has at least one card in hand, in addition this card, to discard."""
    """Check if the player has less cards in hand than their opponent. If the player has more cards in hand than their opponent, they can't play this card."""
    hand = board.find_player_area(player_id, "hand")
    opponent_id = next((pid for pid in board.player_ids if pid != player_id), None)
    opponent_hand = board.find_player_area(opponent_id, "hand") if opponent_id else None
    return bool(
        hand
        and opponent_hand
        and len(hand.children) > 1
        and len(hand.children) < len(opponent_hand.children)
    )

async def holon_scientist_effect(ctx: EffectContext):
    """Draw cards until they have the same number of cards in hand as their opponent."""
    discarded = await ctx.discard_from_hand(
        1,
        minimum=1,
        prompt="Discard a card from your hand",
    )
    if not discarded:
        return

    opponent_hand_size = ctx.hand_size(ctx.opponent_id)
    await ctx.draw_until(opponent_hand_size)

card = SupporterCardDef(
    guid="195a4523-8cb3-5d4f-94fa-3f77d04ac369",
    key="EX11",
    name="com.direwolfdigital.cake.data.archetypes.trainer.HolonScientist.Name",
    display_name="Holon Scientist",
    searchable_by=["Holon Scientist","Supporter","HolonScientist"],
    subtypes=["Supporter"],
    collector_number=97,
    set_code="EX11",
    rarity=Rarities.Uncommon,
    effect=holon_scientist_effect,
    condition=holon_scientist_condition
)
