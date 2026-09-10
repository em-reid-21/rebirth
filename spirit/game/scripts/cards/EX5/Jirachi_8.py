from spirit.game.data_utils import PokemonCardDef, Attack, CARD_DEFS_BY_GUID
from spirit.game.attributes import AttrID, PokemonStage, PokemonTypes, Rarities, SpecialConditions
from spirit.game.card_effects.attacks_common import condition_attack
from spirit.game.models.board import BoardState
from spirit.game.session.effects import EffectContext, PokemonEntity, cast


def _can_evolve_further(pokemon: PokemonEntity) -> bool:
    logic_name = pokemon.get_attribute(AttrID.EVOLUTION_LOGIC_NAME)
    if not logic_name:
        return False

    return any(
        definition.extra_attributes.get(
            str(AttrID.EVOLUTION_LOGIC_FROM.value), {}
        ).get("value") == logic_name
        for definition in CARD_DEFS_BY_GUID.values()
    )
def make_a_wish_condition(board: BoardState, player_id: str, pokemon: PokemonEntity):
    return any(_can_evolve_further(p) for p in board.pokemon_in_play(player_id))

async def make_a_wish(ctx: EffectContext):
    """Search your deck for a card that evolves from 1 of your Pokémon and put it on that Pokémon. (This counts as evolving that Pokémon.) If you do, put 1 damage counter on Jirachi. Shuffle your deck afterward."""
    my_pokemon = ctx.my_pokemon_in_play()
    eligible_pokemon = [p for p in my_pokemon if _can_evolve_further(p)]
    if eligible_pokemon:
        target = await ctx.choose_pokemon(eligible_pokemon, prompt="Choose a Pokémon to evolve.")
        if target:
            evolution_basic_name = target.get_attribute(AttrID.EVOLUTION_LOGIC_NAME)

            def is_evolution_of_chosen_basic(card):
                return evolution_basic_name and card.get_attribute(AttrID.EVOLUTION_LOGIC_FROM) == evolution_basic_name

            evolution = await ctx.search_deck(
                is_evolution_of_chosen_basic, count=1, minimum=0,
                prompt="Choose a card to evolve with.",
            )

            if evolution:
                await ctx.evolve_pokemon(target, evolution[0])
                await ctx.deal_damage(10, cast(PokemonEntity, ctx.source), as_counters=True)
            await ctx.shuffle_deck()

card = PokemonCardDef(
    guid="313865b6-6236-54b4-a5d2-e592d3afa5b3",
    key="EX5",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Jirachi.Name",
    display_name="Jirachi",
    searchable_by=["Jirachi","Basic","Jirachi"],
    subtypes=["Basic"],
    collector_number=8,
    set_code="EX5",
    rarity=Rarities.RareHolo,
    hp=70,
    elements=[PokemonTypes.PSYCHIC, PokemonTypes.METAL],
    stage=PokemonStage.BASIC,
    retreat_cost=1,
    weakness_type=PokemonTypes.FIRE,
    abilities=[
        Attack(
            title="Make a Wish",
            game_text="Search your deck for a card that evolves from 1 of your Pokémon and put it on that Pokémon. (This counts as evolving that Pokémon.) If you do, put 1 damage counter on Jirachi. Shuffle your deck afterward.",
            cost={PokemonTypes.COLORLESS: 1},
            effect=make_a_wish,
            condition=make_a_wish_condition,
        ),
        Attack(
            title="Mind Bend",
            game_text="Flip a coin. If heads, the Defending Pokémon is now Confused.",
            cost={PokemonTypes.PSYCHIC: 1, PokemonTypes.METAL: 1},
            damage=30,
            effect=condition_attack(SpecialConditions.CONFUSED, flip=True),
        ),
    ],
)
