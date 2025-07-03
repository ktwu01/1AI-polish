import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """测试健康检查"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_process_text():
    """测试文本处理接口"""
    test_data = {
        "content": "人工智能技术在学术写作中的应用越来越广泛。",
        "style": "academic"
    }
    
    response = client.post("/api/v1/process", json=test_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "original_text" in data
    assert "processed_text" in data
    assert "ai_probability" in data
    assert "processing_time" in data
    assert data["ai_probability"] >= 0.0
    assert data["ai_probability"] <= 1.0

def test_async_process_text():
    """测试异步文本处理接口"""
    test_data = {
        "content": "这是一个测试文本，用于验证异步处理功能。",
        "style": "formal"
    }
    
    response = client.post("/api/v1/process/async", json=test_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "task_id" in data
    assert "status" in data
    assert data["status"] == "processing"

def test_invalid_text_request():
    """测试无效请求"""
    # 空文本测试
    response = client.post("/api/v1/process", json={"content": ""})
    assert response.status_code == 422
    
    # 超长文本测试
    long_text = "a" * 20000
    response = client.post("/api/v1/process", json={"content": long_text})
    assert response.status_code == 422

def test_invalid_style_request():
    """测试无效风格参数"""
    test_data = {
        "content": "测试文本",
        "style": "unknown"
    }

    response = client.post("/api/v1/process", json=test_data)
    assert response.status_code == 422
