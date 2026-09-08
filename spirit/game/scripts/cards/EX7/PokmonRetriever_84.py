from spirit.game.data_utils import ItemCardDef, subtypes_for
from spirit.game.attributes import Rarities
from spirit.game.models.board import BoardState
from spirit.game.session.effects import EffectContext, is_pokemon_card

"""Search your discard pile for Basic Pokémon and Evolution cards. You may either show 1 Basic Pokémon or Evolution card to your opponent and put it into your hand, or show a combination of 3 Basic Pokémon or Evolution cards to your opponent and shuffle them into your deck."""

def pokmon_retriever_condition(board: BoardState, player_id: str, card=None) -> bool:
    """Check if there are any Basic Pokémon or Evolution cards in the player's discard pile."""
    discard = board.find_player_area(player_id, "discard")
    return bool(discard and any(_is_retrievable(card) for card in discard.children))

def _is_retrievable(card):
    return is_pokemon_card(card) and (
        "Basic" in subtypes_for(card.archetype_id)
        or "Stage 1" in subtypes_for(card.archetype_id)
        or "Stage 2" in subtypes_for(card.archetype_id)
    )


async def pokmon_retriever_effect(ctx: EffectContext):
    """Put one eligible Pokémon into hand, or shuffle three into the deck."""
    candidates = [card for card in ctx.discard_pile() if _is_retrievable(card)]
    if not candidates:
        return

    choices = ["Put 1 Pokémon into your hand", "Shuffle 3 Pokémon into your deck"]
    choice = await ctx.choose(
        "Choose how to use Pokémon Retriever",
        choices,
    )

    if choice == 0:
        picks = await ctx.choose_cards(
            candidates,
            1,
            minimum=1,
            prompt="Choose a Pokémon to put into your hand",
        )
        if picks:
            await ctx.reveal_cards(picks)
            await ctx.put_in_hand(picks, reveal=False)
        return

    picks = await ctx.choose_cards(
        candidates,
        3,
        minimum=3,
        prompt="Choose 3 Pokémon to shuffle into your deck",
    )
    if picks:
        await ctx.reveal_cards(picks)
        await ctx.shuffle_into_deck(picks)
    
card = ItemCardDef(
    guid="c2824a97-1f80-5265-9046-a88d3763f435",
    key="EX7",
    name="com.direwolfdigital.cake.data.archetypes.trainer.PokmonRetriever.Name",
    display_name="Pokémon Retriever",
    searchable_by=["Pokémon Retriever","Rocket's Secret Machine","PokmonRetriever"],
    subtypes=["Rocket's Secret Machine"],
    collector_number=84,
    set_code="EX7",
    rarity=Rarities.Uncommon,
    effect=pokmon_retriever_effect,
    condition=pokmon_retriever_condition
)
