<%@ page contentType="text/html;charset=UTF-8" language="java" %>

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Notification Result</title>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"/>
</head>

<body class="container py-4">

<h2>Notification Status</h2>

<div class="alert alert-success">
    <strong>Status:</strong> ${status}
</div>

<div class="card mt-3">
    <div class="card-body">
        <h5 class="card-title">Message</h5>
        <pre class="mb-0">${message}</pre>
    </div>
</div>

<a href="${pageContext.request.contextPath}/products"
   class="btn btn-secondary mt-4">
    Back to Products
</a>

</body>
</html>
