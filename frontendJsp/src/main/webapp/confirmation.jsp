<%@ page import="org.json.JSONObject" %>
<%@ page import="org.json.JSONArray" %>
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

<p>
    <strong>Order ID:</strong> ${orderId}
    <br/>

    <%
        JSONObject pricing = (JSONObject) request.getAttribute("pricing");
        JSONArray items = (JSONArray) request.getAttribute("items");

        for (int i = 0; i < items.length(); i++) {
            JSONObject item = items.getJSONObject(i);
    %>

    <strong>product:</strong><%= item.getString("produc_name") %>
    <br/>
    <strong>unit price:</strong><%= item.getDouble("unit_price") %>
    <br/>
    <strong>quantity:</strong><%= item.getInt("quantity") %>
    <br/>
    <strong>total price after discount:</strong><%= item.getDouble("total_after_discount") %>
    <br/>
    <strong>tax amount:</strong> <%= pricing.getDouble("tax_amount")%>
    <br/>
    <strong>grand total:</strong> <%= pricing.getDouble("grand_total")%>
    <br/>
    <strong>status:</strong> ${status}
    <br/>
    <strong>timestamp:</strong> ${timestamp}
    <br/>

    <%
        }
    %>

</p>

<form action="${pageContext.request.contextPath}/sendNotification" method="post">
    <input type="hidden" name="order_id" value="${orderId}" />
    <input type="hidden" name="customer_id" value="${customerId}" />

    <button class="btn btn-primary" type="submit">
        Send Notification
    </button>
</form>

</body>
</html>
