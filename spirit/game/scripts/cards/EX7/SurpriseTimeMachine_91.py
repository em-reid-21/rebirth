from spirit.game.card_effects.pokemon import devolvable
from spirit.game.data_utils import ItemCardDef
from spirit.game.attributes import AttrID, Rarities
from spirit.game.models.board import BoardState, PokemonEntity
from spirit.game.session.effects import EffectContext

""" Choose 1 of your Evolved Pokémon, remove the highest Stage Evolution card from it, and shuffle it into your deck (this counts as devolving that Pokémon). If that Pokémon remains in play, search your deck for an Evolution card that evolves from that Pokémon and put it onto that Pokémon (this counts as evolving that Pokémon). Shuffle your deck afterward. """

def surprise_time_machine_candidates(board: BoardState, player_id: str):
    """You can only use this card if you have an Evolved Pokémon in play either active or benched."""
    return [
        p for p in board.pokemon_in_play(player_id)
        if devolvable(p)
    ]

def surprise_time_machine_condition(board: BoardState, player_id: str, pokemon: PokemonEntity):
    return surprise_time_machine_candidates(board, player_id)

async def surprise_time_machine_effect(ctx: EffectContext):
    candidates = surprise_time_machine_candidates(ctx.board, ctx.player_id)
    if candidates:
        target = await ctx.choose_pokemon(candidates, "Choose an evolved Pokémon to devolve")
        if target:
            # The promoted previous stage isn't returned, so diff pokemon_in_play to find it.
            before_ids = {p.entity_id for p in ctx.board.pokemon_in_play(ctx.player_id)}
            removed = await ctx.devolve_pokemon(target, steps=1, destination="deck")
            if removed:
                await ctx.shuffle_deck(ctx.player_id)
                remaining = next(
                    (p for p in ctx.board.pokemon_in_play(ctx.player_id)
                     if p.entity_id not in before_ids),
                    None,
                )
                if remaining is not None and remaining not in ctx.knockouts:
                    evolves_from = remaining.get_attribute(AttrID.EVOLUTION_LOGIC_NAME)
                    deck_cards = ctx.deck()
                    pokemon_candidates = [
                        card for card in deck_cards
                        if card.get_attribute(AttrID.EVOLUTION_LOGIC_FROM) == evolves_from
                    ]

                    picks = await ctx.choose_cards(
                        pokemon_candidates,
                        1,
                        minimum=0,
                        prompt=(
                            "Choose an Evolution card to put onto the devolved Pokémon."
                        ),
                        display_cards=deck_cards,
                    )
                    if picks:
                        await ctx.evolve_pokemon(remaining, picks[0])
                    await ctx.shuffle_deck(ctx.player_id)

card = ItemCardDef(
    guid="a37144f2-53be-5d82-989d-42d73e4a4d2b",
    key="EX7",
    name="com.direwolfdigital.cake.data.archetypes.trainer.SurpriseTimeMachine.Name",
    display_name="Surprise! Time Machine",
    searchable_by=["Surprise! Time Machine","Rocket's Secret Machine","SurpriseTimeMachine"],
    subtypes=["Rocket's Secret Machine"],
    collector_number=91,
    set_code="EX7",
    rarity=Rarities.Uncommon,
    effect=surprise_time_machine_effect,
    condition=surprise_time_machine_condition,
)
