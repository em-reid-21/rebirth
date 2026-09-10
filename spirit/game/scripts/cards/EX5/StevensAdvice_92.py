from spirit.game.data_utils import SupporterCardDef
from spirit.game.attributes import Rarities
from spirit.game.models.board import BoardState, PokemonEntity
from spirit.game.session.effects import EffectContext


def stevens_advice_condition(board: BoardState, player_id: str, pokemon: PokemonEntity):
    """If you have more than 7 cards (including this one) in your hand, you can't play this card."""
    hand = board.find_player_area(player_id, "hand")
    return hand is not None and len(hand.children) <= 7

    
async def stevens_advice_effect(ctx: EffectContext):
    """Draw a number of cards up to the number of your opponent's Pokémon in play.
If you have more than 7 cards (including this one) in your hand, you can't play this card."""
    opponent_pokemon_count = len(ctx.opponent_pokemon_in_play())
    player_draw = await ctx.choose(
        "Choose how many cards to draw.",
        [str(i) for i in range(1, opponent_pokemon_count + 1)],
        player_id=ctx.player_id,
        use_panel=False,
    )
    await ctx.draw_cards(int(player_draw))


card = SupporterCardDef(
    guid="25e2b4fb-8b58-5b04-a194-09894b6545c3",
    key="EX5",
    name="com.direwolfdigital.cake.data.archetypes.trainer.StevensAdvice.Name",
    display_name="Steven's Advice",
    searchable_by=["Steven's Advice","Supporter","StevensAdvice"],
    subtypes=["Supporter"],
    collector_number=92,
    set_code="EX5",
    rarity=Rarities.Uncommon,
    effect=stevens_advice_effect,
    condition=stevens_advice_condition
)
