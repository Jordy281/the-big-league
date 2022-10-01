"""
This file (test_dvaccount_model.py) contains the unit tests for the models.py file.
"""
def test_dvaccount(dvAccount):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the platform_name and platform_id fields are defined correctly
    """

    assert dvAccount.platform_name == 'DV-Account'
    assert dvAccount.platform_id == 1234

def test_partner_with_all_accounts(partner_with_all_accounts, dvAccount, cmAccount):
    """
    GIVEN a User model
    WHEN a new User is created with DV accounts
    THEN check the partner_name and active fields are defined correctly
    THEN check if the DV account in partner matches the one passed in
    """
    assert partner_with_all_accounts.partner_name == 'Dandelion-Test'
    assert partner_with_all_accounts.active == True
    assert partner_with_all_accounts.dv_accounts == [dvAccount]
    assert partner_with_all_accounts.cm_accounts == [cmAccount]
    accounts = partner_with_all_accounts.dv_accounts
    exists=False
    for account in accounts:
        if account.platform_name == dvAccount.platform_name and account.platform_id == dvAccount.platform_id:
            exists=True
    
    assert exists

