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

def test_dashboard_page(client):
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert "Faculty Dashboard" in response.get_data(as_text=True)
    assert "Prof. Demo Name" in response.get_data(as_text=True)

def test_form_page_get(client):
    response = client.get('/form')
    assert response.status_code == 200

def test_api_students_get(client):
    response = client.get('/api/students')
    assert response.status_code == 200

def test_form_page_post(client):
    payload = {
        'student_name': 'Aarav Sharma',
        'usn': '1MS22CS001',
        'attendance_percentage': '92',
        'eng_math_3': '88',
        'data_structures': '91',
        'digital_logic': '85',
        'oop_java': '90',
        'discrete_math': '86',
        'dbms': '89',
        'operating_systems': '87',
        'computer_networks': '88',
        'design_analysis_algo': '92',
        'software_engineering': '90'
    }
    response = client.post('/form', data=payload)
    assert response.status_code == 200
