from spirit.game.data_utils import ItemCardDef
from spirit.game.attributes import AttrID, Rarities, TrainerType
from spirit.game.session.effects import EffectContext
from spirit.game.session.game_session import BoardState

"""Choose up to 2 in any combination of Pokémon Tool cards and Stadium cards in play (both yours and your opponent's) and discard them."""

def windstorm_condition(board: BoardState, player_id: str, card=None) -> bool:
    """Check if there are any Pokémon Tool cards or Stadium cards in play to discard."""
    return bool(_windstorm_targets(board))


def _windstorm_targets(board: BoardState) -> list:
    targets = [
        tool
        for pid in board.player_ids
        for pokemon in board.pokemon_in_play(pid)
        for tool in pokemon.children
        if tool.get_attribute(AttrID.TRAINER_TYPE) in (
            TrainerType.POKEMON_TOOL.value,
            TrainerType.POKEMON_TOOL_F.value,
        )
    ]
    stadium_area = board.find_global_area("activeStadium")
    if stadium_area:
        targets.extend(stadium_area.children)
    return targets


async def windstorm_effect(ctx: EffectContext):
    """Discard up to 2 Pokémon Tools and/or Stadiums in play."""
    targets = _windstorm_targets(ctx.board)
    if not targets:
        return

    picks = await ctx.choose_cards(
        targets,
        2,
        minimum=1,
        prompt="Choose up to 2 Pokémon Tools or Stadiums to discard",
    )
    await ctx.discard_cards(picks)

card = ItemCardDef(
    guid="db3d3b1c-9b4b-5089-989b-7f0711b2423d",
    key="EX14",
    name="com.direwolfdigital.cake.data.archetypes.trainer.Windstorm.Name",
    display_name="Windstorm",
    searchable_by=["Windstorm","Item","Windstorm"],
    subtypes=["Item"],
    collector_number=85,
    set_code="EX14",
    rarity=Rarities.Uncommon,
    effect=windstorm_effect,
    condition=windstorm_condition
)
