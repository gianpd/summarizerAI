import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_summaries import crud_summary
from app.schemas.summary_schema import SummaryCreate


@pytest.mark.asyncio
async def test_create_summary_from_text(client: AsyncClient):
    """Test creating summary from text"""
    payload = {"text": "This is a test text for summarization. It contains multiple sentences to test the summarization functionality."}
    response = await client.post("/api/v1/summaries/text", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "text" in data
    assert "summary" in data
    assert data["text"] == payload["text"]
    assert len(data["summary"]) > 0


@pytest.mark.asyncio
async def test_create_summary_from_url(client: AsyncClient):
    """Test creating summary from URL"""
    payload = {"url": "https://example.com"}
    response = await client.post("/api/v1/summaries/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["url"] == payload["url"]


@pytest.mark.asyncio
async def test_get_summary(client: AsyncClient, db_session: AsyncSession):
    """Test getting summary by ID"""
    # Create a summary first
    summary_data = SummaryCreate(
        url="https://example.com",
        summary="Test summary",
        key_top="test",
        keywords="test, example"
    )
    summary = await crud_summary.create(db_session, obj_in=summary_data)
    
    # Get the summary
    response = await client.get(f"/api/v1/summaries/{summary.id}/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == summary.id
    assert data["url"] == str(summary_data.url)


@pytest.mark.asyncio
async def test_get_nonexistent_summary(client: AsyncClient):
    """Test getting non-existent summary"""
    response = await client.get("/api/v1/summaries/999/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_summaries(client: AsyncClient, db_session: AsyncSession):
    """Test getting all summaries"""
    # Create multiple summaries
    for i in range(3):
        summary_data = SummaryCreate(
            url=f"https://example{i}.com",
            summary=f"Test summary {i}",
        )
        await crud_summary.create(db_session, obj_in=summary_data)
    
    response = await client.get("/api/v1/summaries/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_delete_summary(client: AsyncClient, db_session: AsyncSession):
    """Test deleting summary"""
    # Create a summary first
    summary_data = SummaryCreate(
        url="https://example.com",
        summary="Test summary"
    )
    summary = await crud_summary.create(db_session, obj_in=summary_data)
    
    # Delete the summary
    response = await client.delete(f"/api/v1/summaries/{summary.id}/")
    
    assert response.status_code == 200
    
    # Verify it's deleted
    response = await client.get(f"/api/v1/summaries/{summary.id}/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint"""
    response = await client.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}