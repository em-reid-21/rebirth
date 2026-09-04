from spirit.game.data_utils import SupporterCardDef
from spirit.game.attributes import Rarities
from spirit.game.session.effects import (
    EffectContext,
    is_basic_pokemon,
    is_stage1_pokemon,
    is_stage2_pokemon,
)


async def dawn(ctx: EffectContext):
    """Search your deck for a Basic Pokémon, a Stage 1 Pokémon, and a Stage 2
    Pokémon, reveal them, and put them into your hand. Then, shuffle your deck."""
    basic, stage1, stage2 = await ctx.search_deck_groups(
        [
            (is_basic_pokemon, 1, "Choose a Basic Pokémon to put into your hand."),
            (is_stage1_pokemon, 1, "Choose a Stage 1 Pokémon to put into your hand."),
            (is_stage2_pokemon, 1, "Choose a Stage 2 Pokémon to put into your hand."),
        ],
        prompt="Search your deck for a Basic Pokémon, a Stage 1 Pokémon, and a Stage 2 Pokémon.",
    )
    await ctx.put_in_hand(basic + stage1 + stage2, reveal=True)
    await ctx.shuffle_deck()


card = SupporterCardDef(
    guid="cdcb61ab-7c9b-5c5b-abcd-b28d55b971b5",
    key="ME2",
    name="com.direwolfdigital.cake.data.archetypes.trainer.Dawn.Name",
    display_name="Dawn",
    searchable_by=["Dawn", "Supporter", "Dawn"],
    subtypes=["Supporter"],
    collector_number=87,
    set_code="ME2",
    regulation_mark="I",
    rarity=Rarities.Uncommon,
    effect=dawn,
)
