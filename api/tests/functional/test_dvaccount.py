def test_get_all_account(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/dvaccounts' page is posted to (POST)
    THEN check the response is correct
    """
    rv = test_client.get('/api/dvaccounts')
    #print(rv.json['data'])
    assert rv.status_code == 200
    assert len(rv.json) == 2
    account = rv.json[0]
    assert account['platform_name'] == 'init-dvAccount1'
    assert account['platform_id'] == 1
    account = rv.json[1]
    assert account['platform_name'] == 'init-dvAccount2'
    assert account['platform_id'] == 2

def test_get_account(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/dvaccounts' page is posted to (POST)
    THEN check the response is correct
    """

    response = test_client.get('/api/dvaccounts/2')
    #print(rv.json['data'])
    assert response.status_code == 200
    account = response.json
    assert account['platform_name'] == 'init-dvAccount2'
    assert account['platform_id'] == 2
    assert account['rates'] == [{'max_usage_rate_threshold': '', 'max_usage_rate_threshold_unit': '', 'platform_tech_fee': 2, 'tier': 'Managed', 'total_media_fee': 2, 'trueview_pg_direct_tech_fee': 2}]

def test_post_account_fail(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/dvaccounts' page is posted to with an incorrect body (POST)
    THEN check the response is correct
    """
    # Empty Post
    response = test_client.post('/api/dvaccounts', json={})
    assert response.status_code == 400
    assert response.json['errors']['json']['platform_name'][0]=='Missing data for required field.'

    # Missing Platform ID
    response = test_client.post('/api/dvaccounts', json={
        'platform_name': 'Dandelion-DV-Test'
    })

    assert response.status_code == 400
    assert response.json['errors']['json']['platform_id'][0]=='Missing data for required field.'

    # Missing Platform Name
    response = test_client.post('/api/dvaccounts', json={
        'platform_id': '3'
    })

    assert response.status_code == 400
    assert response.json['errors']['json']['platform_name'][0]=='Missing data for required field.'

def test_post_account(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/dvaccounts' page is posted to (POST)
    THEN check the response is correct
    """

    response = test_client.post('/api/dvaccounts', json={
        'platform_name': 'Dandelion-DV-Test',
        'platform_id': 3,
        'partner_id': 1,
        'rates': [
            {
                "max_usage_rate_threshold": None,
                "max_usage_rate_threshold_unit": None,
                "platform_tech_fee": 3,
                "tier": "Managed",
                "total_media_fee": 3,
                "trueview_pg_direct_tech_fee": 3
            }
        ]
    })
    print(response.text)
    assert response.status_code ==201

    response = test_client.get('/api/dvaccounts')
    #print(rv.json['data'])
    assert response.status_code == 200
    assert len(response.json) == 3
    assert response.json[2]['platform_name'] == 'Dandelion-DV-Test'
    assert response.json[2]['platform_id'] == 3

    # Ensure that the post actually updated the partner too
    response = test_client.get('/api/partners/1')
    print(response.text)
    partner = response.json
    account_exists = False
    for account in partner['dv_accounts']:
        if account['platform_id']==3 and account['platform_name'] == 'Dandelion-DV-Test':
            account_exists = True
    assert account_exists

def test_update_account_fail(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/dvaccounts' page is posted to (POST)
    THEN check the response is correct
    """

    # Update a account that does not exist
    response = test_client.put('/api/dvaccounts/4', json={
        'platform_name': 'Dandelion-DV-Test-Fail',
        'platform_id': 3,
        'partner_id': 1
    })
    print(response.json)
    assert response.status_code == 404
    assert response.json['message'] == 'Not Found'
    """
    I would have to double check but I think accounts are allowed to have the same name in DV360

    #Update a account name to one that already exists
    response = test_client.put('/api/dvaccounts/3', json={
        'platform_name': 'init-dvaccount1',
        'platform_id': 3,
        'partner_id': 1
    })
    print(response.json)
    assert response.status_code == 409
    assert response.json['message'] == 'Conflict'
    """

def test_update_account(test_client, init_database):
    response = test_client.put('/api/dvaccounts/3', json={
        'platform_name': 'Dandelion-DV-Test-Update',
        'platform_id': 3,
        'partner_id': 1
    })
    #print(rv.json['data'])
    assert response.status_code == 200
    assert response.json['platform_name'] == 'Dandelion-DV-Test-Update'
    assert response.json['platform_id'] == 3
    assert response.json['partner_id'] == 1

    response = test_client.get('/api/dvaccounts/3')
    assert response.status_code == 200
    assert response.json['platform_name'] == 'Dandelion-DV-Test-Update'
    assert response.json['platform_id'] == 3
    assert response.json['partner_id'] == 1

def test_delete_account_fail(test_client, init_database):
    # Test an invalid id
    response = test_client.delete('/api/dvaccounts/4')
    assert response.status_code == 404
    assert response.json['message'] == 'Not Found'

def test_delete_account(test_client, init_database):
    # Test an invalid id
    response = test_client.delete('/api/dvaccounts/3')
    assert response.status_code == 200

    #Try to get the deleted account
    response = test_client.get('/api/dvaccounts/3')
    assert response.status_code == 404
    assert response.json['message'] == 'Not Found'

    #Verify there are only two records in the database
    response = test_client.get('/api/dvaccounts')
    assert response.status_code == 200
    assert len(response.json) == 2


def test_post_account_from_partner(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/partners' page is posted to with a nested dv account(POST)
    THEN check the response is correct
    """

    response = test_client.post('/api/partners', json={
        'partner_name': 'Dandelion-Test',
        'dv_accounts':[
            {
                'platform_name': 'Dandelion-DV-Test',
                'platform_id': 3,
                'partner_id': 1,
                'rates': [
                    {
                        "max_usage_rate_threshold": None,
                        "max_usage_rate_threshold_unit": None,
                        "platform_tech_fee": 3,
                        "tier": "Managed",
                        "total_media_fee": 3,
                        "trueview_pg_direct_tech_fee": 3
                    }
                ]
            }
        ]
    })
    print(response.text)
    assert response.status_code ==201

    response = test_client.get('/api/dvaccounts')
    #print(rv.json['data'])
    assert response.status_code == 200
    assert len(response.json) == 3
    assert response.json[2]['platform_name'] == 'Dandelion-DV-Test'
    assert response.json[2]['platform_id'] == 3

    # Ensure that the post actually updated the partner too
    response = test_client.get('/api/partners/3')
    print(response.text)
    partner = response.json
    account_exists = False
    for account in partner['dv_accounts']:
        if account['platform_id']==3 and account['platform_name'] == 'Dandelion-DV-Test':
            account_exists = True
            account['rates'] == [
                    {
                        "max_usage_rate_threshold": "",
                        "max_usage_rate_threshold_unit": "",
                        "platform_tech_fee": 3,
                        "tier": "Managed",
                        "total_media_fee": 3,
                        "trueview_pg_direct_tech_fee": 3
                    }
                ]

    assert account_exists

def test_delete_account_from_partner(test_client,init_database):
    # Test an invalid id
    response = test_client.delete('/api/partners/3')
    assert response.status_code == 200

    #Try to get the deleted partner
    response = test_client.get('/api/partners/3')
    assert response.status_code == 404
    assert response.json['message'] == 'Not Found'

    #Try to get the deleted partner
    response = test_client.get('/api/dvaccounts/3')
    assert response.status_code == 404
    assert response.json['message'] == 'Not Found'

    #Verify there are only two records in the database
    response = test_client.get('/api/dvaccounts')
    assert response.status_code == 200
    assert len(response.json) == 2
