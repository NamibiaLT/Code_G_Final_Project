

def test_backend(client):
    """Test that the homepage will load"""
    response = client.get('/')
    assert response.status_code == 200
