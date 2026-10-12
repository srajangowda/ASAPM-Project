import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_form_page_get(client):
    response = client.get('/form')
    assert response.status_code == 200

def test_form_page_post(client):
    payload = {
        'gender': 'female',
        'ethnicity': 'group B',
        'parental_level_of_education': "bachelor's degree",
        'lunch': 'standard',
        'test_preparation_course': 'none',
        'reading_score': '75',
        'writing_score': '78'
    }
    response = client.post('/form', data=payload)
    assert response.status_code == 200

