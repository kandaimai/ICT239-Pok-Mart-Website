from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.model import LoginForm, RegForm, Item, User
from app import app



poke_mart_items = [
    # === BASIC HEALING ITEMS ===
    {
        "item_id": 1,
        "item_name": "Potion",
        "item_description": "Restores 20 HP to a single Pokémon.",
        "item_price": 200,
        "item_quantity": 50
    },
    {
        "item_id": 2,
        "item_name": "Super Potion",
        "item_description": "Restores 60 HP to a single Pokémon.",
        "item_price": 700,
        "item_quantity": 40
    },
    {
        "item_id": 3,
        "item_name": "Hyper Potion",
        "item_description": "Restores 120 HP to a single Pokémon.",
        "item_price": 1200,
        "item_quantity": 30
    },
    {
        "item_id": 4,
        "item_name": "Max Potion",
        "item_description": "Fully restores a Pokémon’s HP.",
        "item_price": 2500,
        "item_quantity": 25
    },
    {
        "item_id": 5,
        "item_name": "Full Restore",
        "item_description": "Fully restores HP and heals all status conditions.",
        "item_price": 3000,
        "item_quantity": 20
    },
    {
        "item_id": 6,
        "item_name": "Antidote",
        "item_description": "Cures a poisoned Pokémon.",
        "item_price": 100,
        "item_quantity": 60
    },
    {
        "item_id": 7,
        "item_name": "Paralyze Heal",
        "item_description": "Cures a paralyzed Pokémon.",
        "item_price": 200,
        "item_quantity": 55
    },
    {
        "item_id": 8,
        "item_name": "Awakening",
        "item_description": "Wakes up a sleeping Pokémon.",
        "item_price": 250,
        "item_quantity": 50
    },
    {
        "item_id": 9,
        "item_name": "Burn Heal",
        "item_description": "Heals a burned Pokémon.",
        "item_price": 250,
        "item_quantity": 50
    },
    {
        "item_id": 10,
        "item_name": "Ice Heal",
        "item_description": "Thaws out a frozen Pokémon.",
        "item_price": 250,
        "item_quantity": 50
    },

    # === STATUS AND REVIVAL ITEMS ===
    {
        "item_id": 11,
        "item_name": "Full Heal",
        "item_description": "Cures all status conditions of a Pokémon.",
        "item_price": 600,
        "item_quantity": 40
    },
    {
        "item_id": 12,
        "item_name": "Revive",
        "item_description": "Revives a fainted Pokémon with half of its maximum HP.",
        "item_price": 1500,
        "item_quantity": 25
    },
    {
        "item_id": 13,
        "item_name": "Max Revive",
        "item_description": "Revives a fainted Pokémon with full HP.",
        "item_price": 4000,
        "item_quantity": 15
    },

    # === POWER & PP RESTORATION ===
    {
        "item_id": 14,
        "item_name": "Ether",
        "item_description": "Restores 10 PP of one selected move.",
        "item_price": 1200,
        "item_quantity": 20
    },
    {
        "item_id": 15,
        "item_name": "Max Ether",
        "item_description": "Fully restores the PP of one move.",
        "item_price": 2000,
        "item_quantity": 15
    },
    {
        "item_id": 16,
        "item_name": "Elixir",
        "item_description": "Restores 10 PP to each move of one Pokémon.",
        "item_price": 3000,
        "item_quantity": 10
    },
    {
        "item_id": 17,
        "item_name": "Max Elixir",
        "item_description": "Fully restores the PP of all moves of one Pokémon.",
        "item_price": 4500,
        "item_quantity": 8
    },

    # === REPELS ===
    {
        "item_id": 18,
        "item_name": "Repel",
        "item_description": "Repels weak wild Pokémon for 100 steps.",
        "item_price": 350,
        "item_quantity": 45
    },
    {
        "item_id": 19,
        "item_name": "Super Repel",
        "item_description": "Repels weak wild Pokémon for 200 steps.",
        "item_price": 500,
        "item_quantity": 40
    },
    {
        "item_id": 20,
        "item_name": "Max Repel",
        "item_description": "Repels weak wild Pokémon for 250 steps.",
        "item_price": 700,
        "item_quantity": 35
    },

    # === BALLS ===
    {
        "item_id": 21,
        "item_name": "Poké Ball",
        "item_description": "A device for catching wild Pokémon. Basic capture rate.",
        "item_price": 200,
        "item_quantity": 100
    },
    {
        "item_id": 22,
        "item_name": "Great Ball",
        "item_description": "A good-quality Ball with a higher catch rate than a Poké Ball.",
        "item_price": 600,
        "item_quantity": 80
    },
    {
        "item_id": 23,
        "item_name": "Ultra Ball",
        "item_description": "An ultra-performance Ball with a high catch rate.",
        "item_price": 1200,
        "item_quantity": 60
    },
    {
        "item_id": 24,
        "item_name": "Premier Ball",
        "item_description": "A commemorative Ball with a sleek white design.",
        "item_price": 200,
        "item_quantity": 50
    },
    {
        "item_id": 25,
        "item_name": "Luxury Ball",
        "item_description": "A comfortable Ball that makes Pokémon grow friendlier.",
        "item_price": 1000,
        "item_quantity": 40
    },
    {
        "item_id": 26,
        "item_name": "Quick Ball",
        "item_description": "Works best if used at the start of a wild encounter.",
        "item_price": 1000,
        "item_quantity": 30
    },
    {
        "item_id": 27,
        "item_name": "Timer Ball",
        "item_description": "Becomes more effective at catching Pokémon as battle drags on.",
        "item_price": 1000,
        "item_quantity": 30
    },
    {
        "item_id": 28,
        "item_name": "Dusk Ball",
        "item_description": "Works better in dark places like caves or at night.",
        "item_price": 1000,
        "item_quantity": 30
    },
    {
        "item_id": 29,
        "item_name": "Net Ball",
        "item_description": "Works well on Water- and Bug-type Pokémon.",
        "item_price": 1000,
        "item_quantity": 30
    },
    {
        "item_id": 30,
        "item_name": "Heal Ball",
        "item_description": "Restores HP and heals status when catching a Pokémon.",
        "item_price": 300,
        "item_quantity": 50
    },

    # === BATTLE ITEMS ===
    {
        "item_id": 31,
        "item_name": "X Attack",
        "item_description": "Temporarily boosts Attack during battle.",
        "item_price": 500,
        "item_quantity": 35
    },
    {
        "item_id": 32,
        "item_name": "X Defense",
        "item_description": "Temporarily boosts Defense during battle.",
        "item_price": 550,
        "item_quantity": 35
    },
    {
        "item_id": 33,
        "item_name": "X Speed",
        "item_description": "Temporarily boosts Speed during battle.",
        "item_price": 350,
        "item_quantity": 35
    },
    {
        "item_id": 34,
        "item_name": "X Sp. Atk",
        "item_description": "Temporarily boosts Special Attack during battle.",
        "item_price": 350,
        "item_quantity": 35
    },
    {
        "item_id": 35,
        "item_name": "Guard Spec.",
        "item_description": "Prevents stat reduction for five turns.",
        "item_price": 700,
        "item_quantity": 30
    },
    {
        "item_id": 36,
        "item_name": "Dire Hit",
        "item_description": "Raises critical-hit ratio during one battle.",
        "item_price": 650,
        "item_quantity": 30
    },

    # === EV/STAT-BOOSTING VITAMINS ===
    {
        "item_id": 37,
        "item_name": "Protein",
        "item_description": "Increases a Pokémon’s base Attack stat.",
        "item_price": 9800,
        "item_quantity": 15
    },
    {
        "item_id": 38,
        "item_name": "Iron",
        "item_description": "Increases a Pokémon’s base Defense stat.",
        "item_price": 9800,
        "item_quantity": 15
    },
    {
        "item_id": 39,
        "item_name": "Calcium",
        "item_description": "Increases a Pokémon’s base Special Attack stat.",
        "item_price": 9800,
        "item_quantity": 15
    },
    {
        "item_id": 40,
        "item_name": "Zinc",
        "item_description": "Increases a Pokémon’s base Special Defense stat.",
        "item_price": 9800,
        "item_quantity": 15
    },
    {
        "item_id": 41,
        "item_name": "Carbos",
        "item_description": "Increases a Pokémon’s base Speed stat.",
        "item_price": 9800,
        "item_quantity": 15
    },
    {
        "item_id": 42,
        "item_name": "HP Up",
        "item_description": "Increases a Pokémon’s base HP stat.",
        "item_price": 9800,
        "item_quantity": 15
    },
    {
        "item_id": 43,
        "item_name": "PP Up",
        "item_description": "Slightly increases the maximum PP of a move.",
        "item_price": 9800,
        "item_quantity": 10
    },
    {
        "item_id": 44,
        "item_name": "PP Max",
        "item_description": "Maximizes the PP of a selected move.",
        "item_price": 20000,
        "item_quantity": 5
    },

    # === HELD ITEMS AND MISC ===
    {
        "item_id": 45,
        "item_name": "Escape Rope",
        "item_description": "Used to escape instantly from caves or dungeons.",
        "item_price": 550,
        "item_quantity": 40
    },
    {
        "item_id": 46,
        "item_name": "Poké Doll",
        "item_description": "Helps you escape from a battle with a wild Pokémon.",
        "item_price": 1000,
        "item_quantity": 25
    },
    {
        "item_id": 47,
        "item_name": "Air Mail",
        "item_description": "A letter that can be attached to a held Pokémon for trade.",
        "item_price": 50,
        "item_quantity": 100
    },
    {
        "item_id": 48,
        "item_name": "Rare Candy",
        "item_description": "Raises a Pokémon’s level by one.",
        "item_price": 4800,
        "item_quantity": 10
    },

    # === TECHNICAL MACHINES (TMs) ===
    {
        "item_id": 101,
        "item_name": "TM01 - Work Up",
        "item_description": "Raises the user’s Attack and Sp. Atk.",
        "item_price": 10000,
        "item_quantity": 8
    },
    {
        "item_id": 102,
        "item_name": "TM08 - Hyper Beam",
        "item_description": "A strong attack that leaves the user recharging next turn.",
        "item_price": 20000,
        "item_quantity": 5
    },
    {
        "item_id": 103,
        "item_name": "TM13 - Ice Beam",
        "item_description": "A chilling beam that may freeze the target.",
        "item_price": 12000,
        "item_quantity": 7
    },
    {
        "item_id": 104,
        "item_name": "TM24 - Thunderbolt",
        "item_description": "A strong electric attack that may paralyze the target.",
        "item_price": 12000,
        "item_quantity": 7
    },
    {
        "item_id": 105,
        "item_name": "TM35 - Flamethrower",
        "item_description": "A powerful fire attack that may burn the target.",
        "item_price": 12000,
        "item_quantity": 7
    },
    {
        "item_id": 106,
        "item_name": "TM36 - Sludge Bomb",
        "item_description": "A poisonous sludge attack that may poison the target.",
        "item_price": 12000,
        "item_quantity": 7
    },
    {
        "item_id": 107,
        "item_name": "TM41 - Facade",
        "item_description": "Power doubles if the user is poisoned, burned, or paralyzed.",
        "item_price": 8000,
        "item_quantity": 8
    },
    {
        "item_id": 108,
        "item_name": "TM73 - Thunder Wave",
        "item_description": "Paralyzes the target with an electrical shock.",
        "item_price": 6000,
        "item_quantity": 9
    },
    {
        "item_id": 109,
        "item_name": "TM85 - Dream Eater",
        "item_description": "Only works on sleeping targets. Restores HP equal to half the damage dealt.",
        "item_price": 8000,
        "item_quantity": 6
    },
    {
        "item_id": 110,
        "item_name": "TM92 - Fly",
        "item_description": "Flies up on the first turn, strikes on the second.",
        "item_price": 10000,
        "item_quantity": 8
    }
]

cart = []

@app.route('/')
@app.route('/shop', methods = ['GET'])  
def shop():
    #save item manually for testing
    '''
    Item.save_item(
        item_id = 2,
        item_name = "Super Potion",
        item_description = "Restores 60 HP to a single Pokémon.",
        item_price = 700,
        item_quantity = 4
    )
    '''
    '''
    for p in range(1, len(poke_mart_items), 1):
        Item.save_item(
            item_id=poke_mart_items[p]["item_id"],
            item_name=poke_mart_items[p]["item_name"],
            item_description=poke_mart_items[p]["item_description"],
            item_price=poke_mart_items[p]["item_price"],
            item_quantity=poke_mart_items[p]["item_quantity"]
        )
    '''
    items = Item.get_all_items()
    
    return render_template('shop.html', poke_mart_items = poke_mart_items)

@app.route('/shop/<item_id>', methods = ['GET'])
def show_items(item_id):
    for item in poke_mart_items:
        if int(item_id) == item["id"]:
            item_dict = item
    return render_template('item.html', poke_mart_items = poke_mart_items, item = item_dict)

@app.route('/cart', methods = ['GET', 'POST'])
@login_required
def handle_cart():
    if request.method == "GET":
        return "display cart"
    else:
        id = request.form["item_id"]
        quantity = request.form["quantity"]
        return f'id, {id}, quantity: {quantity}'
    

#login route
@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template("login.html", form = form)
    else:
        poketrainer_id = request.form['poketrainer_id']
        password = request.form['password']
        #return f'poketrainer_id: {poketrainer_id}, password: {password}'
        #authenticate user
        user = User.objects(poketrainer_id = poketrainer_id).first()
        if user:
            login_user(user)
            flash("Login Successful", "success")
            return redirect(url_for("shop"))
        else:
            flash("login unsuccessful", "danger")
            return redirect(url_for("register"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("shop"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegForm()
    if request.method == 'GET':
        return render_template("register.html", form = form)
    if form.validate_on_submit():
        poketrainer_id = request.form['poketrainer_id']
        password = request.form['password']
        email = request.form['email']
        #return f'poketrainer_id: {poketrainer_id}, password: {password}, email: {email}'
        if User.save_user(poketrainer_id, email, password):
            flash("Account created", 'success')
        else:
            flash("Unsuccssful", "danger")
        return redirect(url_for("login"))
    return render_template("register.html", form = form)