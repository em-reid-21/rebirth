from spirit.game.data_utils import SupporterCardDef, def_for
from spirit.game.attributes import Rarities
from spirit.game.card_effects.trainers import is_metal_energy_card
from spirit.game.models.board import BoardState
from spirit.game.session.effects import EffectContext, is_pokemon_card
from spirit.game.card_effects.support_common import search_to_hand

def holon_researcher_condition(board: BoardState, player_id: str, card=None) -> bool:
    """Check if the player has at least one card in hand, in addition this card, to discard."""
    hand = board.find_player_area(player_id, "hand")
    return bool(hand and len(hand.children) > 1)

def _has_delta_on_card(card):
    definition = def_for(card.archetype_id)
    return definition is not None and "Delta Species" in definition.subtypes

def _is_researcher_target(card):
    return is_metal_energy_card(card) or (
        is_pokemon_card(card) and _has_delta_on_card(card)
    )

async def holon_researcher_effect(ctx: EffectContext):
    """Search your deck for a [M] Energy card or a Basic Pokémon (or Evolution card) that has δ on its card, show it to your opponent, and put it into your hand. Shuffle your deck afterward."""
    discarded = await ctx.discard_from_hand(
        1,
        minimum=1,
        prompt="Discard a card from your hand",
    )
    if not discarded:
        return

    await search_to_hand(
        _is_researcher_target,
        count=1,
        minimum=0,
        reveal=True,
        prompt="Choose a Metal Energy or a Delta Species Pokémon",
    )(ctx)

card = SupporterCardDef(
    guid="735f78ef-f7c2-523e-a612-92b4ffe40595",
    key="EX11",
    name="com.direwolfdigital.cake.data.archetypes.trainer.HolonResearcher.Name",
    display_name="Holon Researcher",
    searchable_by=["Holon Researcher","Supporter","HolonResearcher"],
    subtypes=["Supporter"],
    collector_number=95,
    set_code="EX11",
    rarity=Rarities.Uncommon,
    effect=holon_researcher_effect,
    condition=holon_researcher_condition
)
