from spirit.game.data_utils import PokemonCardDef, Attack, Ability, subtypes_for
from spirit.game.attributes import AbilityTypes, PokemonStage, PokemonTypes, Rarities
from spirit.game.session.effects import EffectContext
from spirit.game.session.passives import Passive


class _StarLightPassive(Passive):
    """Reduce Jirachi ex's Colorless attack cost while the condition holds."""

    def modify_attack_cost(self, cost, pokemon, carrier, board):
        if carrier is not pokemon or "Colorless" not in cost:
            return cost
        opponent = next(
            (player_id for player_id in board.player_ids
             if player_id != carrier.owning_player_id),
            None,
        )
        if opponent is None:
            return cost
        opponent_pokemon = board.pokemon_in_play(opponent)
        if not any(
            subtype in {"ex", "Stage 2"}
            for pokemon in opponent_pokemon
            for subtype in subtypes_for(pokemon.archetype_id)
        ):
            return cost
        remaining = cost["Colorless"] - 1
        if remaining > 0:
            cost["Colorless"] = remaining
        else:
            del cost["Colorless"]
        return cost


class _ShieldBeamPassive(Passive):
    """Prevent the opponent's Pokemon from using Poké-Powers this turn."""

    def blocks_abilities(self, pokemon, carrier):
        return pokemon.owning_player_id != carrier.owning_player_id

async def shield_beam_effect(ctx: EffectContext):
    await ctx.deal_damage()
    """During your opponent's next turn, your opponent can't use any Poké-Powers on his or her Pokémon."""
    ctx.add_passive_through_opponents_turn(ctx.source, _ShieldBeamPassive())

card = PokemonCardDef(
    guid="d8b0ecbb-1f2d-536e-8f5b-9f889c4adfc0",
    key="EX14",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Jirachiex.Name",
    display_name="Jirachi ex",
    searchable_by=["Jirachi ex","Basic","ex","Jirachiex"],
    subtypes=["Basic","ex"],
    collector_number=94,
    set_code="EX14",
    rarity=Rarities.RareHoloEX,
    hp=90,
    elements=[PokemonTypes.PSYCHIC],
    stage=PokemonStage.BASIC,
    retreat_cost=1,
    abilities=[
        Ability(
            title="Star Light",
            ability_type=AbilityTypes.POKE_BODY,
            game_text="As long as your opponent has any Pokémon-ex or Stage 2 Evolved Pokémon in play, Jirachi ex pays Colorless less Energy to use Shield Beam or Super Psy Bolt.",
            passive=_StarLightPassive(),
        ),
        Attack(
            title="Shield Beam",
            game_text="During your opponent's next turn, your opponent can't use any Poké-Powers on his or her Pokémon.",
            cost={PokemonTypes.PSYCHIC: 1, PokemonTypes.COLORLESS: 1},
            damage=30,
            effect=shield_beam_effect,
        ),
        Attack(
            title="Super Psy Bolt",
            cost={PokemonTypes.PSYCHIC: 1, PokemonTypes.COLORLESS: 2},
            damage=50,
        ),
    ],
)
