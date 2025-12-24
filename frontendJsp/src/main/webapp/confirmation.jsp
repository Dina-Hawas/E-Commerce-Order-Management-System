<%@ page import="org.json.JSONArray" %>
<%@ page import="org.json.JSONObject" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Confirmation</title>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"/>
</head>

<body class="container py-4">

<h2>Order Confirmation</h2>

<p><strong>Order ID:</strong> ${orderId}</p>
<p><strong>Status:</strong> ${status}</p>
<p><strong>Timestamp:</strong> ${timestamp}</p>

<hr/>

<%
    JSONArray items = (JSONArray) request.getAttribute("items");

    for (int i = 0; i < items.length(); i++) {
        JSONObject item = items.getJSONObject(i);
%>

<div class="card p-3 mb-3">
    <p><strong>Product:</strong> <%= item.getString("produc_name") %></p>
    <p><strong>Unit Price:</strong> <%= item.getDouble("unit_price") %></p>
    <p><strong>Quantity:</strong> <%= item.getInt("quantity") %></p>
    <p><strong>Total after discount:</strong> <%= item.getDouble("total_after_discount") %></p>
</div>

<%
    }
%>

<hr/>

<p><strong>Tax Amount:</strong> ${taxAmount}</p>
<p><strong>Grand Total:</strong> ${grandTotal}</p>

<form action="${pageContext.request.contextPath}/sendNotification" method="post">
    <input type="hidden" name="order_id" value="${orderId}" />
    <input type="hidden" name="customer_id" value="${customerId}" />

    <button class="btn btn-primary" type="submit">
        Send Notification
    </button>
</form>

</body>
</html>
