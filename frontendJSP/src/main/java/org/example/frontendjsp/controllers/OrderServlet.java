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

import org.json.JSONArray;
import org.json.JSONObject;

@WebServlet("/submitOrder")
public class OrderServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        int customerId = Integer.parseInt(request.getParameter("customer_id"));

        String[] productIds = request.getParameterValues("product_id[]");
        String[] quantities = request.getParameterValues("quantity[]");

        if (productIds == null || quantities == null || productIds.length != quantities.length) {
            request.setAttribute("errorMessage", "Invalid order data.");
            request.getRequestDispatcher("/checkout.jsp").forward(request, response);
            return;
        }

        // Build products array
        JSONArray productsArray = new JSONArray();

        for (int i = 0; i < productIds.length; i++) {
            JSONObject item = new JSONObject();
            item.put("product_id", Integer.parseInt(productIds[i]));
            item.put("quantity", Integer.parseInt(quantities[i]));
            productsArray.put(item);
        }

        // Final payload
        JSONObject payload = new JSONObject();
        payload.put("customer_id", customerId);
        payload.put("products", productsArray);

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest orderReq = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:5001/api/orders/create"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(payload.toString()))
                .build();

        try {
            HttpResponse<String> orderRes =
                    client.send(orderReq, HttpResponse.BodyHandlers.ofString());

            if (orderRes.statusCode() != 201) {
                request.setAttribute(
                        "errorMessage",
                        "Requested quantity exceeds available stock."
                );
                request.getRequestDispatcher("/checkout.jsp").forward(request, response);
                return;
            }

            JSONObject json = new JSONObject(orderRes.body());

            request.setAttribute("orderId", json.getString("order_id"));
            request.setAttribute("customerId", json.getInt("customer_id"));
            request.setAttribute("status", json.getString("status"));
            request.setAttribute("timestamp", json.getString("timestamp"));

            JSONObject pricing = json.getJSONObject("pricing");
            request.setAttribute("subtotal", pricing.getDouble("subtotal"));
            request.setAttribute("taxAmount", pricing.getDouble("tax_amount"));
            request.setAttribute("grandTotal", pricing.getDouble("grand_total"));
            request.setAttribute("items", pricing.getJSONArray("items"));

            request.getRequestDispatcher("/confirmation.jsp").forward(request, response);

        } catch (InterruptedException e) {
            response.sendError(500, "Order service unavailable.");
        }
    }
}
