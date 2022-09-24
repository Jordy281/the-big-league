from api.models import Partner, DvAccount, CmAccount

# Using u instead of p as thats what the example code uses and Im lazy
u = Partner(partner_name='Dandelion-Test', active=True)


"""
This file (test_partner_model.py) contains the unit tests for the models.py file.
"""
def test_partner(partner):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the partner_name and active fields are defined correctly
    """
    assert partner.partner_name == 'Dandelion-Test'
    assert partner.active == True
    assert partner.dv_accounts == []
    assert partner.cm_accounts == []

def test_partner_with_all_accounts(partner_with_all_accounts, dvAccount, cmAccount):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the partner_name and active fields are defined correctly
    """
    assert partner_with_all_accounts.partner_name == 'Dandelion-Test'
    assert partner_with_all_accounts.active == True
    assert partner_with_all_accounts.dv_accounts == [dvAccount]
    assert partner_with_all_accounts.cm_accounts == [cmAccount]

