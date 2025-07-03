def test_signup(client):
    res = client.post('/auth/signup', json={"email": "test@x.com", "password": "123"})
    assert res.status_code == 201
