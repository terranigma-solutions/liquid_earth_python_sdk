from liquid_earth_api.data.schemas import PostData
from gempy.core.data.enumerators import ExampleModel
from liquid_earth_api import push_data_to_le_space, get_available_projects, get_deep_link
import gempy as gp

# * Add here a valid token. This is just valid for an hour
user_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlhaaFI1cmJ6alVlZ2hmckI3bEtxNnhDamNfZG1CUlVfWTdyNUx3RlVoeGsiLCJ0eXAiOiJKV1QifQ.eyJ2ZXIiOiIxLjAiLCJpc3MiOiJodHRwczovL3RlcnJhbmlnbWEuYjJjbG9naW4uY29tLzQxMTllZGYxLTFhOWQtNDg1NC1iNTg5LWZkYjU5NGMzMzgxMi92Mi4wLyIsInN1YiI6IjQzNzczYjcyLWZlYWUtNDk1ZC1hMWQ5LWU1MjlkYzY0ZGE5ZiIsImF1ZCI6IjY4NWUwOGMwLTBhYWMtNDJmNi04MGE5LWM1NzQ0MGNkMjk2MiIsImV4cCI6MTY5NDc2NjczMSwiYWNyIjoiYjJjXzFhX3JvcGNfYXV0aF9saWNlbnNlX2NsYWltcyIsImlhdCI6MTY5NDc2MzEzMSwiYXV0aF90aW1lIjoxNjk0NzYzMTMxLCJleHRlbnNpb25fbGljZW5zZSI6InN1cGVyIiwiZXh0ZW5zaW9uX2xpY2Vuc2VfZXhwIjoiMjAzMS0wMS0yOFQwODozODoyNVoiLCJzaWduSW5OYW1lcy5lbWFpbEFkZHJlc3MiOiJtaWd1ZWxAdGVycmFuaWdtYS1zb2x1dGlvbnMuY29tIiwibmFtZSI6Ik1pZ3VlbCBkZSBsYSBWYXJnYSIsImdpdmVuX25hbWUiOiJNaWd1ZWwiLCJmYW1pbHlfbmFtZSI6ImRlIGxhIFZhcmdhIiwiYXRfaGFzaCI6Ii1VcThzblA2amI0dmhmLTI2WnlSS0EiLCJuYmYiOjE2OTQ3NjMxMzF9.CD03JhAHfMpwCyN9U8XQ3qEwKnhZQMyNPUKeI01D4QL9lDzOOJXEJWhjPeBwJjlX1abpcs0kDV5XBWN6oYSDmAQ26op8Y0UNqyklk-Q9pXQ515O7PZRNiY_EC-PWeQuVUtCtYp6YT6bnD-r3FX0SJwMH-8-vhrXFJYNB4NkgSZtk4f7SIjpo-KSsSSI0_YsWez0swHp0bE0_w5Ye410EldlJr2GiUe2qHQpP_f8YIjehDPZvvETlwwIhYPBMmeSp6-pBwSlHuOY-m69BAzFr0SuYpGRw1PiCIg-OXlJ8b3Nqverk8e4g3oDvmPjxLEE8qK7uqnLznPiLg0_kz2JqkA"


def test_get_available_projects():
    available_projects = get_available_projects(
        token=user_token
    )
    return available_projects


def test_get_deeplink():
    clashach_project: PostData = _get_clashach_project()
    deep_link = get_deep_link(clashach_project, token=user_token)
    print(deep_link)


def test_upload_data_to_space():
    # * Getting available projects

    post_data = _get_clashach_project()

    model = gp.generate_example_model(ExampleModel.ANTICLINE, compute_model=True)
    foo = push_data_to_le_space(model, post_data=post_data, token=user_token)


def _get_clashach_project() -> PostData:
    all_projects = test_get_available_projects()
    # Look for the item that the ["name"] == "Clashach"
    for project in all_projects:
        if project["name"] == "Clashach":
            clashach_project = project
    if clashach_project is None:
        raise ValueError("Clashach project not found")
    post_data = PostData(
        spaceId=clashach_project["spaceId"],
        ownerId=clashach_project["ownerId"],
        dataType="static_mesh",
        fileName="test"
    )
    return post_data
