from spirit.game.card_effects.support_common import more_prizes_remaining_than_opponent
from spirit.game.card_effects.trainers import is_energy_card
from spirit.game.data_utils import ItemCardDef
from spirit.game.attributes import Rarities
from spirit.game.models.board import BoardState, PokemonEntity
from spirit.game.session.effects import EffectContext

def defending_pokemon_has_energy(board: BoardState, opponent_id: str):
    """Check if the Defending Pokémon has any Energy attached."""
    defending_pokemon = board.active_pokemon(opponent_id)
    if defending_pokemon is None:
        return False
    return any(is_energy_card(c) for c in defending_pokemon.children)

def pow_hand_extension_condition(board: BoardState, player_id: str, pokemon: PokemonEntity):
    """You may use this card only if you have more Prize cards left than your opponent."""
    opponent_id = next(player for player in board.player_ids if player != player_id)
    defending_pokemon_has_energy_flag = defending_pokemon_has_energy(board, opponent_id)
    opponent_bench = board.find_player_area(opponent_id, "bench")
    opponent_has_benched_pokemon = bool(opponent_bench and opponent_bench.children)
    return more_prizes_remaining_than_opponent(board, player_id) and (defending_pokemon_has_energy_flag or opponent_has_benched_pokemon)

async def pow_hand_extension_effect(ctx: EffectContext):
    """You may use this card only if you have more Prize cards left than your opponent.
Move 1 Energy card attached to the Defending Pokémon to another of your opponent's Pokémon. Or, switch 1 of your opponent's Benched Pokémon with 1 of the Defending Pokémon. Your opponent chooses the Defending Pokémon to switch. """
    choices = ["Move 1 Energy card attached to the Defending Pokémon to another of your opponent's Pokémon", "Switch 1 of your opponent's Benched Pokémon with 1 of the Defending Pokémon"]
    choice = await ctx.choose(
        "Choose how to use Pow! Hand Extension",
        choices,
    )

    if choice == 0:
        defending = ctx.opponent_active()
        if defending is None:
            return
        energies = [energy for energy in ctx.attached_energies(defending)
                    if is_energy_card(energy)]
        destinations = [pokemon for pokemon in ctx.opponent_pokemon_in_play()
                         if pokemon is not defending]
        if not energies or not destinations:
            return
        picked_energy = await ctx.choose_cards(
            energies, 1, minimum=1,
            prompt="Choose an Energy card to move.",
            player_id=ctx.player_id,
        )
        if not picked_energy:
            return
        target = await ctx.choose_pokemon(
            destinations, "Choose an opponent's Pokémon to receive the Energy"
        )
        if target is not None:
            await ctx.move_energy(picked_energy[0], target)
    elif choice == 1:
        target = await ctx.choose_pokemon(
            ctx.opponent_bench(),
            "Choose the opponent's Benched Pokémon to switch with the Defending Pokémon",
            player_id=ctx.opponent_id,
        )
        if target is not None:
            await ctx.switch_active(ctx.opponent_id, target)


card = ItemCardDef(
    guid="7e5e9565-b7a2-5ea7-9eab-5f90610f75d8",
    key="EX7",
    name="com.direwolfdigital.cake.data.archetypes.trainer.PowHandExtension.Name",
    display_name="Pow! Hand Extension",
    searchable_by=["Pow! Hand Extension","Rocket's Secret Machine","PowHandExtension"],
    subtypes=["Rocket's Secret Machine"],
    collector_number=85,
    set_code="EX7",
    rarity=Rarities.Uncommon,
    effect=pow_hand_extension_effect,
    condition=pow_hand_extension_condition
)
