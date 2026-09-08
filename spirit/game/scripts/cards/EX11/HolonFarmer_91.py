from typing import cast

from spirit.game.data_utils import SupporterCardDef
from spirit.game.attributes import Rarities
from spirit.game.card_effects.trainers import is_basic_energy_card
from spirit.game.models.board import BoardState, CardEntity
from spirit.game.session.effects import EffectContext, is_pokemon_card

def holon_farmer_condition(board: BoardState, player_id: str, card=None) -> bool:
    """Check if the player has at least one card in hand, in addition this card, to discard."""
    """Check if the player has at least one matching card in their discard pile to put on top of their deck."""
    hand = board.find_player_area(player_id, "hand")
    discard_pile = board.find_player_area(player_id, "discard")
    discard_cards = discard_pile.children if discard_pile else []
    discard_matches = discard_cards and any(
            is_pokemon_card(cast(CardEntity, c)) or is_basic_energy_card(cast(CardEntity, c))
            for c in discard_cards
        )
    return bool(hand and len(hand.children) > 1 and discard_matches)

async def holon_farmer_effect(ctx: EffectContext):
    """Search your discard pile for 3 basic Energy cards and any combination of 3 Basic Pokémon or Evolution cards, show them to your opponent, and put them on top of your deck. Shuffle your deck afterward. """
    discarded = await ctx.discard_from_hand(
        1,
        minimum=1,
        prompt="Discard a card from your hand",
    )
    if not discarded:
        return

    discard = ctx.discard_pile()
    energies = await ctx.choose_cards(
        [card for card in discard if is_basic_energy_card(card)],
        3,
        minimum=0,
        prompt="Choose up to 3 Basic Energy cards",
    )
    selected_ids = {card.entity_id for card in energies}
    pokemon = await ctx.choose_cards(
        [
            card for card in discard
            if card.entity_id not in selected_ids and is_pokemon_card(card)
        ],
        3,
        minimum=0,
        prompt="Choose up to 3 Basic or Evolution Pokémon",
    )
    selected = energies + pokemon
    await ctx.reveal_cards(selected)
    for card in selected:
        await ctx.put_on_top_of_deck(card)
    await ctx.shuffle_deck()

card = SupporterCardDef(
    guid="38f2715f-12ae-5e96-9eb4-6ec4a2aa8e65",
    key="EX11",
    name="com.direwolfdigital.cake.data.archetypes.trainer.HolonFarmer.Name",
    display_name="Holon Farmer",
    searchable_by=["Holon Farmer","Supporter","HolonFarmer"],
    subtypes=["Supporter"],
    collector_number=91,
    set_code="EX11",
    rarity=Rarities.Uncommon,
    effect=holon_farmer_effect,
    condition=holon_farmer_condition
)
