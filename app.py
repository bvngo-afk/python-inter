import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# File to store inventory data
INVENTORY_FILE = "inventory.json"

def load_inventory():
    """Load inventory from a JSON file."""
    try:
        with open(INVENTORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_inventory():
    """Save inventory to a JSON file."""
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file)

def reset_inventory():
    """Reset the inventory by clearing all items."""
    global inventory
    inventory = {}
    save_inventory()

# Load inventory on startup
inventory = load_inventory()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'reset' in request.form:
            reset_inventory()
            return redirect(url_for('index'))
        
        item_name = request.form.get('item_name', '').strip().lower()  # Normalize input
        quantity = request.form.get('quantity')
        action = request.form.get('action')
        
        if item_name and quantity.isdigit():
            quantity = int(quantity)
            if action == 'Add':
                if item_name in inventory:
                    inventory[item_name] += quantity  # Update existing item quantity
                else:
                    inventory[item_name] = quantity  # Add new item
            elif action == 'Remove':
                if item_name in inventory:
                    inventory[item_name] -= quantity
                    if inventory[item_name] <= 0:
                        del inventory[item_name]  # Remove item if quantity is zero or negative
            
            save_inventory()  # Save updated inventory
        
        return redirect(url_for('index'))
    
    return render_template('index.html', inventory=inventory)

if __name__ == '__main__':
    app.run(debug=True)
