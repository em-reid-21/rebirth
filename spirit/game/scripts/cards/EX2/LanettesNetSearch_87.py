from spirit.game.data_utils import SupporterCardDef
from spirit.game.attributes import AttrID, PokemonTypes, Rarities
from spirit.game.session.effects import EffectContext, is_basic_pokemon, is_baby_pokemon

""" Search your deck for up to 3 different types of Basic Pokémon cards (excluding Baby Pokémon), show them to your opponent, and put them into your hand. Shuffle your deck afterward. """

def _eligible(card) -> bool:
    return (
        is_basic_pokemon(card) and not is_baby_pokemon(card)
        and bool(card.get_attribute(AttrID.POKEMON_TYPES))
    )

def _has_type(card, pokemon_type: PokemonTypes) -> bool:
    return pokemon_type.value in (card.get_attribute(AttrID.POKEMON_TYPES) or [])

async def lanettes_net_search_effect(ctx: EffectContext):
    # One group per type (count=1 each) so the browser itself enforces
    # "different types": e.g. Minun and Rayquaza ex are both [L], so picking
    # either fills that group's slot and the other stops being selectable.
    groups = [
        (lambda card, t=t: _eligible(card) and _has_type(card, t), 1, "")
        for t in PokemonTypes
    ]
    picked_by_group = await ctx.search_deck_groups(
        groups,
        prompt="Choose up to 3 Basic Pokémon of different types.",
        total=3,
        any_of=True,
    )
    picks = [card for group in picked_by_group for card in group]

    if picks:
        await ctx.put_in_hand(picks, reveal=True)
    await ctx.shuffle_deck()


card = SupporterCardDef(
    guid="bcb48bd8-729f-576e-bd58-e1f97cb26749",
    key="EX2",
    name="com.direwolfdigital.cake.data.archetypes.trainer.LanettesNetSearch.Name",
    display_name="Lanette's Net Search",
    searchable_by=["Lanette's Net Search","Supporter","LanettesNetSearch"],
    subtypes=["Supporter"],
    collector_number=87,
    set_code="EX2",
    rarity=Rarities.Uncommon,
    effect=lanettes_net_search_effect
)
