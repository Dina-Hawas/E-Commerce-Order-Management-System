package org.example.frontendjsp.controllers;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import org.json.JSONObject;

@WebServlet("/submitOrder")
public class OrderServlet extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        int customerId = Integer.parseInt(request.getParameter("customer_id"));
        int productId = Integer.parseInt(request.getParameter("product_id"));
        int quantity = Integer.parseInt(request.getParameter("quantity"));

        // Build JSON payload
        String jsonPayload = String.format(
                "{\"customer_id\":%s,\"products\":[{\"product_id\":%s,\"quantity\":%s}]}",
                customerId, productId, quantity
        );

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest orderReq = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:5001/api/orders/create"))
                .POST(HttpRequest.BodyPublishers.ofString(jsonPayload))
                .header("Content-Type", "application/json")
                .build();

        try {
            HttpResponse<String> orderRes = client.send(orderReq, HttpResponse.BodyHandlers.ofString());
            System.out.println("Order Service Response: " + orderRes.body());

            JSONObject json = new JSONObject(orderRes.body());


            request.setAttribute("orderId", json.getString("order_id"));
            request.setAttribute("customerId", json.getInt("customer_id"));

            request.getRequestDispatcher("/confirmation.jsp").forward(request, response);

        } catch (InterruptedException e) {
            e.printStackTrace();
            response.sendError(500, "Order service unavailable.");
        }
    }
}
