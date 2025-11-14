# StackMason CloudFormation Backend

FastAPI backend with GraphQL API for AWS CloudFormation resources, properties, and regions.

## Features

- **GraphQL API** powered by Strawberry
- **FastAPI** for high performance and modern Python async support
- **PostgreSQL** database with SQLModel ORM
- Complete CloudFormation resource schema with nested properties
- Region-based resource filtering
- Full-text resource search

## Technology Stack

- **FastAPI** - Modern web framework
- **Strawberry GraphQL** - GraphQL library for Python
- **SQLModel** - ORM combining SQLAlchemy and Pydantic for database operations
- **PostgreSQL** - Relational database
- **Uvicorn** - ASGI server

## Setup

### Prerequisites

- Python 3.9+
- PostgreSQL database
- pip or poetry for package management

### Installation

1. Clone the repository (or navigate to the project directory)

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your database:
   - Create a PostgreSQL database
   - Run the schema SQL file to create tables

4. Configure environment variables:
   Create a `.env` file in the project root:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   APP_ENV=local
   ```
   
   **Environment Options:**
   - `local` - Enables GraphQL Playground (default)
   - `production` or `staging` - Disables GraphQL Playground for security

### Running the Server

```bash
# Development mode with auto-reload (recommended)
python run.py

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

## API Endpoints

- **GraphQL Endpoint**: `http://localhost:8000/graphql`
- **GraphQL Playground**: `http://localhost:8000/graphql` (only when `APP_ENV=local`)
- **Health Check**: `http://localhost:8000/health`
- **Root**: `http://localhost:8000/`

**Note:** The GraphQL Playground (GraphiQL) is only enabled when `APP_ENV=local`. Set `APP_ENV=production` to disable it in production for security.

## GraphQL Queries

### Get All Regions

```graphql
query GetRegions {
  regions {
    id
    regionCode
    regionName
  }
}
```

### Get Resources by Region

```graphql
query GetResourcesByRegion($regionId: Int!) {
  resourcesByRegion(regionId: $regionId) {
    id
    resourceType
    documentationUrl
  }
}
```

### Get Complete Resource Details

This is the main query for the frontend to render complete resource information:

```graphql
query GetResourceDetail($resourceId: Int!) {
  resourceDetail(resourceId: $resourceId) {
    id
    resourceType
    documentationUrl
    availableRegions {
      id
      regionCode
      regionName
    }
    properties {
      id
      propertyName
      documentationUrl
      updateType
      isRequired
      isList
      isMap
      primitiveType
      complexTypeId
      complexTypeName
      listAllowsDuplicates
      nestedProperties {
        id
        propertyName
        documentationUrl
        updateType
        isRequired
        isList
        isMap
        primitiveType
        complexTypeId
        complexTypeName
        listAllowsDuplicates
        nestedProperties {
          # Can nest further if needed
          id
          propertyName
          primitiveType
          complexTypeName
          isRequired
          isList
          isMap
        }
      }
    }
    attributes {
      id
      attributeName
      primitiveType
      isList
      listItemType
    }
  }
}
```

### Search Resources

```graphql
query SearchResources($query: String!, $regionId: Int) {
  searchResources(query: $query, regionId: $regionId) {
    id
    resourceType
    documentationUrl
  }
}
```

## User Journey

The API is designed to support the following frontend user journey:

1. **Select Region**
   - Query: `regions` → Display list of AWS regions
   - User selects a region

2. **View Resources for Region**
   - Query: `resourcesByRegion(regionId: X)` → Display available resources
   - User selects a resource

3. **View Complete Resource Details**
   - Query: `resourceDetail(resourceId: Y)` → Display full resource information
   - Frontend renders:
     - Resource type and documentation
     - All properties with their types, requirements, and nested structures
     - All return attributes (Fn::GetAtt)
     - Available regions for this resource

## Data Model

### Resource Structure

The `resourceDetail` query returns a comprehensive resource object:

- **Basic Info**: ID, type, documentation URL
- **Properties**: Hierarchical structure with:
  - Property name and documentation
  - Type information (primitive or complex)
  - Constraints (required, list, map)
  - Update behavior (Mutable/Immutable/Conditional)
  - Nested properties (for complex types)
- **Attributes**: Return values accessible via Fn::GetAtt
- **Regions**: Where this resource is available

### Property Types

Properties can be:
- **Primitive**: String, Integer, Boolean, Double, Long, Json
- **Complex**: References to PropertyTypes with nested properties
- **Lists**: Arrays of primitives or complex types
- **Maps**: Key-value pairs

## Development

### Project Structure

```
stackmason-backend/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── config.py                 # Centralized settings and configuration
│   ├── database.py               # Database connection and session management
│   ├── models/                   # SQLModel ORM models (modularized)
│   │   ├── __init__.py
│   │   ├── region.py             # Region model
│   │   ├── resource.py           # Resource, ResourceRegion, ResourceAttribute models
│   │   └── property.py           # Property, PropertyType models
│   └── graphql/                  # GraphQL layer (modularized)
│       ├── __init__.py
│       ├── schema.py             # Main schema combining all queries
│       ├── types/                # GraphQL types by domain
│       │   ├── __init__.py
│       │   ├── region.py         # Region GraphQL types
│       │   ├── resource.py       # Resource GraphQL types
│       │   └── property.py       # Property GraphQL types
│       ├── queries/              # Query resolvers by domain
│       │   ├── __init__.py
│       │   ├── region.py         # Region queries
│       │   └── resource.py       # Resource queries
│       └── utils/                # Shared utilities
│           ├── __init__.py
│           └── property_tree.py  # Property tree builder
├── run.py                        # Application runner
├── requirements.txt              # Python dependencies
├── sample_queries.graphql        # Example GraphQL queries
└── README.md                     # This file
```

### Modular Architecture

The application follows a **modular architecture** with clear separation of concerns:

#### **Models Layer** (`app/models/`)
- Each domain (region, resource, property) has its own model file
- Easy to add new models without cluttering a single file
- TYPE_CHECKING used to avoid circular imports

#### **GraphQL Layer** (`app/graphql/`)
- **Types**: GraphQL type definitions separated by domain
- **Queries**: Query resolvers organized by domain
- **Utils**: Shared utility functions (like property tree builder)
- **Schema**: Main schema that combines all queries

#### **Configuration** (`app/config.py`)
- Centralized settings using environment variables
- Single source of truth for all configuration

### Adding New Features

#### Adding a New Model
1. Create a new file in `app/models/` (e.g., `app/models/new_model.py`)
2. Define your SQLModel class
3. Export it in `app/models/__init__.py`

#### Adding a New GraphQL Type
1. Create a new file in `app/graphql/types/` (e.g., `app/graphql/types/new_type.py`)
2. Define your `@strawberry.type` class
3. Export it in `app/graphql/types/__init__.py`

#### Adding New Queries
1. Create a new query class in `app/graphql/queries/` (e.g., `app/graphql/queries/new_queries.py`)
2. Define methods with `@strawberry.field` decorator
3. Export the query class in `app/graphql/queries/__init__.py`
4. Add the query class to the main `Query` class in `app/graphql/schema.py`

Example:
```python
# app/graphql/queries/new_queries.py
@strawberry.type
class NewQueries:
    @strawberry.field
    def my_new_query(self) -> str:
        return "Hello"

# app/graphql/schema.py
@strawberry.type
class Query(RegionQueries, ResourceQueries, NewQueries):
    pass
```

## Production Considerations

1. **Environment Variable**: Set `APP_ENV=production` to disable GraphQL Playground
2. **CORS**: Update allowed origins in `app/config.py` for production
3. **Database Connection Pooling**: Configure in `app/database.py`
4. **Environment Variables**: Use proper secret management (never commit `.env` files)
5. **Rate Limiting**: Consider adding rate limiting middleware
6. **Caching**: Implement caching for frequently accessed data
7. **Monitoring**: Add logging and monitoring tools

## License

MIT

