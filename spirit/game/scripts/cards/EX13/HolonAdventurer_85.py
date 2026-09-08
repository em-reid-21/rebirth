from spirit.game.data_utils import SupporterCardDef, def_for
from spirit.game.attributes import Rarities
from spirit.game.models.board import BoardState
from spirit.game.session.effects import EffectContext

def holon_adventurer_condition(board: BoardState, player_id: str, card=None) -> bool:
    """Check if the player has at least one card in hand, in addition this card, to discard."""
    hand = board.find_player_area(player_id, "hand")
    return bool(hand and len(hand.children) > 1)


async def holon_adventurer(ctx: EffectContext):
    """Draw 3 cards. If you discarded a Pokémon that has δ on its card, draw 4 cards instead. """
    discarded = await ctx.discard_from_hand(
        1,
        minimum=1,
        prompt="Discard a card from your hand",
    )
    if not discarded:
        return

    definition = def_for(discarded[0].archetype_id)
    if definition is not None and "Delta Species" in definition.subtypes:
        await ctx.draw_cards(4)
    else:
        await ctx.draw_cards(3)

card = SupporterCardDef(
    guid="8312838c-e731-5380-b37e-b6dbadc725fc",
    key="EX13",
    name="com.direwolfdigital.cake.data.archetypes.trainer.HolonAdventurer.Name",
    display_name="Holon Adventurer",
    searchable_by=["Holon Adventurer","Supporter","HolonAdventurer"],
    subtypes=["Supporter"],
    collector_number=85,
    set_code="EX13",
    rarity=Rarities.Uncommon,
    effect=holon_adventurer,
    condition=holon_adventurer_condition
)
