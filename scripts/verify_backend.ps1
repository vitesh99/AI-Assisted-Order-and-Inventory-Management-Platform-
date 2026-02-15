# Backend Verification Script

$GatewayUrl = "http://localhost:8000/api/v1"
$AdminEmail = "admin@example.com"
$AdminPassword = "adminpassword"

Write-Host "--- 1. Testing Health ---"
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "Gateway Health: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "Gateway Down! Make sure docker is running." -ForegroundColor Red
    exit
}

Write-Host "`n--- 2. Signup Admin User ---"
try {
    $body = @{
        email = $AdminEmail
        password = $AdminPassword
        full_name = "Admin User"
    } | ConvertTo-Json
    
    $signup = Invoke-RestMethod -Uri "$GatewayUrl/auth/signup" -Method Post -Body $body -ContentType "application/json"
    Write-Host "Signup Success: $($signup.email)" -ForegroundColor Green
} catch {
    Write-Host "Signup Failed (User might exist): $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`n--- 3. Make User Superuser (via DB) ---"
# We need this to add products
docker exec -i ai_inventory_db psql -U user -d ai_inventory_auth -c "UPDATE users SET is_superuser = true WHERE email = '$AdminEmail';" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Granted Superuser privs to $AdminEmail" -ForegroundColor Green
} else {
    Write-Host "Failed to grant Superuser privs. Check docker container name." -ForegroundColor Red
}

Write-Host "`n--- 4. Login ---"
try {
    $form = @{
        username = $AdminEmail
        password = $AdminPassword
    }
    $tokenResponse = Invoke-RestMethod -Uri "$GatewayUrl/auth/login" -Method Post -Body $form
    $Token = $tokenResponse.access_token
    $Headers = @{ Authorization = "Bearer $Token" }
    Write-Host "Login Success! Token received." -ForegroundColor Green
} catch {
    Write-Host "Login Failed: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

Write-Host "`n--- 5. Add Product (Inventory) ---"
try {
    $prodBody = @{
        name = "AI Chip"
        description = "High performance chip"
        price = 199.99
        stock_quantity = 50
    } | ConvertTo-Json
    
    $product = Invoke-RestMethod -Uri "$GatewayUrl/inventory/" -Method Post -Body $prodBody -Headers $Headers -ContentType "application/json"
    Write-Host "Product Created: $($product.name) (ID: $($product.id))" -ForegroundColor Green
    $ProductId = $product.id
} catch {
    Write-Host "Create Product Failed: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

Write-Host "`n--- 6. Create Order (Order Service) ---"
try {
    $orderBody = @{
        items = @(
            @{
                product_id = $ProductId
                quantity = 2
            }
        )
    } | ConvertTo-Json
    
    $order = Invoke-RestMethod -Uri "$GatewayUrl/orders/" -Method Post -Body $orderBody -Headers $Headers -ContentType "application/json"
    Write-Host "Order Created: Order #$($order.id) - Total: $($order.total_amount)" -ForegroundColor Green
    $OrderId = $order.id
} catch {
    Write-Host "Create Order Failed: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

Write-Host "`n--- 7. Check AI Summary (Async) ---"
Write-Host "Waiting 5 seconds for AI..."
Start-Sleep -Seconds 5
try {
    $summary = Invoke-RestMethod -Uri "$GatewayUrl/orders/$OrderId/ai-summary" -Method Get -Headers $Headers
    Write-Host "AI Summary: $($summary.summary)" -ForegroundColor Cyan
    Write-Host "Notification Draft: $($summary.notification_draft)" -ForegroundColor Cyan
} catch {
    Write-Host "Fetch Summary Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n--- VERIFICATION COMPLETE ---"
