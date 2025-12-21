
<%@ page import="org.json.JSONObject" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Profile</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"/>
</head>
<body class="container py-4">

<%
    JSONObject customer = (JSONObject) request.getAttribute("customer");
    int id = customer.getInt("id");
%>

<h2>Customer Profile</h2>

<div class="card p-3 mt-3">
    <p><strong>ID:</strong> <%= id %></p>
    <p><strong>Name:</strong> <%= customer.optString("name", "N/A") %></p>
    <p><strong>Email:</strong> <%= customer.optString("email", "N/A") %></p>
    <p><strong>Loyalty Points:</strong> <%= customer.optInt("loyalty_points", 0) %></p>
</div>

<div class="mt-3 d-flex gap-2">
    <a class="btn btn-secondary" href="<%= request.getContextPath() %>/products">Back to Products</a>


</div>

</body>
</html>
