#!/bin/bash
# Demo Data Upload Script v2

BASE_URL="http://localhost:8000/api/v1"

echo "=== Uploading Demo Data ==="
echo ""

# Login to get token
echo "1. Logging in..."
LOGIN=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@school.edu.hk","password":"demo123"}')
TOKEN=$(echo $LOGIN | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
echo "Token obtained: ${TOKEN:0:30}..."
echo ""

# Create temp file for upload
echo "2. Creating sample documents..."

# Document 1: Algebra
cat > /tmp/algebra.txt << 'EOF'
Algebra Basics - Chapter 1

Introduction to Algebra

Algebra is a branch of mathematics that uses letters and symbols to represent numbers and quantities.

Key Concepts:
1. Variables: Letters that represent unknown values (e.g., x, y, z)
2. Constants: Fixed numerical values (e.g., 3, 5, -2)
3. Expressions: Combinations like 3x + 5
4. Equations: Statements showing equality like 2x + 3 = 11

Solving Simple Equations:
- x + 5 = 12 → x = 7
- 3x = 15 → x = 5
- 2x + 3 = 11 → x = 4
EOF

# Document 2: Geometry
cat > /tmp/geometry.txt << 'EOF'
Geometry Basics - Chapter 2

Introduction to Geometry

Geometry studies shapes, sizes, and properties of space.

Basic Shapes:
- Triangle: 3 sides, 3 angles, sum = 180 degrees
- Square: 4 equal sides, 4 right angles (90 degrees)
- Rectangle: 4 sides, opposite sides equal

Area Formulas:
- Triangle: A = 1/2 × base × height
- Square: A = side squared
- Rectangle: A = length × width

Example: Rectangle 8cm × 5cm
Area = 40 cm squared
Perimeter = 26 cm
EOF

# Document 3: Fractions
cat > /tmp/fractions.txt << 'EOF'
Fractions - Chapter 3

Understanding Fractions

A fraction represents a part of a whole with numerator and denominator.

Examples:
- 1/2 = one half
- 3/4 = three quarters

Operations:
- Addition: a/b + c/d = (ad + bc)/bd
- Multiplication: a/b × c/d = ac/bd

Converting to Decimals:
- 1/2 = 0.5
- 1/4 = 0.25

Practice: 3/4 + 1/2 = 5/4 = 1.25
EOF

echo "3. Uploading algebra document..."
curl -s -X POST "$BASE_URL/knowledge/upload?title=Algebra%20Basics&kb_type=textbook" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/algebra.txt" | jq .

echo ""
echo "4. Uploading geometry document..."
curl -s -X POST "$BASE_URL/knowledge/upload?title=Geometry%20Basics&kb_type=textbook" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/geometry.txt" | jq .

echo ""
echo "5. Uploading fractions document..."
curl -s -X POST "$BASE_URL/knowledge/upload?title=Fractions&kb_type=textbook" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/fractions.txt" | jq .

echo ""
echo "=== Checking Results ==="
echo "6. Getting RAG stats..."
curl -s "$BASE_URL/rag/stats/b52ed795-43d2-4ad3-b765-a48e24c35862" | jq .

echo ""
echo "7. Testing RAG query..."
curl -s -X POST "$BASE_URL/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How to solve algebraic equations?",
    "school_id": "b52ed795-43d2-4ad3-b765-a48e24c35862",
    "top_k": 2
  }' | jq .

echo ""
echo "=== Demo Complete ==="