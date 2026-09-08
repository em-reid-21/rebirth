from spirit.game.data_utils import PokemonCardDef, Attack
from spirit.game.attributes import PokemonStage, PokemonTypes, Rarities, SpecialConditions
from spirit.game.card_effects.attacks_common import condition_attack

card = PokemonCardDef(
    guid="e2653f01-4535-5a0a-ae1c-f02e6bc3fbe2",
    key="EX15",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Chikorita.Name",
    display_name="Chikorita δ",
    searchable_by=["Chikorita δ","Basic","Chikorita"],
    subtypes=["Basic", "Delta Species"],
    collector_number=44,
    set_code="EX15",
    rarity=Rarities.Common,
    hp=40,
    elements=[PokemonTypes.FIGHTING],
    stage=PokemonStage.BASIC,
    retreat_cost=1,
    weakness_type=PokemonTypes.FIRE,
    resistance_type=PokemonTypes.WATER,
    abilities=[
        Attack(
            title="Sleep Powder",
            game_text="The Defending Pokémon is now Asleep.",
            cost={PokemonTypes.COLORLESS: 1},
            effect=condition_attack(SpecialConditions.ASLEEP),
        ),
        Attack(
            title="Tackle",
            cost={PokemonTypes.COLORLESS: 2},
            damage=20,
        ),
    ],
)
