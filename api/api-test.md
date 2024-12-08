## 1. Hiển thị Product 
curl -X GET "http://127.0.0.1:8000/products/" \
-H "Content-Type: application/json"

## 2. Tạo Order
# Một sản phẩm
curl -X POST "http://127.0.0.1:8000/orders/" \
-H "Content-Type: application/json" \
-d '{
  "uid": "1234567890",
  "orders": [
    {"product_id": "604a1774-775d-4267-b347-7ff1db6580db", "quantity": 2}
  ]
}'

# Nhiều sản phẩm
curl -X POST "http://127.0.0.1:8000/orders/" \
-H "Content-Type: application/json" \
-d '{
  "uid": "1234567891",
  "orders": [
    {
      "product_id": "604a1774-775d-4267-b347-7ff1db6580db",
      "quantity": 2
    },
    {
      "product_id": "5bfe9058-f4a8-4e60-b07a-02b4b9fbca9d",
      "quantity": 1
    }
  ]
}'

## 3. Hiển thị Order theo UserID
curl -X GET "http://127.0.0.1:8000/orders/1234567890" \
-H "Content-Type: application/json"

## 4. Xoá Order 
curl -X DELETE "http://127.0.0.1:8000/orders/8bde4352-01d0-469f-b9ab-f088013088f5" \
-H "Content-Type: application/json"

## 5. Thay đổi Order
curl -X PUT "http://127.0.0.1:8000/orders/" \
-H "Content-Type: application/json" \
-d '{
  "oid": "da56e36d-23c0-4d21-9c92-e798c64aac35",
  "orders": [
    {
      "product_id": "604a1774-775d-4267-b347-7ff1db6580db",
      "quantity": 3
    }
  ]
}'
