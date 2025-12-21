<%@ page import="org.json.JSONArray" %>
<%@ page import="org.json.JSONObject" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Orders History</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"/>
</head>
<body class="container py-4">

<h2>Orders History</h2>
<p class="text-muted">Customer ID: 1</p>

<%
    JSONArray orders = (JSONArray) request.getAttribute("orders");
    if (orders == null || orders.length() == 0) {
%>
<div class="alert alert-info">No orders found.</div>
<%
} else {
    for (int i = 0; i < orders.length(); i++) {
        JSONObject o = orders.getJSONObject(i);
%>
<div class="card p-3 mb-3">
    <p><strong>Order ID:</strong> <%= o.optString("order_id", o.optString("_id", "N/A")) %></p>
    <p><strong>Status:</strong> <%= o.optString("status", "N/A") %></p>
    <p><strong>Timestamp:</strong> <%= o.optString("timestamp", o.optString("created_at", "N/A")) %></p>

    <%
        // If order details include totals
        JSONObject pricing = o.optJSONObject("pricing");
        if (pricing != null) {
    %>
    <p><strong>Grand Total:</strong> <%= pricing.optDouble("grand_total") %></p>
    <%
        }
    %>
</div>
<%
        }
    }
%>

<a class="btn btn-secondary" href="<%= request.getContextPath() %>/products">Back to Products</a>

</body>
</html>