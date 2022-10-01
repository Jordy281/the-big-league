def test_get_all_partner(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/partners' page is posted to (POST)
    THEN check the response is correct
    """
    rv = test_client.get('/api/partners')
    #print(rv.json['data'])
    assert rv.status_code == 200
    assert len(rv.json) == 2
    assert rv.json[0]['partner_name'] == 'init-partner1'
    assert rv.json[0]['active'] == True


def test_get_partner(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/partners' page is posted to (POST)
    THEN check the response is correct
    """

    rv = test_client.get('/api/partners/2')
    #print(rv.json['data'])
    assert rv.status_code == 200
    assert rv.json['partner_name'] == 'init-partner2'
    assert rv.json['active'] == False

def test_post_partner_fail(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/partners' page is posted to with an incorrect body (POST)
    THEN check the response is correct
    """

    response = test_client.post('/api/partners', json={})
    assert response.status_code == 400
    assert response.json['errors']['json']['partner_name'][0]=='Missing data for required field.'


def test_post_partner(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/partners' page is posted to (POST)
    THEN check the response is correct
    """

    response = test_client.post('/api/partners', json={
        'partner_name': 'Dandelion-Test'
    })
    assert response.status_code ==201

    rv = test_client.get('/api/partners')
    #print(rv.json['data'])
    assert rv.status_code == 200
    assert len(rv.json) == 3
    assert rv.json[2]['partner_name'] == 'Dandelion-Test'
    assert rv.json[2]['active'] == True

def test_update_partner_fail(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/partners' page is posted to (POST)
    THEN check the response is correct
    """

    # Update a partner that does not exist
    response = test_client.put('/api/partners/4', json={
        'partner_name': 'Dandelion-Test-Fail'
    })
    print(response.json)
    assert response.status_code == 404
    assert response.json['message'] == 'Not Found'

    #Update a partner name to one that already exists
    response = test_client.put('/api/partners/3', json={
        'partner_name': 'init-partner1'
    })
    print(response.json)
    assert response.status_code == 409
    assert response.json['message'] == 'Conflict'

def test_update_partner(test_client, init_database):
    response = test_client.put('/api/partners/3', json={
        'partner_name': 'Dandelion-Test-Update'
    })
    #print(rv.json['data'])
    assert response.status_code == 200
    assert response.json['partner_name'] == 'Dandelion-Test-Update'
    assert response.json['partner_id'] == 3

def test_delete_partner_fail(test_client, init_database):
    # Test an invalid id
    response = test_client.delete('/api/partners/4')
    assert response.status_code == 404
    assert response.json['message'] == 'Not Found'

def test_delete_partner(test_client, init_database):
    # Test an invalid id
    response = test_client.delete('/api/partners/3')
    assert response.status_code == 200

    #Try to get the deleted partner
    response = test_client.get('/api/partners/3')
    assert response.status_code == 404
    assert response.json['message'] == 'Not Found'

    #Verify there are only two records in the database
    response = test_client.get('/api/partners')
    assert response.status_code == 200
    assert len(response.json) == 2




