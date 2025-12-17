<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Checkout</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"/>
</head>

<body class="container py-4">
<h1>Checkout</h1>

<form action="<%= request.getContextPath() %>/submitOrder" method="post">

    <div class="mb-3">
        <label class="form-label">Customer ID</label>
        <input class="form-control" type="text" name="customer_id"  required />
    </div>

    <div class="mb-3">
        <label class="form-label">Product ID</label>
        <input class="form-control" type="text" name="product_id" />
    </div>

    <div class="mb-3">
        <label class="form-label">Quantity</label>
        <input class="form-control" type="number" name="quantity"  min="1" required />
    </div>

    <button class="btn btn-success" type="submit">Place Order</button>
</form>

</body>
</html>
