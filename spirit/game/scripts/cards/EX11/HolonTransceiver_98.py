from spirit.game.data_utils import ItemCardDef, def_for
from spirit.game.attributes import Rarities
from spirit.game.card_effects.support_common import search_to_hand
from spirit.game.session.effects import EffectContext, is_supporter_card

def _is_holon_supporter(card):
    if not is_supporter_card(card):
        return False
    definition = def_for(card.archetype_id)
    name = getattr(definition, "display_name", "") or ""
    return "Holon" in name


async def holon_transceiver_effect(ctx: EffectContext):
    """Search for a Holon Supporter in the deck or discard pile."""
    discard_targets = [card for card in ctx.discard_pile() if _is_holon_supporter(card)]

    if discard_targets:
        choice = await ctx.choose(
            "Choose where to search for a Holon Supporter",
            ["Search your deck", "Search your discard pile"],
        )
        if choice == 1:
            picked = await ctx.choose_cards(
                discard_targets,
                1,
                minimum=0,
                prompt="Choose a Holon Supporter to put into your hand",
            )
            if picked:
                await ctx.put_in_hand(picked, reveal=True)
            return

    await search_to_hand(
        _is_holon_supporter,
        count=1,
        minimum=0,
        reveal=True,
        prompt="Choose a Holon Supporter to put into your hand",
    )(ctx)

card = ItemCardDef(
    guid="04caf74a-9cd8-5f0e-804e-cea91f974739",
    key="EX11",
    name="com.direwolfdigital.cake.data.archetypes.trainer.HolonTransceiver.Name",
    display_name="Holon Transceiver",
    searchable_by=["Holon Transceiver","Item","HolonTransceiver"],
    subtypes=["Item"],
    collector_number=98,
    set_code="EX11",
    rarity=Rarities.Uncommon,
    effect=holon_transceiver_effect
)
