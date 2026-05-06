#!/bin/bash
# API Test Script for AI Education Platform

BASE_URL="http://localhost:8000/api/v1"

echo "=== AI Education Platform API Test ==="
echo ""

# 1. Register
echo "1. Registering user..."
REGISTER=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@school.edu.hk","username":"demo","password":"demo123","role":"teacher"}')
echo "Register: $REGISTER"
TOKEN=$(echo $REGISTER | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "Login instead..."
  LOGIN=$(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"email":"demo@school.edu.hk","password":"demo123"}')
  TOKEN=$(echo $LOGIN | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
fi

echo "Token: ${TOKEN:0:50}..."
echo ""

# 2. Get Profile
echo "2. Getting profile..."
curl -s -X GET "$BASE_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN" | jq .
echo ""

# 3. Test RAG Query (as JSON body)
echo "3. Testing RAG query..."
curl -s -X POST "$BASE_URL/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "math formula",
    "school_id": "b52ed795-43d2-4ad3-b765-a48e24c35862",
    "top_k": 3
  }' | jq .
echo ""

# 4. Get RAG stats
echo "4. Getting RAG stats..."
curl -s -X GET "$BASE_URL/rag/stats/b52ed795-43d2-4ad3-b765-a48e24c35862" | jq .
echo ""

echo "=== Test Complete ==="