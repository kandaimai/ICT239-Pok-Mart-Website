from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

poke_mart_items = [
    # === BASIC HEALING ITEMS ===
    {
        "id": 1,
        "name": "Potion",
        "description": "Restores 20 HP to a single Pokémon.",
        "price": 200
    },
    {
        "id": 2,
        "name": "Super Potion",
        "description": "Restores 60 HP to a single Pokémon.",
        "price": 700
    },
    {
        "id": 3,
        "name": "Hyper Potion",
        "description": "Restores 120 HP to a single Pokémon.",
        "price": 1200
    },
    {
        "id": 4,
        "name": "Max Potion",
        "description": "Fully restores a Pokémon’s HP.",
        "price": 2500
    },
    {
        "id": 5,
        "name": "Full Restore",
        "description": "Fully restores HP and heals all status conditions.",
        "price": 3000
    },
    {
        "id": 6,
        "name": "Antidote",
        "description": "Cures a poisoned Pokémon.",
        "price": 100
    },
    {
        "id": 7,
        "name": "Paralyze Heal",
        "description": "Cures a paralyzed Pokémon.",
        "price": 200
    },
    {
        "id": 8,
        "name": "Awakening",
        "description": "Wakes up a sleeping Pokémon.",
        "price": 250
    },
    {
        "id": 9,
        "name": "Burn Heal",
        "description": "Heals a burned Pokémon.",
        "price": 250
    },
    {
        "id": 10,
        "name": "Ice Heal",
        "description": "Thaws out a frozen Pokémon.",
        "price": 250
    },

    # === STATUS AND REVIVAL ITEMS ===
    {
        "id": 11,
        "name": "Full Heal",
        "description": "Cures all status conditions of a Pokémon.",
        "price": 600
    },
    {
        "id": 12,
        "name": "Revive",
        "description": "Revives a fainted Pokémon with half of its maximum HP.",
        "price": 1500
    },
    {
        "id": 13,
        "name": "Max Revive",
        "description": "Revives a fainted Pokémon with full HP.",
        "price": 4000
    },

    # === POWER & PP RESTORATION ===
    {
        "id": 14,
        "name": "Ether",
        "description": "Restores 10 PP of one selected move.",
        "price": 1200
    },
    {
        "id": 15,
        "name": "Max Ether",
        "description": "Fully restores the PP of one move.",
        "price": 2000
    },
    {
        "id": 16,
        "name": "Elixir",
        "description": "Restores 10 PP to each move of one Pokémon.",
        "price": 3000
    },
    {
        "id": 17,
        "name": "Max Elixir",
        "description": "Fully restores the PP of all moves of one Pokémon.",
        "price": 4500
    },

    # === REPELS ===
    {
        "id": 18,
        "name": "Repel",
        "description": "Repels weak wild Pokémon for 100 steps.",
        "price": 350
    },
    {
        "id": 19,
        "name": "Super Repel",
        "description": "Repels weak wild Pokémon for 200 steps.",
        "price": 500
    },
    {
        "id": 20,
        "name": "Max Repel",
        "description": "Repels weak wild Pokémon for 250 steps.",
        "price": 700
    },

    # === BALLS ===
    {
        "id": 21,
        "name": "Poké Ball",
        "description": "A device for catching wild Pokémon. Basic capture rate.",
        "price": 200
    },
    {
        "id": 22,
        "name": "Great Ball",
        "description": "A good-quality Ball with a higher catch rate than a Poké Ball.",
        "price": 600
    },
    {
        "id": 23,
        "name": "Ultra Ball",
        "description": "An ultra-performance Ball with a high catch rate.",
        "price": 1200
    },
    {
        "id": 24,
        "name": "Premier Ball",
        "description": "A commemorative Ball with a sleek white design.",
        "price": 200
    },
    {
        "id": 25,
        "name": "Luxury Ball",
        "description": "A comfortable Ball that makes Pokémon grow friendlier.",
        "price": 1000
    },
    {
        "id": 26,
        "name": "Quick Ball",
        "description": "Works best if used at the start of a wild encounter.",
        "price": 1000
    },
    {
        "id": 27,
        "name": "Timer Ball",
        "description": "Becomes more effective at catching Pokémon as battle drags on.",
        "price": 1000
    },
    {
        "id": 28,
        "name": "Dusk Ball",
        "description": "Works better in dark places like caves or at night.",
        "price": 1000
    },
    {
        "id": 29,
        "name": "Net Ball",
        "description": "Works well on Water- and Bug-type Pokémon.",
        "price": 1000
    },
    {
        "id": 30,
        "name": "Heal Ball",
        "description": "Restores HP and heals status when catching a Pokémon.",
        "price": 300
    },

    # === BATTLE ITEMS ===
    {
        "id": 31,
        "name": "X Attack",
        "description": "Temporarily boosts Attack during battle.",
        "price": 500
    },
    {
        "id": 32,
        "name": "X Defense",
        "description": "Temporarily boosts Defense during battle.",
        "price": 550
    },
    {
        "id": 33,
        "name": "X Speed",
        "description": "Temporarily boosts Speed during battle.",
        "price": 350
    },
    {
        "id": 34,
        "name": "X Sp. Atk",
        "description": "Temporarily boosts Special Attack during battle.",
        "price": 350
    },
    {
        "id": 35,
        "name": "Guard Spec.",
        "description": "Prevents stat reduction for five turns.",
        "price": 700
    },
    {
        "id": 36,
        "name": "Dire Hit",
        "description": "Raises critical-hit ratio during one battle.",
        "price": 650
    },

    # === EV/STAT-BOOSTING VITAMINS ===
    {
        "id": 37,
        "name": "Protein",
        "description": "Increases a Pokémon’s base Attack stat.",
        "price": 9800
    },
    {
        "id": 38,
        "name": "Iron",
        "description": "Increases a Pokémon’s base Defense stat.",
        "price": 9800
    },
    {
        "id": 39,
        "name": "Calcium",
        "description": "Increases a Pokémon’s base Special Attack stat.",
        "price": 9800
    },
    {
        "id": 40,
        "name": "Zinc",
        "description": "Increases a Pokémon’s base Special Defense stat.",
        "price": 9800
    },
    {
        "id": 41,
        "name": "Carbos",
        "description": "Increases a Pokémon’s base Speed stat.",
        "price": 9800
    },
    {
        "id": 42,
        "name": "HP Up",
        "description": "Increases a Pokémon’s base HP stat.",
        "price": 9800
    },
    {
        "id": 43,
        "name": "PP Up",
        "description": "Slightly increases the maximum PP of a move.",
        "price": 9800
    },
    {
        "id": 44,
        "name": "PP Max",
        "description": "Maximizes the PP of a selected move.",
        "price": 20000
    },

    # === HELD ITEMS AND MISC ===
    {
        "id": 45,
        "name": "Escape Rope",
        "description": "Used to escape instantly from caves or dungeons.",
        "price": 550
    },
    {
        "id": 46,
        "name": "Poké Doll",
        "description": "Helps you escape from a battle with a wild Pokémon.",
        "price": 1000
    },
    {
        "id": 47,
        "name": "Air Mail",
        "description": "A letter that can be attached to a held Pokémon for trade.",
        "price": 50
    },
    {
        "id": 48,
        "name": "Rare Candy",
        "description": "Raises a Pokémon’s level by one.",
        "price": 4800
    },

    # === TECHNICAL MACHINES (TMs) ===
    {
        "id": 101,
        "name": "TM01 - Work Up",
        "description": "Raises the user’s Attack and Sp. Atk.",
        "price": 10000
    },
    {
        "id": 102,
        "name": "TM08 - Hyper Beam",
        "description": "A strong attack that leaves the user recharging next turn.",
        "price": 20000
    },
    {
        "id": 103,
        "name": "TM13 - Ice Beam",
        "description": "A chilling beam that may freeze the target.",
        "price": 12000
    },
    {
        "id": 104,
        "name": "TM24 - Thunderbolt",
        "description": "A strong electric attack that may paralyze the target.",
        "price": 12000
    },
    {
        "id": 105,
        "name": "TM35 - Flamethrower",
        "description": "A powerful fire attack that may burn the target.",
        "price": 12000
    },
    {
        "id": 106,
        "name": "TM36 - Sludge Bomb",
        "description": "A poisonous sludge attack that may poison the target.",
        "price": 12000
    },
    {
        "id": 107,
        "name": "TM41 - Facade",
        "description": "Power doubles if the user is poisoned, burned, or paralyzed.",
        "price": 8000
    },
    {
        "id": 108,
        "name": "TM73 - Thunder Wave",
        "description": "Paralyzes the target with an electrical shock.",
        "price": 6000
    },
    {
        "id": 109,
        "name": "TM85 - Dream Eater",
        "description": "Only works on sleeping targets. Restores HP equal to half the damage dealt.",
        "price": 8000
    },
    {
        "id": 110,
        "name": "TM92 - Fly",
        "description": "Flies up on the first turn, strikes on the second.",
        "price": 10000
    }
]
cart = []

@app.route('/')
@app.route('/shop', methods = ['GET'])  
def shop():
    return render_template('shop.html', poke_mart_items = poke_mart_items)

@app.route('/shop/<item_id>', methods = ['GET'])
def show_items(item_id):
    for item in poke_mart_items:
        if int(item_id) == item["id"]:
            item_dict = item
    return render_template('item.html', poke_mart_items = poke_mart_items, item = item_dict)

@app.route('/cart', methods = ['GET', 'POST'])
def handle_cart():
    return redirect(url_for("shop"))