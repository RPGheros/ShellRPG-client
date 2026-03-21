
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

DamageType = Literal[
    "physical", "melee", "distance", "fire", "water", "ice", "lightning", "storm",
    "earth", "stone", "metal", "holy", "unholy", "soul", "poison", "illusion", "shadow",
]

WORLD = {"width": 4096, "height": 4096, "chunk_size": 32, "start_x": 2048, "start_y": 2048}

MONEY_GOLD_FACTOR = 100
QUALITY_ORDER = ["kaputt", "gebraucht", "normal", "gehärtet", "veredelt", "geschärft", "modifiziert", "magisch", "episch", "legendär", "heilig", "unheilig"]

BIOMES = [
    "Kornmark-Auen", "Schwarzwurzelwald", "Nebelmoor", "Aschensteppe", "Grenzland", "Eisenhügel",
    "Jade-Dschungel", "Kristalldünen", "Salzebenen", "Donnermesa", "Leviathanküste", "Hohlfrost-Tundra",
    "Sonnenmoor", "Obsidianweite", "Mondsumpf", "Basaltkessel",
    "Flusshain", "Grasmeer", "Rabensteppe", "Silberküste", "Lavakessel", "Düsterforst",
    "Himmelsbruch", "Bernsteinfeld", "Dornenwildnis", "Sturmschlucht",
]
BIOME_WEIGHTS = [
    ("Kornmark-Auen", 12), ("Schwarzwurzelwald", 10), ("Nebelmoor", 8), ("Aschensteppe", 8), ("Grenzland", 8),
    ("Eisenhügel", 7), ("Jade-Dschungel", 6), ("Kristalldünen", 5), ("Salzebenen", 5), ("Donnermesa", 4),
    ("Leviathanküste", 4), ("Hohlfrost-Tundra", 4), ("Sonnenmoor", 4), ("Obsidianweite", 4), ("Mondsumpf", 4), ("Basaltkessel", 3),
    ("Flusshain", 5), ("Grasmeer", 5), ("Rabensteppe", 4), ("Silberküste", 3), ("Lavakessel", 3), ("Düsterforst", 4),
    ("Himmelsbruch", 2), ("Bernsteinfeld", 3), ("Dornenwildnis", 3), ("Sturmschlucht", 3),
]

BIOME_TERRAIN = {
    "Kornmark-Auen": "Feldweg", "Schwarzwurzelwald": "Waldpfad", "Nebelmoor": "Moorpfad", "Aschensteppe": "Brandland",
    "Grenzland": "Grenzpfad", "Eisenhügel": "Hügelpfad", "Jade-Dschungel": "Rankenpfad", "Kristalldünen": "Düne",
    "Salzebenen": "Salzkruste", "Donnermesa": "Hochfläche", "Leviathanküste": "Küstenweg", "Hohlfrost-Tundra": "Frostpfad",
    "Sonnenmoor": "Lichtmoor", "Obsidianweite": "Glasboden", "Mondsumpf": "Mondmoor", "Basaltkessel": "Basaltpfad",
    "Flusshain": "Auenpfad", "Grasmeer": "Wiesenweg", "Rabensteppe": "Steppe", "Silberküste": "Brandungsweg",
    "Lavakessel": "Schlackepfad", "Düsterforst": "Dunkelwaldpfad", "Himmelsbruch": "Kliffkante",
    "Bernsteinfeld": "Bernsteinacker", "Dornenwildnis": "Dornpfad", "Sturmschlucht": "Schluchtpfad",
}

RESOURCE_BY_BIOME = {
    "Kornmark-Auen": ("gold",), "Schwarzwurzelwald": ("wood",), "Nebelmoor": ("gems",), "Aschensteppe": ("iron", "gold"),
    "Grenzland": ("wood", "iron"), "Eisenhügel": ("iron",), "Jade-Dschungel": ("wood", "gems"), "Kristalldünen": ("gems",),
    "Salzebenen": ("gold",), "Donnermesa": ("iron",), "Leviathanküste": ("gems",), "Hohlfrost-Tundra": ("gems",),
    "Sonnenmoor": ("wood", "gems"), "Obsidianweite": ("iron", "gems"), "Mondsumpf": ("gems",), "Basaltkessel": ("iron", "gold"),
    "Flusshain": ("wood", "gold"), "Grasmeer": ("wood",), "Rabensteppe": ("iron",), "Silberküste": ("gems", "gold"),
    "Lavakessel": ("iron", "gems"), "Düsterforst": ("wood",), "Himmelsbruch": ("gems",), "Bernsteinfeld": ("gems",),
    "Dornenwildnis": ("wood", "gems"), "Sturmschlucht": ("iron",),
}

GEM_COMBINATIONS_BASE = {
    "smaragd": "poison",
    "ruby": "fire",
    "sapphire": "lightning",
    "diamond": "ice",
    "calcedon": "soul",
    "onyx": "unholy",
    "bergkristall": "holy",
    "zirkon": "earth",
    "bernstein": "storm",
    "opal": "illusion",
    "obsidian": "shadow",
}

DIRECTION_ALIASES = {"n": "N", "north": "N", "s": "S", "south": "S", "w": "W", "west": "W", "o": "O", "e": "O", "east": "O"}
DIR_VECTORS = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "O": (1, 0)}

RACE_SOUL_DAMAGE = {
    "Mensch": "soul", "Bestie": "physical", "Untoter": "unholy", "Dämon": "fire", "Elementar": "storm",
    "Vampyr": "unholy", "Leviathanbrut": "water", "Titanensplitter": "stone", "Geist": "holy",
}

SPECIAL_DAMAGE_HINTS = {
    "Kleriker": {"Dämon": 1.25, "Untoter": 1.35, "Vampyr": 1.2},
    "Vampyrjäger": {"Vampyr": 1.4},
    "Ritter": {"Bestie": 1.1},
}

WEAPON_CLASSES = [
    "schwert", "axt", "zweihand-axt", "nunchaku", "kampfstab", "zauberstab", "morgenstern",
    "handschild", "wurfstern", "steinschleuder", "wurfmesser", "wurf-axt", "zweihand-schwert",
    "hellebarde", "katana", "saebel", "dolch", "kurzschwert", "bogen"
]

SKILL_ICONS = ["attack", "guard", "dodge", "auto-battle", "soul-trap", "fireball", "lightning-orb", "city-build", "militia", "trade"]

STARTING_COMMANDS = [
    "look", "inspect", "map", "inventory", "equipment", "buffs", "quests", "market", "journal",
    "walk north|south|west|east|x,y", "walk route <ziel>", "hunt north|south|west|east|x,y",
    "gather iron|wood|gems|gold|x,y", "explore", "equip <item>", "use <item>", "lang de|en",
    "attack", "guard", "dodge", "cast soul trap", "cast fireball", "cast lightning orb",
    "cast lightning strike", "cast fire wall", "cast fire beam", "auto battle on|off|balanced|aggressive|defensive",
    "craft --item sword --material iron", "socket --slot weapon --gem ruby shard", "enchant --slot weapon",
    "soul forge --slot weapon --stone soulstone lesser", "merchant list", "buy <item>", "sell <item>",
    "city found <name>", "city status", "city appoint governor <name>", "city appoint general <1-5> <name>",
    "city build <building>", "militia recruit <unit> [amount]", "militia status", "cube enter", "cube leave", "cube say <frage>", "show commands"
]

@dataclass(frozen=True)
class ItemDef:
    item_id: str
    name: dict[str, str]
    category: str
    quality: str
    slot: str | None = None
    price_silver: int = 0
    damage: int = 0
    armor: int = 0
    damage_type: DamageType | None = None
    ammo_type: str | None = None
    weapon_class: str | None = None
    charges: int = 0
    pages: tuple[dict[str, str], ...] = ()
    permanent_bonus: dict[str, int] = field(default_factory=dict)
    buffs: tuple[dict[str, object], ...] = ()
    affixes: tuple[str, ...] = ()
    description: dict[str, str] = field(default_factory=dict)
    socket_slots: int = 0
    icon: str = ""

@dataclass(frozen=True)
class MonsterClass:
    enemy_id: str
    name: dict[str, str]
    race: str
    faction: str
    level: int
    max_hp: int
    attack_kind: str
    damage_type: DamageType
    power: int
    armor: int
    wisdom: int
    intelligence: int
    dexterity: int
    accuracy: int
    defense: int
    block: int
    dodge: int
    loot_table: tuple[tuple[str, int, int], ...]
    group_min: int = 1
    group_max: int = 1
    media_file: str = ""
    biome_tags: tuple[str, ...] = ()
    resistances: dict[str, int] = field(default_factory=dict)

@dataclass(frozen=True)
class TravelEncounter:
    encounter_id: str
    name: dict[str, str]
    description: dict[str, str]
    biomes: tuple[str, ...]
    media_file: str

@dataclass(frozen=True)
class BuildingDef:
    building_id: str
    name: dict[str, str]
    kind: str
    build_cost: dict[str, int]
    research_cost: dict[str, int]
    outputs: dict[str, int]
    upkeep: dict[str, int]
    faction_conflicts: tuple[str, ...] = ()
    description: dict[str, str] = field(default_factory=dict)
    sprite: str = ""

@dataclass(frozen=True)
class UnitDef:
    unit_id: str
    name: dict[str, str]
    role: str
    upkeep_silver: int
    offense: int
    defense: int
    ranged: bool = False
    commander_bonus: dict[str, int] = field(default_factory=dict)
    sprite: str = ""

SPECIAL_TILES = {
    (2048, 2048): {"de": "Graufurt-Osttor", "en": "Graufurt East Gate", "biome": "Kornmark-Auen", "terrain": "Stadttor", "city": "Graufurt", "poi": ("graufurt_market",), "resources": (), "media_base": "tile_graufurt-eastgate"},
    (2051, 2048): {"de": "Aschenwall-Vorwerk", "en": "Ashenwall Outwork", "biome": "Aschensteppe", "terrain": "Grenzfestung", "city": "Aschenwall", "resources": ("gold",), "poi": (), "media_base": "tile_ashenwall-outwork"},
    (2052, 2049): {"de": "Valmora-Hain", "en": "Valmora Grove", "biome": "Schwarzwurzelwald", "terrain": "Hainstadt", "city": "Valmora-Hain", "resources": ("wood",), "poi": (), "media_base": "tile_valmora-grove"},
    (2056, 2052): {"de": "Schwarzer Kubus", "en": "Black Cube", "biome": "Obsidianweite", "terrain": "Schwebendes Artefakt", "city": None, "resources": (), "poi": ("black_cube",), "media_base": "tile_black-cube"},
}
ROUTES = {"graufurt": (2048, 2048), "valmora": (2052, 2049), "ashenwall": (2051, 2048), "cube": (2056, 2052), "frontier": (2070, 2060)}

def pages(*parts_de_en):
    return tuple({"de": de, "en": en} for de, en in parts_de_en)

ITEMS = {
    "iron_sword": ItemDef("iron_sword", {"de":"Eisenschwert","en":"Iron Sword"}, "weapon", "normal", slot="weapon", price_silver=34, damage=13, damage_type="melee", weapon_class="schwert", socket_slots=1, description={"de":"Schlicht, zuverlässig, schwer genug.", "en":"Plain, reliable, heavy enough."}, icon="item_iron-sword"),
    "steel_sword": ItemDef("steel_sword", {"de":"Stahlschwert","en":"Steel Sword"}, "weapon", "gehärtet", slot="weapon", price_silver=60, damage=18, damage_type="melee", weapon_class="schwert", socket_slots=2, icon="item_steel-sword"),
    "oak_bow": ItemDef("oak_bow", {"de":"Eichenbogen","en":"Oak Bow"}, "weapon", "normal", slot="weapon", price_silver=28, damage=10, damage_type="distance", weapon_class="bogen", ammo_type="arrows", socket_slots=1, icon="item_oak-bow"),
    "short_sword": ItemDef("short_sword", {"de":"Kurzschwert","en":"Short Sword"}, "weapon", "normal", slot="weapon", price_silver=22, damage=11, damage_type="melee", weapon_class="kurzschwert", socket_slots=1, icon="item_short-sword"),
    "battle_axe": ItemDef("battle_axe", {"de":"Kampfaxt","en":"Battle Axe"}, "weapon", "normal", slot="weapon", price_silver=38, damage=16, damage_type="melee", weapon_class="axt", socket_slots=1, icon="item_battle-axe"),
    "great_axe": ItemDef("great_axe", {"de":"Zweihandaxt","en":"Two-Handed Axe"}, "weapon", "gehärtet", slot="weapon", price_silver=55, damage=22, damage_type="melee", weapon_class="zweihand-axt", socket_slots=2, icon="item_great-axe"),
    "nunchaku": ItemDef("nunchaku", {"de":"Nunchaku","en":"Nunchaku"}, "weapon", "normal", slot="weapon", price_silver=29, damage=12, damage_type="melee", weapon_class="nunchaku", socket_slots=1, icon="item_nunchaku"),
    "war_staff": ItemDef("war_staff", {"de":"Kampfstab","en":"War Staff"}, "weapon", "normal", slot="weapon", price_silver=27, damage=12, damage_type="melee", weapon_class="kampfstab", socket_slots=1, icon="item_war-staff"),
    "spell_wand": ItemDef("spell_wand", {"de":"Zauberstab","en":"Spell Wand"}, "weapon", "veredelt", slot="weapon", price_silver=41, damage=9, damage_type="soul", weapon_class="zauberstab", socket_slots=1, icon="item_spell-wand"),
    "morningstar": ItemDef("morningstar", {"de":"Morgenstern","en":"Morningstar"}, "weapon", "normal", slot="weapon", price_silver=40, damage=15, damage_type="melee", weapon_class="morgenstern", socket_slots=1, icon="item_morningstar"),
    "buckler": ItemDef("buckler", {"de":"Defensivschild","en":"Defensive Shield"}, "armor", "normal", slot="offhand", price_silver=18, armor=7, icon="item_buckler"),
    "throwing_star": ItemDef("throwing_star", {"de":"Wurfstern","en":"Throwing Star"}, "ammo", "normal", slot="ammo", price_silver=12, damage=7, damage_type="distance", weapon_class="wurfstern", icon="item_throwing-star"),
    "sling": ItemDef("sling", {"de":"Steinschleuder","en":"Sling"}, "weapon", "normal", slot="weapon", price_silver=16, damage=8, damage_type="distance", weapon_class="steinschleuder", socket_slots=1, icon="item_sling"),
    "throwing_knife": ItemDef("throwing_knife", {"de":"Wurfmesser","en":"Throwing Knife"}, "ammo", "normal", slot="ammo", price_silver=14, damage=8, damage_type="distance", weapon_class="wurfmesser", icon="item_throwing-knife"),
    "throwing_axe": ItemDef("throwing_axe", {"de":"Wurfaxt","en":"Throwing Axe"}, "ammo", "normal", slot="ammo", price_silver=16, damage=9, damage_type="distance", weapon_class="wurf-axt", icon="item_throwing-axe"),
    "greatsword": ItemDef("greatsword", {"de":"Zweihandschwert","en":"Greatsword"}, "weapon", "gehärtet", slot="weapon", price_silver=58, damage=21, damage_type="melee", weapon_class="zweihand-schwert", socket_slots=2, icon="item_greatsword"),
    "halberd": ItemDef("halberd", {"de":"Hellebarde","en":"Halberd"}, "weapon", "gehärtet", slot="weapon", price_silver=54, damage=19, damage_type="melee", weapon_class="hellebarde", socket_slots=2, icon="item_halberd"),
    "katana": ItemDef("katana", {"de":"Katana","en":"Katana"}, "weapon", "geschärft", slot="weapon", price_silver=52, damage=18, damage_type="melee", weapon_class="katana", socket_slots=2, icon="item_katana"),
    "sabre": ItemDef("sabre", {"de":"Säbel","en":"Sabre"}, "weapon", "geschärft", slot="weapon", price_silver=37, damage=14, damage_type="melee", weapon_class="saebel", socket_slots=1, icon="item_sabre"),
    "dagger": ItemDef("dagger", {"de":"Dolch","en":"Dagger"}, "weapon", "normal", slot="weapon", price_silver=15, damage=9, damage_type="melee", weapon_class="dolch", socket_slots=1, icon="item_dagger"),
    "chain_hauberk": ItemDef("chain_hauberk", {"de":"Kettenhemd","en":"Chain Hauberk"}, "armor", "normal", slot="armor", price_silver=46, armor=16, icon="item_chain-hauberk"),
    "pilgrim_charm": ItemDef("pilgrim_charm", {"de":"Pilgeramulett","en":"Pilgrim Charm"}, "accessory", "veredelt", slot="accessory", price_silver=20, icon="item_pilgrim-charm"),
    "healing_draught": ItemDef("healing_draught", {"de":"Heiltrunk","en":"Healing Draught"}, "consumable", "normal", price_silver=12, buffs=({"type":"heal","value":24,"duration":0},), icon="item_healing-draught"),
    "lucky_tonic": ItemDef("lucky_tonic", {"de":"Glückstonikum","en":"Lucky Tonic"}, "consumable", "normal", price_silver=18, buffs=({"type":"loot_luck","value":100,"duration":6},), icon="item_lucky-tonic"),
    "war_oil": ItemDef("war_oil", {"de":"Kriegsöl","en":"War Oil"}, "consumable", "normal", price_silver=22, buffs=({"type":"damage_bonus","value":30,"duration":5},), icon="item_war-oil"),
    "quickstep_tonic": ItemDef("quickstep_tonic", {"de":"Schritttinktur","en":"Quickstep Tonic"}, "consumable", "normal", price_silver=20, buffs=({"type":"speed","value":10,"duration":5},), icon="item_quickstep-tonic"),
    "ward_salt": ItemDef("ward_salt", {"de":"Schutzsalz","en":"Ward Salt"}, "consumable", "normal", price_silver=22, buffs=({"type":"resistance_bonus","value":100,"duration":5},), icon="item_ward-salt"),
    "strength_manual": ItemDef("strength_manual", {"de":"Lehrbuch der Stärke","en":"Manual of Strength"}, "book", "veredelt", price_silver=60, permanent_bonus={"strength":10}, pages=pages(("Der Rücken beugt sich nicht vor Last, sondern vor Gewohnheit.","The back bends not to weight, but to habit."),("Jede Wiederholung hämmert Willen in Fleisch.","Each repetition hammers will into flesh.")), icon="item_strength-manual"),
    "chronicle_graufurt": ItemDef("chronicle_graufurt", {"de":"Chronik Graufurts","en":"Chronicle of Graufurt"}, "book", "normal", price_silver=14, pages=pages(("Graufurt notiert jede Steuer, aber kaum je die Tränen.","Graufurt records every tax, and hardly ever the tears."),("Am Osttor beginnt jede Lüge als Gerücht.","At the east gate every lie begins as rumor.")), icon="item_chronicle-graufurt"),
    "fireball_scroll": ItemDef("fireball_scroll", {"de":"Schriftrolle: Feuerball","en":"Scroll: Fireball"}, "scroll", "magisch", price_silver=32, charges=1, icon="item_fireball-scroll"),
    "lightning_orb_scroll": ItemDef("lightning_orb_scroll", {"de":"Schriftrolle: Kugelblitz","en":"Scroll: Lightning Orb"}, "scroll", "magisch", price_silver=34, charges=1, icon="item_lightning-orb-scroll"),
    "lightning_strike_scroll": ItemDef("lightning_strike_scroll", {"de":"Schriftrolle: Blitzschlag","en":"Scroll: Lightning Strike"}, "scroll", "magisch", price_silver=36, charges=1, icon="item_lightning-strike-scroll"),
    "fire_wall_scroll": ItemDef("fire_wall_scroll", {"de":"Schriftrolle: Feuerwand","en":"Scroll: Fire Wall"}, "scroll", "magisch", price_silver=38, charges=1, icon="item_fire-wall-scroll"),
    "fire_beam_scroll": ItemDef("fire_beam_scroll", {"de":"Schriftrolle: Feuerstrahl","en":"Scroll: Fire Beam"}, "scroll", "magisch", price_silver=40, charges=1, icon="item_fire-beam-scroll"),
    "silver_coin": ItemDef("silver_coin", {"de":"Silbermünze","en":"Silver Coin"}, "currency", "normal", price_silver=1, icon="item_silver-coin"),
    "gold_coin": ItemDef("gold_coin", {"de":"Goldmünze","en":"Gold Coin"}, "currency", "normal", price_silver=100, icon="item_gold-coin"),
}
for gem in ["diamond","onyx","sapphire","ruby","smaragd","calcedon","bergkristall","zirkon","bernstein","opal","obsidian"]:
    ITEMS[f"{gem}_shard"] = ItemDef(f"{gem}_shard", {"de":f"{gem.title()}-Splitter","en":f"{gem.title()} Shard"}, "gem", "normal", price_silver=24, icon=f"item_{gem}-shard")
for resource, price in [("iron_ore", 6),("wood_bundle",4),("leather_strip",5),("mithril_ore", 20),("steel_ingot",14)]:
    ITEMS[resource] = ItemDef(resource, {"de":resource.replace("_"," ").title(), "en":resource.replace("_"," ").title()}, "resource", "normal", price_silver=price, icon=f"item_{resource.replace('_','-')}")
for soulstone in ["petty","lesser","common","greater","grand"]:
    ITEMS[f"soulstone_{soulstone}"] = ItemDef(f"soulstone_{soulstone}", {"de":f"Seelenstein {soulstone.title()}","en":f"{soulstone.title()} Soulstone"}, "soulstone", "magisch", price_silver=40, icon=f"item_soulstone-{soulstone}")

# merchant stock
MERCHANT_STOCK = {
    "Graufurt": ["iron_sword","short_sword","oak_bow","chain_hauberk","buckler","healing_draught","lucky_tonic","chronicle_graufurt","throwing_knife"],
    "Valmora-Hain": ["dagger","sabre","spell_wand","quickstep_tonic","ward_salt","opal_shard","smaragd_shard","wood_bundle"],
    "Aschenwall": ["battle_axe","greatsword","halberd","war_oil","fireball_scroll","ruby_shard","iron_ore","steel_ingot"],
}

RECIPES = {
    "iron sword": {"materials": {"iron_ore": 3, "wood_bundle": 1}, "result": "iron_sword"},
    "steel sword": {"materials": {"steel_ingot": 3, "wood_bundle": 1}, "result": "steel_sword"},
    "oak bow": {"materials": {"wood_bundle": 3, "leather_strip": 1}, "result": "oak_bow"},
    "chain hauberk": {"materials": {"iron_ore": 5, "leather_strip": 2}, "result": "chain_hauberk"},
    "buckler": {"materials": {"wood_bundle": 2, "iron_ore": 1}, "result": "buckler"},
}

BUILDINGS = {
    "faction-outpost": BuildingDef("faction-outpost", {"de":"Fraktions-Außenposten","en":"Faction Outpost"}, "military",
        {"wood_bundle":10,"iron_ore":6,"silver_coin":40}, {"silver_coin":25}, {"taxes":2,"control":3}, {"silver_coin":2},
        ("rival-faction",), {"de":"Sichert Grenzen und provoziert Rivalen.", "en":"Secures borders and provokes rivals."}, "building_faction-outpost"),
    "faction-camp": BuildingDef("faction-camp", {"de":"Fraktionslager","en":"Faction Camp"}, "military",
        {"wood_bundle":14,"iron_ore":8,"silver_coin":60}, {"silver_coin":35}, {"taxes":3,"control":5,"militia-cap":10}, {"silver_coin":3},
        ("rival-faction",), {"de":"Versorgt Garnisonen und Feldzüge.", "en":"Supplies garrisons and field campaigns."}, "building_faction-camp"),
    "faction-fortress": BuildingDef("faction-fortress", {"de":"Fraktionsfestung","en":"Faction Fortress"}, "military",
        {"wood_bundle":25,"steel_ingot":18,"silver_coin":140}, {"silver_coin":80}, {"taxes":5,"control":10,"militia-cap":25}, {"silver_coin":6},
        ("forest-spirit",), {"de":"Massive Befestigung mit hohem politischen Gewicht.", "en":"Massive fortification with political weight."}, "building_faction-fortress"),
    "lumber-camp": BuildingDef("lumber-camp", {"de":"Holzlager","en":"Lumber Camp"}, "economic",
        {"wood_bundle":6,"silver_coin":20}, {"silver_coin":10}, {"wood_bundle":4}, {"silver_coin":1},
        ("valmora",), {"de":"Erhöht Holzoutput, verschärft Konflikte mit Waldfraktionen.", "en":"Raises timber output and sharpens conflicts with forest factions."}, "building_lumber-camp"),
    "iron-mine": BuildingDef("iron-mine", {"de":"Eisenmine","en":"Iron Mine"}, "economic",
        {"wood_bundle":8,"iron_ore":4,"silver_coin":28}, {"silver_coin":16}, {"iron_ore":4}, {"silver_coin":1},
        (), {"de":"Fördert Eisen aus lokalen Vorkommen.", "en":"Extracts iron from local veins."}, "building_iron-mine"),
    "mithril-shaft": BuildingDef("mithril-shaft", {"de":"Mithrilschacht","en":"Mithril Shaft"}, "economic",
        {"wood_bundle":12,"steel_ingot":8,"silver_coin":90}, {"silver_coin":50}, {"mithril_ore":2}, {"silver_coin":3},
        (), {"de":"Tiefe Förderung mit enormen Kosten.", "en":"Deep extraction at enormous cost."}, "building_mithril-shaft"),
    "steelworks": BuildingDef("steelworks", {"de":"Stahlwerk","en":"Steelworks"}, "economic",
        {"iron_ore":10,"wood_bundle":5,"silver_coin":44}, {"silver_coin":22}, {"steel_ingot":3}, {"silver_coin":2},
        (), {"de":"Veredelt Rohstoffe zu militärischem Kernmaterial.", "en":"Refines raw materials into military core stock."}, "building_steelworks"),
    "watchtower": BuildingDef("watchtower", {"de":"Wachturm","en":"Watchtower"}, "support",
        {"wood_bundle":5,"iron_ore":2,"silver_coin":18}, {"silver_coin":8}, {"fow":2,"control":2}, {"silver_coin":1},
        (), {"de":"Verbessert Sicht und Randwarnungen.", "en":"Improves sight and frontier warnings."}, "building_watchtower"),
    "herb-garden": BuildingDef("herb-garden", {"de":"Kräutergarten","en":"Herb Garden"}, "support",
        {"wood_bundle":4,"silver_coin":14}, {"silver_coin":8}, {"alchemy":2}, {"silver_coin":1},
        (), {"de":"Lieferkette für Heilkunde, Hexen und Alchemie.", "en":"Supply chain for healing, hedge witches and alchemy."}, "building_herb-garden"),
    "trade-hall": BuildingDef("trade-hall", {"de":"Handelshalle","en":"Trade Hall"}, "economic",
        {"wood_bundle":8,"iron_ore":3,"silver_coin":35}, {"silver_coin":18}, {"taxes":6,"market":4}, {"silver_coin":2},
        (), {"de":"Erhöht Angebot, Nachfrage und Zolleffizienz.", "en":"Raises supply, demand and tariff efficiency."}, "building_trade-hall"),
}

UNITS = {
    "swordfighters": UnitDef("swordfighters", {"de":"Schwertkämpfer","en":"Sword Fighters"}, "frontline", 2, 8, 8, False, {"offense": 1}, "unit_swordfighters"),
    "archers": UnitDef("archers", {"de":"Bogenschützen","en":"Archers"}, "ranged", 2, 7, 4, True, {"ranged": 2}, "unit_archers"),
    "spearmen": UnitDef("spearmen", {"de":"Speerträger","en":"Spearmen"}, "anti-cavalry", 2, 7, 7, False, {"defense": 1}, "unit_spearmen"),
    "shield-guard": UnitDef("shield-guard", {"de":"Schildwache","en":"Shield Guard"}, "defense", 3, 5, 10, False, {"defense": 2}, "unit_shield-guard"),
    "scouts": UnitDef("scouts", {"de":"Kundschafter","en":"Scouts"}, "recon", 2, 6, 5, True, {"fow": 2}, "unit_scouts"),
    "engineers": UnitDef("engineers", {"de":"Pioniere","en":"Engineers"}, "support", 3, 4, 6, False, {"build": 2}, "unit_engineers"),
}

# 20+ monster classes
MONSTER_CLASSES = {
    "wolf_pack": MonsterClass("wolf_pack", {"de":"Wolfsrudel","en":"Wolf Pack"}, "Bestie", "Wilde Tiere", 3, 28, "melee", "physical", 9, 2, 6, 4, 12, 9, 7, 1, 8, (("wood_bundle",1,2),), 2, 4, "monster_wolf-pack", ("Schwarzwurzelwald","Düsterforst")),
    "gravebound_pair": MonsterClass("gravebound_pair", {"de":"Grabgebundene","en":"Gravebound"}, "Untoter", "Untote", 4, 36, "magic", "unholy", 11, 4, 10, 8, 5, 8, 8, 1, 2, (("calcedon_shard",1,1),), 2, 3, "monster_gravebound-pair", ("Nebelmoor","Mondsumpf"), {"holy":-20,"unholy":20}),
    "ash_bandits": MonsterClass("ash_bandits", {"de":"Aschenbanditen","en":"Ash Bandits"}, "Mensch", "Banditen", 4, 34, "melee", "physical", 10, 3, 7, 7, 10, 10, 8, 3, 4, (("silver_coin",3,8),("iron_ore",1,2)), 2, 3, "monster_ash-bandits", ("Aschensteppe","Grenzland")),
    "cinder_imps": MonsterClass("cinder_imps", {"de":"Glutwichtel","en":"Cinder Imps"}, "Dämon", "Dämonen", 4, 26, "magic", "fire", 11, 1, 8, 11, 12, 9, 5, 0, 7, (("ruby_shard",1,1),), 2, 4, "monster_cinder-imps", ("Aschensteppe","Lavakessel"), {"fire":20,"water":-15}),
    "storm_harrier": MonsterClass("storm_harrier", {"de":"Sturmjäger","en":"Storm Harrier"}, "Bestie", "Wilde Monster", 5, 31, "distance", "storm", 12, 2, 8, 6, 14, 11, 7, 0, 9, (("bernstein_shard",1,1),), 1, 2, "monster_storm-harrier", ("Donnermesa","Sturmschlucht"), {"storm":20,"stone":-10}),
    "reef_stalker": MonsterClass("reef_stalker", {"de":"Riffschleicher","en":"Reef Stalker"}, "Leviathanbrut", "Leviathane", 5, 44, "melee", "water", 13, 4, 8, 7, 10, 11, 9, 3, 5, (("diamond_shard",1,1),), 1, 2, "monster_reef-stalker", ("Leviathanküste","Silberküste"), {"water":20,"lightning":-10}),
    "ice_shambler": MonsterClass("ice_shambler", {"de":"Frostschlurfer","en":"Ice Shambler"}, "Untoter", "Untote", 5, 48, "magic", "ice", 14, 5, 10, 8, 6, 9, 8, 2, 3, (("diamond_shard",1,1),), 1, 1, "monster_ice-shambler", ("Hohlfrost-Tundra",), {"ice":25,"fire":-20}),
    "opal_mirage": MonsterClass("opal_mirage", {"de":"Opalspiegel","en":"Opal Mirage"}, "Geist", "Antiker", 6, 34, "magic", "illusion", 15, 2, 13, 14, 12, 12, 7, 0, 9, (("opal_shard",1,1),), 1, 2, "monster_opal-mirage", ("Kristalldünen","Mondsumpf"), {"illusion":30,"soul":-10}),
    "obsidian_myrmidon": MonsterClass("obsidian_myrmidon", {"de":"Obsidianmyrmidon","en":"Obsidian Myrmidon"}, "Antiker", "Antiker", 6, 52, "melee", "shadow", 15, 6, 11, 9, 8, 12, 11, 5, 4, (("obsidian_shard",1,1),("iron_ore",2,3)), 1, 2, "monster_obsidian-myrmidon", ("Obsidianweite","Basaltkessel"), {"shadow":20,"holy":-15}),
    "jade_serpent": MonsterClass("jade_serpent", {"de":"Jadeschlange","en":"Jade Serpent"}, "Bestie", "Wilde Monster", 6, 39, "melee", "poison", 14, 3, 8, 6, 13, 11, 7, 1, 10, (("smaragd_shard",1,1),), 1, 2, "monster_jade-serpent", ("Jade-Dschungel","Dornenwildnis"), {"poison":20}),
    "ironbark_watcher": MonsterClass("ironbark_watcher", {"de":"Eisenrindenwächter","en":"Ironbark Watcher"}, "Elementar", "Waldgeister", 6, 55, "melee", "stone", 14, 7, 10, 8, 7, 10, 11, 4, 3, (("wood_bundle",2,4),), 1, 1, "monster_ironbark-watcher", ("Schwarzwurzelwald","Düsterforst"), {"stone":25,"fire":-15}),
    "bog_hexer": MonsterClass("bog_hexer", {"de":"Moorhexer","en":"Bog Hexer"}, "Mensch", "Ketzer", 6, 33, "magic", "soul", 15, 2, 14, 12, 8, 11, 7, 0, 6, (("calcedon_shard",1,1),), 1, 1, "monster_bog-hexer", ("Sonnenmoor","Nebelmoor"), {"soul":15,"holy":-15}),
    "basalt_giantling": MonsterClass("basalt_giantling", {"de":"Basaltling","en":"Basalt Giantling"}, "Titanensplitter", "Titanen", 7, 66, "melee", "stone", 17, 8, 8, 6, 5, 10, 10, 6, 2, (("zirkon_shard",1,1),("iron_ore",2,4)), 1, 1, "monster_basalt-giantling", ("Basaltkessel","Himmelsbruch"), {"stone":30,"storm":-10}),
    "thunder_owl": MonsterClass("thunder_owl", {"de":"Donnereule","en":"Thunder Owl"}, "Bestie", "Wilde Tiere", 5, 31, "distance", "lightning", 12, 2, 9, 8, 14, 11, 7, 0, 9, (("bernstein_shard",1,1),), 1, 2, "monster_thunder-owl", ("Donnermesa","Sturmschlucht"), {"lightning":20}),
    "hollow_fiend": MonsterClass("hollow_fiend", {"de":"Hohlendieb","en":"Hollow Fiend"}, "Dämon", "Dämonen", 6, 45, "melee", "unholy", 15, 4, 10, 9, 11, 11, 8, 2, 7, (("onyx_shard",1,1),), 1, 2, "monster_hollow-fiend", ("Hohlfrost-Tundra","Obsidianweite"), {"unholy":20,"holy":-20}),
    "sunken_crab": MonsterClass("sunken_crab", {"de":"Versunkene Schere","en":"Sunken Crab"}, "Leviathanbrut", "Leviathane", 4, 41, "melee", "water", 11, 5, 6, 4, 6, 8, 10, 4, 2, (("diamond_shard",1,1),), 1, 3, "monster_sunken-crab", ("Leviathanküste","Sonnenmoor"), {"water":15}),
    "dune_glassling": MonsterClass("dune_glassling", {"de":"Dünenglasling","en":"Dune Glassling"}, "Elementar", "Elementarwesen", 5, 29, "magic", "fire", 13, 1, 9, 10, 13, 10, 7, 0, 8, (("opal_shard",1,1),("ruby_shard",1,1)), 1, 3, "monster_dune-glassling", ("Kristalldünen",), {"fire":10,"stone":-10}),
    "salt_lich": MonsterClass("salt_lich", {"de":"Salzlurch","en":"Salt Lich"}, "Untoter", "Untote", 7, 50, "magic", "soul", 16, 3, 15, 13, 8, 11, 9, 0, 5, (("silver_coin",8,14),), 1, 1, "monster_salt-lich", ("Salzebenen",), {"soul":20,"holy":-20}),
    "ember_clerk": MonsterClass("ember_clerk", {"de":"Glutschreiber","en":"Ember Clerk"}, "Dämon", "Dämonen", 6, 37, "magic", "fire", 14, 2, 12, 11, 9, 10, 7, 0, 6, (("ruby_shard",1,1),), 1, 1, "monster_ember-clerk", ("Aschensteppe","Lavakessel"), {"fire":25}),
    "thorn_howler": MonsterClass("thorn_howler", {"de":"Dornenheuler","en":"Thorn Howler"}, "Bestie", "Wilde Monster", 7, 43, "melee", "poison", 16, 4, 8, 7, 12, 11, 8, 1, 9, (("smaragd_shard",1,1),), 1, 2, "monster_thorn-howler", ("Dornenwildnis",), {"poison":25}),
    "sky_cutter": MonsterClass("sky_cutter", {"de":"Himmelschlitzer","en":"Sky Cutter"}, "Elementar", "Elementarwesen", 7, 40, "distance", "storm", 16, 2, 9, 12, 15, 12, 7, 0, 10, (("bernstein_shard",1,1),), 1, 2, "monster_sky-cutter", ("Himmelsbruch","Sturmschlucht"), {"storm":30}),
    "raven_monk": MonsterClass("raven_monk", {"de":"Rabenmönch","en":"Raven Monk"}, "Mensch", "Ketzer", 7, 42, "magic", "shadow", 16, 3, 12, 13, 9, 12, 8, 1, 7, (("obsidian_shard",1,1),), 1, 1, "monster_raven-monk", ("Rabensteppe","Düsterforst"), {"shadow":20}),
    "silver_tide": MonsterClass("silver_tide", {"de":"Silberflut","en":"Silver Tide"}, "Leviathanbrut", "Leviathane", 7, 49, "magic", "water", 17, 4, 11, 12, 8, 11, 9, 0, 6, (("diamond_shard",1,1),("opal_shard",1,1)), 1, 2, "monster_silver-tide", ("Silberküste",), {"water":25}),
    "amber_warden": MonsterClass("amber_warden", {"de":"Bernsteinhüter","en":"Amber Warden"}, "Geist", "Antiker", 6, 38, "magic", "storm", 15, 3, 12, 11, 10, 11, 8, 0, 7, (("bernstein_shard",1,1),), 1, 1, "monster_amber-warden", ("Bernsteinfeld",), {"storm":20,"stone":-10}),
}

TRAVEL_ENCOUNTERS = [
    TravelEncounter("broken_wagon_rut", {"de":"Zerbrochene Wagenrinne","en":"Broken Wagon Rut"}, {"de":"Ein gebrochener Wagen zwingt Reisende zum Umweg und birgt verlorene Ware.", "en":"A broken wagon forces travellers into a detour and hides lost cargo."}, ("Kornmark-Auen","Grenzland"), "event_broken-wagon-rut"),
    TravelEncounter("pilgrim_fire", {"de":"Pilgerfeuer","en":"Pilgrim Fire"}, {"de":"Müde Pilger hüten eine stille Feuerstelle und mehr Fragen als Antworten.", "en":"Tired pilgrims keep a quiet fire and more questions than answers."}, ("Kornmark-Auen","Grenzland"), "event_pilgrim-fire"),
    TravelEncounter("wolf_signs", {"de":"Rudelspuren","en":"Pack Signs"}, {"de":"Frische Kratzspuren zeigen, dass hier ein Rudel kreuzt.", "en":"Fresh claw marks show that a pack crosses here."}, ("Schwarzwurzelwald","Düsterforst"), "event_wolf-signs"),
    TravelEncounter("broken_bell", {"de":"Gebrochene Glocke","en":"Broken Bell"}, {"de":"Von einem Schreinpfahl hängt eine Glocke, die bei Wind nicht mehr läutet.", "en":"A bell hangs from a shrine post, but the wind no longer makes it ring."}, ("Grenzland","Nebelmoor"), "event_broken-bell"),
    TravelEncounter("marsh_lights", {"de":"Moorlichter","en":"Marsh Lights"}, {"de":"Lichter gleiten knapp über dem Wasser und warten auf einen falschen Schritt.", "en":"Lights drift just above the water and wait for a wrong step."}, ("Nebelmoor","Mondsumpf"), "event_marsh-lights"),
    TravelEncounter("ash_rain", {"de":"Ascheregen","en":"Ash Rain"}, {"de":"Feine Asche legt sich wie Mehl über Haut und Klinge.", "en":"Fine ash settles like flour over skin and blade."}, ("Aschensteppe","Lavakessel"), "event_ash-rain"),
    TravelEncounter("root_whisper", {"de":"Wurzelflüstern","en":"Root Whisper"}, {"de":"Die Wurzeln knacken, als würden sie Ratschläge austauschen.", "en":"Roots crack as if exchanging advice."}, ("Schwarzwurzelwald","Düsterforst"), "event_root-whisper"),
    TravelEncounter("double_toll", {"de":"Doppelzoll","en":"Double Toll"}, {"de":"Zwei Parteien beanspruchen dieselbe Brücke und dieselbe Geduld.", "en":"Two factions claim the same bridge and the same patience."}, ("Kornmark-Auen","Flusshain"), "event_double-toll"),
    TravelEncounter("raven_circle", {"de":"Krähenkreis","en":"Raven Circle"}, {"de":"Krähen kreisen über einer Stelle, an der etwas vergraben wurde.", "en":"Crows circle above a place where something was buried."}, ("Schwarzwurzelwald","Rabensteppe"), "event_raven-circle"),
    TravelEncounter("wounded_courier", {"de":"Verwundeter Kurier","en":"Wounded Courier"}, {"de":"Ein Kurier ringt mit Atem, Schuld und einer nassen Kartentasche.", "en":"A courier wrestles with breath, guilt, and a soaked map satchel."}, ("Kornmark-Auen","Aschensteppe"), "event_wounded-courier"),
]

ELEMENT_MATRIX = {}
types = ["fire","water","ice","lightning","storm","earth","stone","metal","holy","unholy","soul","poison","illusion","shadow","melee","distance","physical"]
for a in types:
    for b in types:
        ELEMENT_MATRIX[(a,b)] = 1.0
# A few tuned interactions
for key,val in {
    ("fire","ice"):1.35,("fire","water"):0.65,("water","fire"):1.25,("lightning","water"):1.3,("storm","stone"):0.85,
    ("earth","lightning"):0.9,("stone","storm"):1.15,("holy","unholy"):1.35,("unholy","holy"):1.2,("poison","bestial"):1.1,
    ("shadow","holy"):0.75,("illusion","soul"):1.1,("ice","fire"):0.65,("metal","lightning"):1.15,("lightning","metal"):1.1,
}.items():
    ELEMENT_MATRIX[key]=val
