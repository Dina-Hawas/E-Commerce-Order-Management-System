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
<%

    String[] productIds = request.getParameterValues("selectedProduct");
    String errorMessage = (String) request.getAttribute("errorMessage");

%>

<% if (errorMessage != null) { %>

<div class="alert alert-danger"><%= errorMessage %></div>
<a class="btn btn-secondary" href="<%= request.getContextPath() %>/products">Back to Products</a>

<% } else if (productIds == null || productIds.length == 0) { %>

<div class="alert alert-danger">
    No product selected. Please choose at least one product.
</div>
<a class="btn btn-secondary" href="<%= request.getContextPath() %>/products">Back to Products</a>

<% } else { %>

<form action="<%= request.getContextPath() %>/submitOrder" method="post">

    <div class="mb-3">
        <label class="form-label">Customer ID</label>
        <input class="form-control" type="text" name="customer_id" value="1" readonly />
    </div>

    <h5>Selected Products</h5>

    <% for (String pid : productIds) { %>
    <div class="card p-3 mb-3">
        <div class="mb-2">
            <label class="form-label">Product ID</label>
            <input class="form-control" type="text"
                   name="product_id[]" value="<%= pid %>" readonly />
        </div>

        <div class="mb-2">
            <label class="form-label">Quantity</label>
            <input class="form-control" type="number"
                   name="quantity[]" min="1" required />
        </div>
    </div>
    <% } %>

    <button class="btn btn-success" type="submit">Place Order</button>
    <a class="btn btn-secondary" href="<%= request.getContextPath() %>/products">Cancel</a>
</form>

<%}%>
</body>
</html>
