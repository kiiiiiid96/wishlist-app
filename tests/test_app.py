import pytest
from app import app
from database import init_db, get_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    init_db()
    with app.test_client() as client:
        yield client

def test_index_status_200(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_add_wish(client):
    rv = client.post('/add', data={'name': 'Тест', 'price': '99', 'link': ''}, follow_redirects=True)
    assert rv.status_code == 200
    db = get_db()
    wish = db.execute("SELECT * FROM wishes WHERE name='Тест'").fetchone()
    assert wish is not None

def test_search_filter(client):
    rv = client.get('/search?q=Наушники')
    assert b'Наушники Sony' in rv.data

def test_404_on_nonexistent_id(client):
    rv = client.get('/edit/9999')
    assert rv.status_code == 404

def test_validation_rejects_empty_name(client):
    rv = client.post('/add', data={'name': '', 'price': '10', 'link': ''})
    assert b'Название не может быть пустым' in rv.data
