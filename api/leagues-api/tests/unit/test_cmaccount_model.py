"""
This file (test_cmaccount_model.py) contains the unit tests for the models.py file.
"""
def test_cmaccount(cmAccount):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the platform_name and platform_id fields are defined correctly
    """

    assert cmAccount.platform_name == 'CM-Account'
    assert cmAccount.platform_id == 9876

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
    accounts = partner_with_all_accounts.cm_accounts
    exists=False
    for account in accounts:
        if account.platform_name == cmAccount.platform_name and account.platform_id == cmAccount.platform_id:
            exists=True
    assert exists

