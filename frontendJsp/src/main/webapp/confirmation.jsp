
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
