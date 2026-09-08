from spirit.game.card_effects.support_common import more_prizes_remaining_than_opponent
from spirit.game.data_utils import PokemonCardDef, Attack, Ability, unimplemented
from spirit.game.attributes import AbilityTypes, AttrID, PokemonStage, PokemonTypes, Rarities
from spirit.game.models import board
from spirit.game.session.effects import EffectContext
from spirit.game.session.passives import Passive

# SV06/BloodmoonUrsalunaex_141.py 
class _RageAuraPassive(Passive):
    """Ignore all Colorless Energy necessary to use Rayquaza ex's Special Circuit and Sky-high Claws attacks if you have more Prize cards left than your opponent."""

    def modify_attack_cost(self, cost, pokemon, carrier, board):
        if carrier is not pokemon:
            return cost
        owner = carrier.owning_player_id
        if owner is None:
            return cost
        if not more_prizes_remaining_than_opponent(board, owner):
            return cost
        if "Colorless" not in cost:
            return cost
        del cost["Colorless"]
        return cost

# From ZeraoraVMax_54.py
def _has_ability(pokemon) -> bool:
    abilities = pokemon.get_attribute(AttrID.PIE_ABILITIES) or []
    return any(isinstance(e, dict) and e.get("abilityType") in ("PokePower", "PokeBody")
               for e in abilities)

async def special_circuit_condition(ctx: EffectContext):
    """Choose 1 of your opponent's Pokémon. This attack does 30 damage to the Pokémon. If you choose a Pokémon that has any Poké-Powers or Poké-Bodies, this attack does 50 damage instead. (Don't apply Weakness and Resistance for Benched Pokémon.)"""
    candidates = ctx.opponent_pokemon_in_play()
    if not candidates:
        return
    target = await ctx.choose_pokemon(
        candidates, "Choose 1 of your opponent's Pokémon to deal damage to"
    )
    if target is None:
        return
    damage = 50 if _has_ability(target) else 30
    await ctx.deal_damage(damage, target)

card = PokemonCardDef(
    guid="459957cb-e9aa-5025-8c91-630d9b51819d",
    key="EX15",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Rayquazaex.Name",
    display_name="Rayquaza ex δ",
    searchable_by=["Rayquaza ex δ","Basic","ex","Rayquazaex"],
    subtypes=["Basic","ex", "Delta Species"],
    collector_number=97,
    set_code="EX15",
    rarity=Rarities.RareHoloEX,
    hp=110,
    elements=[PokemonTypes.LIGHTNING],
    stage=PokemonStage.BASIC,
    retreat_cost=2,
    abilities=[
        Ability(
            title="Rage Aura",
            ability_type=AbilityTypes.POKE_BODY,
            game_text="If you have more Prize cards left than your opponent, ignore all Colorless Energy necessary to use Rayquaza ex's Special Circuit and Sky-high Claws attacks.",
            passive=_RageAuraPassive(),
        ),
        Attack(
            title="Special Circuit",
            game_text="Choose 1 of your opponent's Pokémon. This attack does 30 damage to the Pokémon. If you choose a Pokémon that has any Poké-Powers or Poké-Bodies, this attack does 50 damage instead. (Don't apply Weakness and Resistance for Benched Pokémon.)",
            cost={PokemonTypes.LIGHTNING: 1, PokemonTypes.COLORLESS: 1},
            effect=special_circuit_condition,
        ),
        Attack(
            title="Sky-high Claws",
            cost={PokemonTypes.LIGHTNING: 2, PokemonTypes.COLORLESS: 2},
            damage=70,
        ),
    ],
)
