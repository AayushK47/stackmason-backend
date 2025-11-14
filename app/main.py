"""FastAPI application with Strawberry GraphQL."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.config import settings
from app.graphql import schema

# Create FastAPI app
app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Create GraphQL router
graphql_app = GraphQLRouter(
    schema,
    graphiql=settings.IS_LOCAL
)

# Mount GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": settings.APP_TITLE,
        "graphql_endpoint": "/graphql",
        "environment": settings.APP_ENV,
        "playground_enabled": settings.IS_LOCAL
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

