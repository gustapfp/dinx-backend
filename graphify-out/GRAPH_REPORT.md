# Graph Report - back  (2026-05-03)

## Corpus Check
- 30 files · ~2,296 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 116 nodes · 160 edges · 14 communities detected
- Extraction: 64% EXTRACTED · 36% INFERRED · 0% AMBIGUOUS · INFERRED: 57 edges (avg confidence: 0.57)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]

## God Nodes (most connected - your core abstractions)
1. `AuthService` - 12 edges
2. `Users` - 10 edges
3. `RefreshToken` - 10 edges
4. `TokenHelper` - 10 edges
5. `DinxBaseModel` - 9 edges
6. `Create a new user account.          Args:             body (UserCreate): Registr` - 8 edges
7. `Validate credentials and return an access + refresh token pair.          Args:` - 8 edges
8. `Issue a new access token from a valid refresh token.          Args:` - 8 edges
9. `Revoke a refresh token, preventing it from issuing new access tokens.          A` - 8 edges
10. `TokenPair` - 8 edges

## Surprising Connections (you probably didn't know these)
- `AuthService` --uses--> `TokenHelper`  [INFERRED]
  src/app/auth/services.py → src/app/auth/utils/helper.py
- `Create a new user account.          Args:             body (UserCreate): Registr` --uses--> `TokenHelper`  [INFERRED]
  src/app/auth/services.py → src/app/auth/utils/helper.py
- `Validate credentials and return an access + refresh token pair.          Args:` --uses--> `TokenHelper`  [INFERRED]
  src/app/auth/services.py → src/app/auth/utils/helper.py
- `Issue a new access token from a valid refresh token.          Args:` --uses--> `TokenHelper`  [INFERRED]
  src/app/auth/services.py → src/app/auth/utils/helper.py
- `Revoke a refresh token, preventing it from issuing new access tokens.          A` --uses--> `TokenHelper`  [INFERRED]
  src/app/auth/services.py → src/app/auth/utils/helper.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.26
Nodes (13): PasswordHelper, Hash a password using bcrypt.          Args:             password (str): The pas, Verify a password against a bcrypt hash.          Args:             password (st, RefreshToken, Users, TokenPair, UserCreate, UserResponse (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (6): After logout the refresh token must no longer work., A refresh token must not grant access to protected endpoints., An access token must not be accepted on the refresh endpoint., test_logout_revokes_refresh_token(), test_me_with_refresh_token_rejected(), test_refresh_with_access_token_rejected()

### Community 2 - "Community 2"
Cohesion: 0.25
Nodes (9): DinxBaseModel, Enum, Budget, BudgetCategory, BudgetCategoryHistory, DinxBaseModel, Transaction, TransactionType (+1 more)

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (5): BaseModel, refresh(), BudgetHistorySchema, Token, TokenData

### Community 4 - "Community 4"
Cohesion: 0.22
Nodes (4): get_current_user(), Create a long-lived refresh token.          Args:             data (dict): The d, Decode and validate a JWT token (access or refresh).          Args:, TokenHelper

### Community 5 - "Community 5"
Cohesion: 0.22
Nodes (8): client(), engine(), Create a fresh file-based SQLite database for each test.      File-based SQLite, Provide an AsyncClient whose requests use the test database.      Each request g, Register a user and return the response body., Log in and return the token pair., registered_user(), tokens()

### Community 6 - "Community 6"
Cohesion: 0.4
Nodes (2): create_db_and_tables(), lifespan()

### Community 7 - "Community 7"
Cohesion: 0.5
Nodes (3): Create a short-lived access token.          Args:             data (dict): The d, UserRole, str

### Community 8 - "Community 8"
Cohesion: 0.5
Nodes (2): BaseSettings, Settings

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Hash a password using bcrypt.          Args:             password (str): The pas

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Verify a password against a bcrypt hash.          Args:             password (st

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Create a short-lived access token.          Args:             data (dict): The d

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Create a long-lived refresh token.          Args:             data (dict): The d

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Decode and validate a JWT token (access or refresh).          Args:

## Knowledge Gaps
- **17 isolated node(s):** `Hash a password using bcrypt.          Args:             password (str): The pas`, `Verify a password against a bcrypt hash.          Args:             password (st`, `Create a short-lived access token.          Args:             data (dict): The d`, `Create a long-lived refresh token.          Args:             data (dict): The d`, `Decode and validate a JWT token (access or refresh).          Args:` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 6`** (5 nodes): `create_db_and_tables()`, `get_session()`, `lifespan()`, `db.py`, `lifespan.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (4 nodes): `BaseSettings`, `database_url()`, `Settings`, `settings.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `Hash a password using bcrypt.          Args:             password (str): The pas`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Verify a password against a bcrypt hash.          Args:             password (st`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Create a short-lived access token.          Args:             data (dict): The d`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Create a long-lived refresh token.          Args:             data (dict): The d`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Decode and validate a JWT token (access or refresh).          Args:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AuthService` connect `Community 0` to `Community 2`, `Community 4`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `DinxBaseModel` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `AuthService` (e.g. with `RefreshToken` and `Users`) actually correct?**
  _`AuthService` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Users` (e.g. with `AuthService` and `Create a new user account.          Args:             body (UserCreate): Registr`) actually correct?**
  _`Users` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `RefreshToken` (e.g. with `AuthService` and `Create a new user account.          Args:             body (UserCreate): Registr`) actually correct?**
  _`RefreshToken` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `TokenHelper` (e.g. with `AuthService` and `Create a new user account.          Args:             body (UserCreate): Registr`) actually correct?**
  _`TokenHelper` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `DinxBaseModel` (e.g. with `Users` and `RefreshToken`) actually correct?**
  _`DinxBaseModel` has 7 INFERRED edges - model-reasoned connections that need verification._