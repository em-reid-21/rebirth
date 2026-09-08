from spirit.game.data_utils import ItemCardDef, evolves_from
from spirit.game.attributes import AttrID, PokemonStage, Rarities
from spirit.game.models.board import BoardState
from spirit.game.session.effects import EffectContext, is_basic_pokemon, is_pokemon_card


def _stage1_or_stage2_matches(hand_cards, logic_name):
    return [
        card for card in hand_cards
        if is_pokemon_card(card)
        and (card.get_attribute(AttrID.STAGE) == PokemonStage.STAGE1.value or card.get_attribute(AttrID.STAGE) == PokemonStage.STAGE2.value)
        and evolves_from(card.archetype_id, logic_name)
    ]


def _rare_candy_condition(board: BoardState, player_id: str, card=None) -> bool:
    hand = board.find_player_area(player_id, "hand")
    hand_cards = hand.children if hand else []
    return any(
        _stage1_or_stage2_matches(hand_cards, basic.get_attribute(AttrID.EVOLUTION_LOGIC_NAME))
        for basic in board.pokemon_in_play(player_id)
        if is_basic_pokemon(basic)
        and basic.get_attribute(AttrID.EVOLUTION_LOGIC_NAME)
    )


async def _rare_candy(ctx: EffectContext):
    """Evolve a Basic Pokémon directly into a matching Stage 2 Pokémon."""
    hand = ctx.hand()
    candidates = [
        pokemon for pokemon in ctx.my_pokemon_in_play()
        if is_basic_pokemon(pokemon)
        and _stage1_or_stage2_matches(
            hand, pokemon.get_attribute(AttrID.EVOLUTION_LOGIC_NAME)
        )
    ]
    if not candidates:
        return

    target = await ctx.choose_pokemon(candidates, "Choose a Basic Pokémon in play")
    if target is None:
        return

    logic_name = target.get_attribute(AttrID.EVOLUTION_LOGIC_NAME)
    stage2_hand = _stage1_or_stage2_matches(hand, logic_name) if logic_name else []
    if not stage2_hand:
        return

    picks = await ctx.choose_cards(
        stage2_hand, 1, prompt="Choose a Stage 2 Pokémon to evolve into"
    )
    if picks:
        await ctx.evolve_pokemon(target, picks[0])

card = ItemCardDef(
    guid="dd3e4199-d5fd-535e-b54d-1323fd7c8790",
    key="EX2",
    name="com.direwolfdigital.cake.data.archetypes.trainer.RareCandy.Name",
    display_name="Rare Candy",
    searchable_by=["Rare Candy","Item","RareCandy"],
    subtypes=["Item"],
    collector_number=88,
    set_code="EX2",
    rarity=Rarities.Uncommon,
    effect=_rare_candy,
    condition=_rare_candy_condition
)
