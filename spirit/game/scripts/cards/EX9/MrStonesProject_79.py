from spirit.game.card_effects.trainers import is_basic_energy_card
from spirit.game.data_utils import SupporterCardDef
from spirit.game.attributes import Rarities
from spirit.game.models.board import BoardState
from spirit.game.session.effects import EffectContext

""" Search your deck for up to 2 Basic cards, show them to your opponent, and put them into your hand. Shuffle your deck afterward. Or, search your discard pile for up to 2 Basic cards, show them to your opponent, and put them into your hand. """    

def energy_in_discard(discard):
    return [card for card in discard if is_basic_energy_card(card)]

async def search(ctx: EffectContext, deck_or_discard: str):
    if deck_or_discard == "deck":
        cards = [card for card in ctx.deck() if is_basic_energy_card(card)]
        display_cards = ctx.deck()
    elif deck_or_discard == "discard":
        cards = energy_in_discard(ctx.discard_pile())
        display_cards = ctx.discard_pile()
    else:
        return
    picks = await ctx.choose_cards(
                cards,
                2,
                minimum=0,
                prompt="Choose up to 2 Basic cards to put into your hand",
                display_cards=display_cards
            )
    if picks:
        await ctx.reveal_cards(picks)
        await ctx.put_in_hand(picks, reveal=True)
    return

async def mr_stones_project_effect(ctx: EffectContext):
    candidates = energy_in_discard(ctx.discard_pile())
    if not candidates:
        await search(ctx, "deck")
        return

    choices = ["Search your deck for up to 2 Basic cards"]
    if candidates:
        choices.append("Search your discard pile for up to 2 Basic cards")
    choice = await ctx.choose(
        "Choose how to use Mr. Stone's Project",
        choices,
    )

    if choice == 0:
        await search(ctx, "deck")
        return

    if choice == 1:
        await search(ctx, "discard")
        return

card = SupporterCardDef(
    guid="3ae7468f-1fa1-5ff7-8522-b7e5ba2477b8",
    key="EX9",
    name="com.direwolfdigital.cake.data.archetypes.trainer.MrStonesProject.Name",
    display_name="Mr. Stone's Project",
    searchable_by=["Mr. Stone's Project","Supporter","MrStonesProject"],
    subtypes=["Supporter"],
    collector_number=79,
    set_code="EX9",
    rarity=Rarities.Uncommon,
    effect=mr_stones_project_effect
)
