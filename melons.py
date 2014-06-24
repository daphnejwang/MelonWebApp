from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2


app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site""" 
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    melon_types = {}
    total_price = 0.00
    if "cart" in session:
        for key, quantity in session["cart"].iteritems():
            melon = model.get_melon_by_id(int(key))
            total = melon.price * quantity
            melon_types[melon.common_name] = {'quantity': quantity, 'price': melon.price, 'total': total}
            total_price += total
    return render_template("cart.html", display_melons=melon_types, total_price = total_price)
    
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.
    
    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """
    id = str(id)
    if "cart" in session:
        if id in session["cart"].keys():
            session["cart"][id] +=1
        else:
            session["cart"][id] = 1
    else:
        session["cart"] = {id: 1}
    flash("Successfully added to cart.")
    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    if "username" in session:
        message = "%s is logged in." % session['username']
        return render_template("logout.html", message=message)
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    test email: ashley@eimbee.biz, frances@jabbercube.org
    """
    error = None
    email = request.form['email']
    customer = model.get_customer_by_email(email)
    if customer:
        session['username'] = customer.first_name
        return redirect("/melons")
    else:
        error = 'Invalid username/password.'
    return render_template('login.html', error = error)


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    app.run(debug=True)
