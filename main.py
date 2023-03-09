from flask import Flask, render_template, url_for
from post import PostMaster



app = Flask(__name__)

@app.route('/')
def new_posts():
    return render_template("index.html", all_posts=pm.quote_list[::-1])


@app.route('/output')
def generate_quote():
    return render_template("post.html", has_value=False, post=pm.quote_list[-1])


@app.route('/roll', methods=['GET'])
def roll_post():
    new_post = pm.add_entry()
    pm.save_info()
    return render_template("post.html", has_value=True, post=new_post), {"Refresh": f"6; url={url_for('generate_quote')}"}

if __name__ == "__main__":
    pm = PostMaster()
    app.run(debug=True)



