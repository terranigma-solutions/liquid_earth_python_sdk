# AGENTS.md — Liquid Earth Python SDK

## Quick Start

```bash
# Install with dev dependencies
pip install -r requirements/requirements_dev.txt

# Run tests (most integration tests are skipped by default — see "Testing" below)
python -m pytest

# Run with TeamCity output (CI only)
python -m pytest --teamcity -v
```

## Project Purpose

Python SDK that uploads 3D subsurface meshes (from GemPy, subsurface OBJ/GLTF/DXF/MX formats) to the Liquid Earth web platform via REST API + Azure Blob Storage. Author: Miguel de la Varga (miguel@terranigma-solutions.com). License: EUPL v1.2.

## Directory Layout

```
liquid_earth_sdk/            # SDK package
├── __init__.py              # Public API: exports 4 functions
├── config.py                # BASE_URL resolution (APIM vs local override)
│
├── api/
│   ├── le_api.py            # High-level API: upload, get projects, delete, set_token
│   └── _utils_api.py        # Helper: find_space_item by Name
│
├── core/
│   ├── output.py            # Models: AvailableProject (Pydantic), ServerResponse (dataclass)
│   └── data/
│       ├── schemas.py       # Dataclasses for API request payloads
│       └── le_data_types.py # Enum: DataTypes
│
└── modules/
    ├── rest_client/
    │   ├── rest_interface.py # Low-level REST: all API endpoints
    │   ├── _utils.py         # handle_response() helper
    │   └── _links.py         # Dead code — NOT imported anywhere
    │
    ├── blob_client/
    │   └── blob_interface.py # Pushes subsurface data to Azure Blob Storage
    │
    └── data_converter/
        └── converter_interface.py  # GemPy GeoModel → subsurface.UnstructuredData

tests/
├── conftest.py              # Empty
├── pytest.ini               # Defines markers: core, gempy
├── test_le_api_test_cases.py     # Core API: get/delete projects, get_deep_link
├── test_le_api_gempy_test.py     # GemPy synthetic upload test
├── test_token_api.py             # Token lifecycle: login → generate → verify → revoke
├── test_mcp.py                   # MCP-related test (new)
└── test_subsurface/              # OBJ/GLTF/DXF file-format upload tests (all skipped by default)
```

## Architecture & Data Flow

```
User code
   │
   ▼
le_api.upload_mesh_to_existing_space() / _new_space()
   │
   ├── rest_interface.get_available_projects()      → find/create space
   ├── rest_interface.post_add_data_to_space()      → get SAS tokens
   ├── blob_interface.push_unstructured_data()       → upload binary to Azure Blob
   └── rest_interface.get_deep_link()                → return deep link
```

## Essential Commands

| Action | Command | Notes |
|---|---|---|
| Install | `pip install -r requirements/requirements_dev.txt` | Includes all deps |
| Run tests | `python -m pytest` | Many tests skipped by default |
| Run with CI output | `python -m pytest --teamcity -v` | TeamCity CI only |
| Run specific marker | `python -m pytest -m core` | Only core tests |
| Build dist | `python -m build` | Disabled in CI |
| Publish to PyPI | `twine upload dist/*` | Disabled in CI |
| Version | Auto from git tags via `setuptools_scm` | No manual version bumps |

## CRITICAL GOTCHAS

### 1. Token Name Mismatch (`set_token` vs config)

`set_token()` in `le_api.py` writes `LIQUID_EARTH_TOKEN` to `.env`, but `config.py` does not read it. Tests use `LIQUID_EARTH_API_TOKEN`. These are **two separate env var names**. The SDK does NOT automatically detect the token from `.env` — callers must pass `token` explicitly.

If working with tests, set `LIQUID_EARTH_API_TOKEN` in `.env`. If using `set_token()`, the test env var will NOT be written.

### 2. Test Dict Access Bug

`TestLEApiBase._get_test_project()` at line 27-28 accesses `found_project["SpaceId"]` and `["OwnerId"]` as if it's a dict, but `_utils_api.find_space_item()` returns an `AvailableProject` Pydantic model (not a dict). This will raise `TypeError: 'AvailableProject' object is not subscriptable` at runtime. The correct syntax would be `found_project.SpaceId`.

The test method at line 53-56 does it correctly with attribute access. This is an inconsistency within the same file.

### 3. `_links.py` is Dead Code

`modules/rest_client/_links.py` contains an alternative `get_deep_link()` that prints "Error" instead of raising. It is never imported anywhere. Do not use it.

### 4. `localhost` Override Transforms in `config.py`

If `BACKEND_OVERRIDE` contains "localhost", it gets replaced with `<hostname>.local:<port>/api`. This is for macOS `.local` mDNS resolution. If this behavior is unwanted, use a different hostname in `BACKEND_OVERRIDE`.

### 5. Version Lookup Bug in `__init__.py`

`__init__.py` calls `version("subsurface")` where it should call `version("liquid_earth_sdk")`. This will likely fail `PackageNotFoundError` and fall back to `'unknown-YYYYMMDD'`.

### 6. Texture Extension is Hardcoded

In `_upload_mesh_common()` at `le_api.py:100`, `texture_ext` is always `"png"` regardless of the actual texture format.

### 7. Most Tests are Skipped by Default

Integration tests that upload actual file formats (OBJ, GLTF, DXF, MX) are skipped unless environment variable `ONLY_EXPLICIT` is set to something other than `true`. They also require test data from `TERRA_PATH_DEVOPS`.

## Testing Patterns

- **Class-based hierarchy**: `TestLEApiBase` (marker: `core`) → `TestLEApiWithGempy` (marker: `gempy`)
- **Setup via classmethod**: `setup_class()` loads token from env, sets up space name
- **Token from env**: Tests read `LIQUID_EARTH_API_TOKEN` from the environment
- **Heavy use of `@pytest.mark.skip` / `@pytest.mark.skipif`**: Most real upload tests are disabled by default
- **pytest markers defined in** `tests/pytest.ini`: `core`, `gempy`
- **conftest.py is empty** — no shared fixtures

## Code Conventions

| Aspect | Convention |
|---|---|
| Naming | `snake_case` for functions/vars, `PascalCase` for classes |
| Private helpers | Prefixed with `_` (e.g., `_upload_mesh_common`) |
| Request models | `@dataclass` classes in `core/data/schemas.py` |
| Response models | `pydantic.BaseModel` (`AvailableProject`) or simple `@dataclass` (`ServerResponse`) |
| Enums | `enum.Enum` in `core/data/le_data_types.py` |
| Imports | Relative imports within SDK (`from ..core.output import ...`) |
| Type hints | Used throughout but sometimes incomplete (e.g., `dict[str]` without value type) |
| Error handling | Functions raise on failure or return `ServerResponse` with link=None; no custom exceptions |

## CI Pipeline (TeamCity)

- **Trigger**: Non-draft PRs and default branch pushes (excluding `.teamcity/**` changes)
- **Testing Build**: Installs `requirements_dev.txt`, runs `python -m pytest --teamcity -v`
- **Release Build**: (disabled VCS trigger) Depends on Testing passing, then tags, builds, publishes (all disabled steps)
- **Config in**: `.teamcity/` directory (Kotlin DSL + XML patches)