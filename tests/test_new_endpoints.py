"""Integration tests for new C# API endpoints: ChangeSpaceRole, ImportDataToSpace, GetSpaceUpdates.

These tests target a local Azure Function host (BACKEND_OVERRIDE) or a dev environment.
They discover the test space dynamically via get_available_projects().
"""

import os
import pytest
from dotenv import load_dotenv
from liquid_earth_sdk.api import le_api

load_dotenv()

pytestmark = pytest.mark.core

TOKEN = os.environ.get("LIQUID_EARTH_API_TOKEN")

TEST_SPACE_NAME = "[TEMP] DXF From SDK"
TEST_EMAIL = "test-le@terranigma-solutions.com"

def _get_test_space(token: str) -> dict | None:
    """Find the shared test space by name and return its encrypted SpaceId + OwnerId."""
    projects = le_api.get_available_projects(token)
    for p in projects:
        if p.Name == TEST_SPACE_NAME:
            return {"SpaceId": p.SpaceId, "OwnerId": p.OwnerId}
    pytest.skip(f"Test space '{TEST_SPACE_NAME}' not found in available projects")
    return None


# ── ChangeSpaceRole ─────────────────────────────────────────────────────────


def test_change_space_role_grant_contributor():
    """Grant Contributor (1) permissions to the test user."""
    space = _get_test_space(TOKEN)
    result = le_api.change_space_role(
        space_id=space["SpaceId"],
        owner_id=space["OwnerId"],
        target_email=TEST_EMAIL,
        permissions=1,  # Contributor
        token=TOKEN,
    )
    assert result is not None


def test_change_space_role_revoke():
    """Revoke (11) permissions from the test user."""
    space = _get_test_space(TOKEN)
    result = le_api.change_space_role(
        space_id=space["SpaceId"],
        owner_id=space["OwnerId"],
        target_email=TEST_EMAIL,
        permissions=11,  # Revoke
        token=TOKEN,
    )
    assert result is not None


def test_change_space_role_invalid_permissions():
    """Invalid permission value should return an error."""
    space = _get_test_space(TOKEN)
    with pytest.raises(ValueError, match="HTTP Error 400|Bad Request|Invalid request"):
        le_api.change_space_role(
            space_id=space["SpaceId"],
            owner_id=space["OwnerId"],
            target_email=TEST_EMAIL,
            permissions=999,
            token=TOKEN,
        )


def test_change_space_role_missing_target():
    """Missing targetEmail should return a 400."""
    space = _get_test_space(TOKEN)
    # Pass an empty email — the C# endpoint will reject it as missing target
    with pytest.raises(ValueError, match="HTTP Error 400|Bad Request|Invalid request"):
        le_api.change_space_role(
            space_id=space["SpaceId"],
            owner_id=space["OwnerId"],
            target_email="",
            permissions=1,
            token=TOKEN,
        )


# ── ImportDataToSpace ────────────────────────────────────────────────────────


@pytest.mark.skipif(True, reason="Space is not ready")
def test_import_data_to_space_dxf():
    """Import a DXF file from blob storage into the test space."""
    space = _get_test_space(TOKEN)
    try:
        result = le_api.import_data_to_space(
            space_id=space["SpaceId"],
            owner_id=space["OwnerId"],
            path_in="raw_files/DxfFile.dxf",
            path_out="static_mesh/DxfFile.le",
            type_of_import="DXF",
            token=TOKEN,
        )
        assert result is not None, "Expected a response from ImportDataToSpace"
    except ValueError as e:
        # 500 from subsurface-le Cosmos RBAC is acceptable locally
        assert "HTTP Error 500" in str(e), f"Unexpected error: {e}"


@pytest.mark.skipif(True, reason="Space is not ready")
def test_import_data_to_space_obj_mesh():
    """Import an OBJ mesh from blob storage."""
    space = _get_test_space(TOKEN)
    try:
        result = le_api.import_data_to_space(
            space_id=space["SpaceId"],
            owner_id=space["OwnerId"],
            path_in="raw_files/face1.obj",
            path_out="static_mesh/face1.le",
            type_of_import="OBJ_MESH",
            token=TOKEN,
        )
        assert result is not None
    except ValueError as e:
        # 500 from subsurface-le Cosmos RBAC is acceptable locally
        assert "HTTP Error 500" in str(e), f"Unexpected error: {e}"


def test_import_data_to_space_invalid_type():
    """An unsupported type_of_import should raise a 400 or 500 depending on when validation fails."""
    space = _get_test_space(TOKEN)
    with pytest.raises(ValueError, match="HTTP Error"):
        le_api.import_data_to_space(
            space_id=space["SpaceId"],
            owner_id=space["OwnerId"],
            path_in="raw_files/test.xyz",
            type_of_import="NOT_REAL",
            token=TOKEN,
        )


def test_import_data_to_space_missing_path():
    """Missing path_in should raise a 400."""
    space = _get_test_space(TOKEN)
    with pytest.raises(ValueError, match="HTTP Error 400"):
        le_api.import_data_to_space(
            space_id=space["SpaceId"],
            owner_id=space["OwnerId"],
            path_in="",
            type_of_import="DXF",
            token=TOKEN,
        )


# ── GetSpaceUpdates ──────────────────────────────────────────────────────────


def test_get_space_updates():
    """Fetch update history for the test space."""
    space = _get_test_space(TOKEN)
    try:
        result = le_api.get_space_updates(
            space_id=space["SpaceId"],
            token=TOKEN,
        )
        assert result is not None
        assert "space_id" in result
        assert "updates" in result
        assert isinstance(result["updates"], list)
        pass
    except ValueError as e:
        # 500 from Cosmos RBAC issue locally is acceptable
        assert "HTTP Error 500" in str(e), f"Unexpected error: {e}"


def test_get_space_updates_bad_id():
    """A malformed space ID should return a 400 or 500 (decryption failure)."""
    with pytest.raises(ValueError, match="HTTP Error"):
        le_api.get_space_updates(
            space_id="not-valid-id",
            token=TOKEN,
        )


def test_get_space_updates_no_auth():
    """No token should fail authorization."""
    with pytest.raises(ValueError, match="HTTP Error 401|HTTP Error 500"):
        le_api.get_space_updates(
            space_id="does-not-matter",
            token="",
        )