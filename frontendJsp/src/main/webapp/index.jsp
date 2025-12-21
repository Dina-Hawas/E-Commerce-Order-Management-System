<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%
  if (request.getAttribute("productsJson") == null) {
    response.sendRedirect("products");
    return;
  }
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>Inventory Products</title>

  <!-- Bootstrap (same as old index.jsp) -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"/>

  <!-- CSS to make your div-cards match the Bootstrap look -->
  <style>
    body.container {
      max-width: 960px;
    }
    #products .product-card {
      border: 1px solid var(--bs-border-color);
      border-radius: .5rem;
      padding: 1rem;
      margin-bottom: .75rem;
      background: var(--bs-body-bg);
    }
    #products .product-title {
      font-weight: 700;
      font-size: 1.05rem;
      margin-bottom: .25rem;
    }
    #products .meta {
      color: var(--bs-secondary-color);
      font-size: .95rem;
    }
    #products .meta-row {
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
      margin-top: .25rem;
    }
    #products .meta-row span {
      background: var(--bs-tertiary-bg);
      border: 1px solid var(--bs-border-color);
      border-radius: .375rem;
      padding: .2rem .5rem;
    }
  </style>
</head>

<body class="container py-4">
<a class="btn btn-outline-primary" href="<%=request.getContextPath()%>/profile?customer_id=1">Profile</a>
<a class="btn btn-outline-secondary" href="<%=request.getContextPath()%>/ordersHistory?customer_id=1">Orders History</a>

<h1 class="mb-4">Product Catalog</h1>

<%
  String productsJson = (String) request.getAttribute("productsJson");
  if (productsJson == null) productsJson = "[]";
%>

<div id="products"></div>

<script>
  const products = <%= productsJson %>;
  const root = document.getElementById("products");

  if (!Array.isArray(products)) {
    root.innerHTML = `<div class="alert alert-danger">
            <b>Error:</b> Inventory service did not return a JSON array.
        </div>`;
  } else if (products.length === 0) {
    root.innerHTML = `<div class="alert alert-warning">
            No products found (or you opened index.jsp directly instead of /products).
        </div>`;
  } else {
    root.innerHTML = products.map(p => `
          <div class="product-card shadow-sm">
            <div class="product-title">\${p.product_name || ""}</div>
            <div class="meta-row meta">
              <span><b>ID:</b> \${p.product_id ?? ""}</span>
              <span><b>Price:</b> \$\${p.unit_price ?? ""}</span>
              <span><b>Available:</b> \${p.quantity_available ?? ""}</span>
            </div>
          </div>
        `).join("");
  }
</script>

<hr class="mt-4"/>
<br>
<div class="text-end mt-3">
  <a href="checkout.jsp" class="btn btn-success btn-lg">
    Go to Checkout
  </a>
</div>
</body>
</html>