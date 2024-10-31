from liquid_earth_api.modules.rest_client.rest_interface import get_dev_tokens, generate_dev_token, revoke_dev_token


def test_get_user_dev_tokens():
    val = get_dev_tokens(
        user_id="7c775179-437b-4269-8cf7-8e6a419f1b00",
        login_token="unused_in_local_dev"
    )
    print(val)
    
    
def test_generate_dev_token():
    val = generate_dev_token(
        user_id="7c775179-437b-4269-8cf7-8e6a419f1b00",
        token_name="test_token",
        login_token="unused_in_local_dev"
    )
    print(val)


def test_revoke_dev_token():
    val = revoke_dev_token(
        user_id="7c775179-437b-4269-8cf7-8e6a419f1b00",
        token_id="le-8b4c9d33528a4e7492583871f6545ea4IAmNqhThFXeIKMQTzummp0Zdyhejwnqh1iSteK1A55I",
        login_token="unused_in_local_dev"
    )
    print(val)
