<%@ page import="java.util.*, org.json.*" %>
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ page import="org.json.*" %>

<html>
<head>
    <meta charset="utf-8"/>
    <title>Product Catalog</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"/>


</head>
<body class="container py-4">

<h1>Product Catalog</h1>

<form action="checkout.jsp" method="get">
    <div class="table-responsive">
        <table class="table table-bordered table-striped table-hover align-middle">
            <thead class="table-dark">
            <tr>
                <th>Product</th>
                <th>Unit Prices</th>
                <th style="width:150px;">Quantity</th>
            </tr>
            </thead>

            <tbody>
            <%
                JSONArray products = (JSONArray) request.getAttribute("${pageContext.request.contextPath}/products");
                if (products != null) {
                    for (int i = 0; i < products.length(); i++) {
                        JSONObject p = products.getJSONObject(i);
            %>
            <tr>
                <td><%= p.getString("product_name") %></td>
                <td>$<%= p.getDouble("unit_price") %></td>
                <td>
                    <input type="number"
                           class="form-control"
                           name="qty_<%= p.getInt("product_id") %>"
                           min="0"
                           value="0">
                </td>
            </tr>
            <%
                    }
                }
            %>
            </tbody>
        </table>
    </div>


<br>
    <div class="text-end mt-3">
        <button type="submit" class="btn btn-success btn-lg">
            Go to Checkout
        </button>
    </div>
</form>

</body>
</html>
