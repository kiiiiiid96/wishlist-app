cat > app.py << 'EOF'
from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_db
from validators import validate_wish

app = Flask(__name__)

@app.route('/')
def index():
    sort_by = request.args.get('sort', 'id')
    if sort_by not in ['price', 'status', 'name']:
        sort_by = 'id'
    db = get_db()
    wishes = db.execute(f'SELECT * FROM wishes ORDER BY {sort_by}').fetchall()
    total = db.execute('SELECT SUM(price) FROM wishes WHERE status != "completed"').fetchone()[0] or 0
    return render_template('index.html', wishes=wishes, total=total, sort_by=sort_by)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        link = request.form['link']
        error = validate_wish(name, price)
        if error:
            return render_template('add.html', error=error)
        db = get_db()
        db.execute('INSERT INTO wishes (name, price, link, status) VALUES (?, ?, ?, ?)',
                   (name, float(price), link, 'pending'))
        db.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    db = get_db()
    wish = db.execute('SELECT * FROM wishes WHERE id = ?', (id,)).fetchone()
    if not wish:
        return render_template('404.html'), 404
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        link = request.form['link']
        error = validate_wish(name, price)
        if error:
            return render_template('edit.html', wish=wish, error=error)
        db.execute('UPDATE wishes SET name=?, price=?, link=? WHERE id=?',
                   (name, float(price), link, id))
        db.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', wish=wish)

@app.route('/delete/<int:id>')
def delete(id):
    db = get_db()
    db.execute('DELETE FROM wishes WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:id>')
def toggle(id):
    db = get_db()
    current = db.execute('SELECT status FROM wishes WHERE id = ?', (id,)).fetchone()
    new_status = 'completed' if current['status'] == 'pending' else 'pending'
    db.execute('UPDATE wishes SET status = ? WHERE id = ?', (new_status, id))
    db.commit()
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    db = get_db()
    wishes = db.execute('SELECT * FROM wishes WHERE name LIKE ?', (f'%{query}%',)).fetchall()
    total = sum(w['price'] for w in wishes if w['status'] != 'completed')
    return render_template('index.html', wishes=wishes, total=total, sort_by='id', search_query=query)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
EOF
