from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# --- Configuration ---
# Configure SQLite database URI (creates 'blog.db' file in the project folder)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# Silence the deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# --- Database Model (Post) ---
class Post(db.Model):
    """Database model for a single blog post."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # Slug is used for clean URLs (e.g., /post/my-first-post)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# Utility function to create a simple slug
def create_slug(title):
    return title.lower().strip().replace(' ', '-').replace('.', '')

# --- Routes ---

# Home Page Route (/) - Display all posts
@app.route('/')
def index():
    """Fetches all posts and displays them on the homepage."""
    # Query the database to get all posts, ordered by newest first
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    # Jinja2 Templating: passes the 'posts' list to the index.html template
    return render_template('index.html', posts=posts)

# Single Post Viewer Route (/post/<slug>)
@app.route('/post/<string:slug>')
def view_post(slug):
    """Displays the full content of a single blog post."""
    # Query the database to find the post by its unique slug
    post = Post.query.filter_by(slug=slug).first_or_404()
    # If found, Jinja2 Templating: passes the single 'post' object to the template
    return render_template('post.html', post=post)

# Post Creation Routes (/create)
@app.route('/create', methods=['GET', 'POST'])
def create_post():
    """Handles displaying the form (GET) and submitting data (POST)."""
    if request.method == 'POST':
        # 1. Get data from form (Form Handling)
        title = request.form.get('title')
        content = request.form.get('content')
        
        # Simple backend validation
        if not title or not content:
            # Re-render the page with an error message in a real app
            # For this simple project, we rely mainly on frontend validation
            return redirect(url_for('create_post'))

        # 2. Process data and save to DB
        post_slug = create_slug(title)
        
        # Create a new Post object
        new_post = Post(title=title, content=content, slug=post_slug)
        
        # Add to session and commit to the database
        try:
            db.session.add(new_post)
            db.session.commit()
            # Redirect to the home page after successful submission
            return redirect(url_for('index'))
        except Exception as e:
            # Handle potential errors (e.g., duplicate slug)
            db.session.rollback()
            print(f"Error saving post: {e}")
            return "An error occurred while saving the post.", 500

    # GET request: render the create post form
    return render_template('create.html')

# This block runs the application when the script is executed
if __name__ == '__main__':
    # Context required for SQLAlchemy to create the database file
    with app.app_context():
        # Creates the database file and tables if they don't exist
        db.create_all()
    app.run(debug=True)