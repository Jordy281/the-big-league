# Test
def test_create_rate(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/cmaccounts' page is posted to (POST)
    THEN check the response is correct and the rate is correct
    """
    response = test_client.post('/api/cmaccounts', json={
        'platform_name': 'Dandelion-CM-Test',
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


    #Check The tables for stuff
    response = test_client.get('/api/cmaccounts/3')
    assert response.status_code == 200
    assert response.json['platform_name'] == 'Dandelion-CM-Test'
    assert response.json['platform_id'] == 3
    assert response.json['partner_id'] == 1
    assert response.json['rates'] == [
        {
            "max_usage_rate_threshold": '',
            "max_usage_rate_threshold_unit": '',
            "platform_tech_fee": 3,
            "tier": "Managed",
            "total_media_fee": 3,
            "trueview_pg_direct_tech_fee": 3
        }
    ]


def test_update_account(test_client, init_database):

    # Now lets try updating the rate
    response = test_client.put('/api/cmaccounts/3', json={
        'platform_name': 'Dandelion-CM-Test-Update',
        'platform_id': 3,
        'partner_id': 1,
        'rates': [
            {
                "max_usage_rate_threshold": None,
                "max_usage_rate_threshold_unit": None,
                "platform_tech_fee": 3,
                "tier": "Self-Serve",
                "total_media_fee": 3,
                "trueview_pg_direct_tech_fee": 3
            }
        ]
    })

    assert response.status_code == 200
    assert response.json['platform_name'] == 'Dandelion-CM-Test-Update'
    assert response.json['platform_id'] == 3
    assert response.json['partner_id'] == 1
    assert response.json['rates'] == [{
        "max_usage_rate_threshold": None,
        "max_usage_rate_threshold_unit": None,
        "platform_tech_fee": 3,
        "tier": "Self-Serve",
        "total_media_fee": 3,
        "trueview_pg_direct_tech_fee": 3
    }]
    #Check The tables for stuff
    response = test_client.get('/api/cmaccounts/3')
    assert response.status_code == 200
    assert response.json['platform_name'] == 'Dandelion-CM-Test-Update'
    assert response.json['platform_id'] == 3
    assert response.json['partner_id'] == 1
    assert response.json['rates'] == [
        {
            "max_usage_rate_threshold": '',
            "max_usage_rate_threshold_unit": '',
            "platform_tech_fee": 3,
            "tier": "Self-Serve",
            "total_media_fee": 3,
            "trueview_pg_direct_tech_fee": 3
        }
    ]


def test_update_account_two_rates(test_client, init_database):

    # Now lets try updating the rate
    response = test_client.put('/api/cmaccounts/3', json={
        'platform_name': 'Dandelion-CM-Test-Update',
        'platform_id': 3,
        'partner_id': 1,
        'rates': [
            {
                "max_usage_rate_threshold": None,
                "max_usage_rate_threshold_unit": None,
                "platform_tech_fee": 3,
                "tier": "Self-Serve",
                "total_media_fee": 3,
                "trueview_pg_direct_tech_fee": 3
            },
            {
                "max_usage_rate_threshold": None,
                "max_usage_rate_threshold_unit": None,
                "platform_tech_fee": 4,
                "tier": "Managed",
                "total_media_fee": 4,
                "trueview_pg_direct_tech_fee": 4
            }
        ]
    })
    # Validate Response
    assert response.status_code == 200
    assert response.json['platform_name'] == 'Dandelion-CM-Test-Update'
    assert response.json['platform_id'] == 3
    assert response.json['partner_id'] == 1
    assert response.json['rates'] == [
        {
            "max_usage_rate_threshold": None,
            "max_usage_rate_threshold_unit": None,
            "platform_tech_fee": 3,
            "tier": "Self-Serve",
            "total_media_fee": 3,
            "trueview_pg_direct_tech_fee": 3
        },
        {
            "max_usage_rate_threshold": None,
            "max_usage_rate_threshold_unit": None,
            "platform_tech_fee": 4,
            "tier": "Managed",
            "total_media_fee": 4,
            "trueview_pg_direct_tech_fee": 4
        }
    ]

    #Check The tables for stuff
    response = test_client.get('/api/cmaccounts/3')
    assert response.status_code == 200
    assert response.json['platform_name'] == 'Dandelion-CM-Test-Update'
    assert response.json['platform_id'] == 3
    assert response.json['partner_id'] == 1
    assert response.json['rates'] == [
        {
            "max_usage_rate_threshold": '',
            "max_usage_rate_threshold_unit": '',
            "platform_tech_fee": 3,
            "tier": "Self-Serve",
            "total_media_fee": 3,
            "trueview_pg_direct_tech_fee": 3
        },
        {
            "max_usage_rate_threshold": '',
            "max_usage_rate_threshold_unit": '',
            "platform_tech_fee": 4,
            "tier": "Managed",
            "total_media_fee": 4,
            "trueview_pg_direct_tech_fee": 4
        }
    ]
    



def test_update_account_remove_one_rate(test_client, init_database):

    # Now lets try updating the rate
    response = test_client.put('/api/cmaccounts/3', json={
        'platform_name': 'Dandelion-CM-Test-Update',
        'platform_id': 3,
        'partner_id': 1,
        'rates': [
            {
                "max_usage_rate_threshold": None,
                "max_usage_rate_threshold_unit": None,
                "platform_tech_fee": 3,
                "tier": "Self-Serve",
                "total_media_fee": 3,
                "trueview_pg_direct_tech_fee": 3
            }
        ]
    })

    assert response.status_code == 200
    assert response.json['platform_name'] == 'Dandelion-CM-Test-Update'
    assert response.json['platform_id'] == 3
    assert response.json['partner_id'] == 1
    assert response.json['rates'] == [
        {
            "max_usage_rate_threshold": None,
            "max_usage_rate_threshold_unit": None,
            "platform_tech_fee": 3,
            "tier": "Self-Serve",
            "total_media_fee": 3,
            "trueview_pg_direct_tech_fee": 3
        }
    ]
    #Check The tables for stuff
    response = test_client.get('/api/cmaccounts/3')
    assert response.status_code == 200
    assert response.json['platform_name'] == 'Dandelion-CM-Test-Update'
    assert response.json['platform_id'] == 3
    assert response.json['partner_id'] == 1
    assert response.json['rates'] == [
        {
            "max_usage_rate_threshold": '',
            "max_usage_rate_threshold_unit": '',
            "platform_tech_fee": 3,
            "tier": "Self-Serve",
            "total_media_fee": 3,
            "trueview_pg_direct_tech_fee": 3
        }
    ]

def test_delete_account(test_client, init_database):
    # Test an invalid id
    response = test_client.delete('/api/cmaccounts/3')
    assert response.status_code == 200

    #Try to get the deleted account
    response = test_client.get('/api/cmaccounts/3')
    assert response.status_code == 404
    assert response.json['message'] == 'Not Found'

    # Lets test the database directly to look for the specified rate

