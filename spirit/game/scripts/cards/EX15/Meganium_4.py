from spirit.game.card_effects.trainers import is_basic_energy_card
from spirit.game.data_utils import PokemonCardDef, Attack, Ability, Activations, Triggers, unimplemented
from spirit.game.attributes import PokemonStage, PokemonTypes, Rarities
from spirit.game.session.effects import AbilityTypes, EffectContext, has_rule_box, is_pokemon_card
from spirit.game.session.passives import TurnDamageModifier

async def evolutionary_call_effect(ctx: EffectContext):
    """Once during your turn, when you play Meganium from your hand to evolve 1 of your Pokémon, you may search your deck for up to 3 in any combination of Basic Pokémon or Evolution cards. Show them to your opponent and put them into your hand. Shuffle your deck afterward."""
    if await ctx.ask_yes_no("Search your deck for up to 3 Basic Pokémon or Evolution cards?"):
        pokemon_candidates = [
            c for c in ctx.deck()
            if is_pokemon_card(c)
        ]

        if not pokemon_candidates:
            return

        picks = await ctx.choose_cards(
            pokemon_candidates,
            3,
            minimum=0,
            prompt=(
                "Choose up to 3 Basic Pokémon or Evolution cards to put into your hand."
            ),
        )
        if picks:
            await ctx.put_in_hand(picks, reveal=True)
        await ctx.shuffle_deck()


async def delta_reduction_effect(ctx: EffectContext):
    """During your opponent's next turn, any damage done by attacks from the Defending Pokémon is reduced by 30 (before applying Weakness and Resistance)."""
    defender = ctx.defender
    if defender is None:
        return
    ctx.add_turn_damage_modifier(TurnDamageModifier(
        -30, ctx.opponent_id,
        source_entity_id=defender.entity_id,
        opposing_active_only=False,
        expires_after_turn=ctx.session.turn_state.turn_number + 1,
    ))

card = PokemonCardDef(
    guid="3fcc4658-9699-5852-9f76-2a81996bad6c",
    key="EX15",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Meganium.Name",
    display_name="Meganium δ",
    searchable_by=["Meganium δ","Stage 2","Meganium"],
    subtypes=["Stage 2", "Delta Species"],
    collector_number=4,
    set_code="EX15",
    rarity=Rarities.RareHolo,
    hp=110,
    elements=[PokemonTypes.FIGHTING],
    stage=PokemonStage.STAGE2,
    retreat_cost=2,
    weakness_type=PokemonTypes.FIRE,
    resistance_type=PokemonTypes.WATER,
    evolves_from="com.direwolfdigital.cake.data.archetypes.pokemon.Bayleef.Name",
    abilities=[
        Ability(
            title="Evolutionary Call",
            ability_type=AbilityTypes.POKE_POWER,
            game_text="Once during your turn, when you play Meganium from your hand to evolve 1 of your Pokémon, you may search your deck for up to 3 in any combination of Basic Pokémon or Evolution cards. Show them to your opponent and put them into your hand. Shuffle your deck afterward.",
            trigger=Triggers.ON_EVOLVE,
            effect=evolutionary_call_effect,
        ),
        Attack(
            title="Delta Reduction",
            game_text="During your opponent's next turn, any damage done by attacks from the Defending Pokémon is reduced by 30 (before applying Weakness and Resistance).",
            cost={PokemonTypes.FIGHTING: 1, PokemonTypes.COLORLESS: 1},
            damage=40,
            effect=delta_reduction_effect,
        ),
        Attack(
            title="Mega Impact",
            cost={PokemonTypes.FIGHTING: 1, PokemonTypes.COLORLESS: 2},
            damage=60,
        ),
    ],
)
