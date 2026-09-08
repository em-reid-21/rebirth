from spirit.game.data_utils import SupporterCardDef
from spirit.game.attributes import AttrID, Rarities
from spirit.game.session.effects import is_basic_pokemon
from spirit.game.session.effects import EffectContext
from spirit.game.session.game_session import BoardState

def holon_mentor_condition(board: BoardState, player_id: str, card=None) -> bool:
    """Check if the player has at least one card in hand, in addition this card, to discard."""
    hand = board.find_player_area(player_id, "hand")
    return bool(hand and len(hand.children) > 1)

def holon_mentor_matching(card):
    """Check if the card is a Basic Pokémon with 100 HP or less."""
    return is_basic_pokemon(card) and card.get_attribute(AttrID.HP) <= 100

async def holon_mentor_effect(ctx: EffectContext):
    """Discard a card from your hand.
    Search your deck for up to 3 Basic Pokémon that each has 100 HP or less, show them to your opponent, and put them into your hand. Shuffle your deck afterward."""
    discarded = await ctx.discard_from_hand(
        1,
        minimum=1,
        prompt="Discard a card from your hand",
    )
    if not discarded:
        return

    deck_cards = ctx.deck()
    pokemon_candidates = [card for card in deck_cards if holon_mentor_matching(card)]

    picks = await ctx.choose_cards(
        pokemon_candidates,
        3,
        minimum=0,
        prompt=(
            "Choose up to 3 Basic Pokémon that each has 100 HP or less."
        ),
        display_cards=deck_cards,
    )
    if picks:
        await ctx.put_in_hand(picks, reveal=True)
    await ctx.shuffle_deck()

card = SupporterCardDef(
    guid="96273697-7dfc-56d8-b71f-92b917da80cb",
    key="EX11",
    name="com.direwolfdigital.cake.data.archetypes.trainer.HolonMentor.Name",
    display_name="Holon Mentor",
    searchable_by=["Holon Mentor","Supporter","HolonMentor"],
    subtypes=["Supporter"],
    collector_number=93,
    set_code="EX11",
    rarity=Rarities.Uncommon,
    effect=holon_mentor_effect,
    condition=holon_mentor_condition
)
