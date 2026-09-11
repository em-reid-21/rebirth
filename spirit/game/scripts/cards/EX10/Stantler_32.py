from spirit.game.data_utils import PokemonCardDef, Attack
from spirit.game.attributes import PokemonStage, PokemonTypes, Rarities, SpecialConditions
from spirit.game.models.board import PokemonEntity
from spirit.game.session.effects import EffectContext, cast, is_evolution_pokemon, is_trainer_card

async def screechy_voice_effect(ctx: EffectContext):
    await ctx.deal_damage()
    if is_evolution_pokemon(cast(PokemonEntity, ctx.defender)):
        await ctx.apply_special_condition(ctx.defender, SpecialConditions.CONFUSED)

async def push_away_effect(ctx: EffectContext):
    await ctx.deal_damage()
    hand = ctx.hand(player_id=ctx.opponent_id)
    if not hand:
        return
    eligible_cards = [card for card in hand if is_trainer_card(card)]
    picks = await ctx.choose_cards(
        eligible_cards, 1, minimum=1,
        prompt="Choose a card to discard from your opponent's hand.",
        display_cards=hand,
    )
    await ctx.discard_cards(picks)


card = PokemonCardDef(
    guid="352efb0f-fcad-57a9-bb1a-36a5cf57f6cb",
    key="EX10",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Stantler.Name",
    display_name="Stantler",
    searchable_by=["Stantler","Basic","Stantler"],
    subtypes=["Basic"],
    collector_number=32,
    set_code="EX10",
    rarity=Rarities.Rare,
    hp=70,
    elements=[PokemonTypes.COLORLESS],
    stage=PokemonStage.BASIC,
    retreat_cost=1,
    weakness_type=PokemonTypes.FIGHTING,
    abilities=[
        Attack(
            title="Screechy Voice",
            game_text="If the Defending Pokémon is an Evolved Pokémon, the Defending Pokémon is now Confused.",
            cost={PokemonTypes.COLORLESS: 1},
            damage=10,
            effect=screechy_voice_effect,
        ),
        Attack(
            title="Push Away",
            game_text="Look at your opponent's hand, choose a Trainer card you find there, and discard it.",
            cost={PokemonTypes.COLORLESS: 2},
            damage=20,
            effect=push_away_effect,
        ),
    ],
)
