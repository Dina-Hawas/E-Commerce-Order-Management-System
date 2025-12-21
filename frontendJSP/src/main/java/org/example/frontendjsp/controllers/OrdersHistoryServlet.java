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

@WebServlet("/ordersHistory")
public class OrdersHistoryServlet extends HttpServlet {

    private static final String CUSTOMER_BASE = "http://localhost:5004";
    private static final String ORDER_BASE    = "http://localhost:5001";

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String customerId = request.getParameter("customer_id");
        if (customerId == null || customerId.isBlank()) {
            Object sessionId = request.getSession().getAttribute("customer_id");
            if (sessionId != null) customerId = sessionId.toString();
        }

        if (customerId == null || customerId.isBlank()) {
            response.sendError(400, "Missing customer_id. Use /ordersHistory?customer_id=1");
            return;
        }

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest ordersReq = HttpRequest.newBuilder()
                .uri(URI.create(CUSTOMER_BASE + "/api/customers/" + customerId + "/orders"))
                .GET()
                .build();

        try {
            HttpResponse<String> ordersRes = client.send(ordersReq, HttpResponse.BodyHandlers.ofString());
            if (ordersRes.statusCode() >= 400) {
                response.sendError(ordersRes.statusCode(), "Customer service error: " + ordersRes.body());
                return;
            }

            JSONObject payload = new JSONObject(ordersRes.body());
            JSONObject customerObj = payload.getJSONObject("customer");
            JSONArray ordersArray = payload.getJSONArray("orders");

            // If orders are already detailed enough, you can just pass ordersArray directly.
            // But to satisfy the PDF requirement, we fetch details per order_id (if needed).
            JSONArray detailedOrders = new JSONArray();

            for (int i = 0; i < ordersArray.length(); i++) {
                JSONObject o = ordersArray.getJSONObject(i);

                // try common keys
                String orderId = o.optString("order_id", o.optString("id", o.optString("_id", "")));

                // If no order id, just include whatever we have
                if (orderId.isBlank()) {
                    detailedOrders.put(o);
                    continue;
                }

                HttpRequest detailReq = HttpRequest.newBuilder()
                        .uri(URI.create(ORDER_BASE + "/api/orders/" + orderId))
                        .GET()
                        .build();

                HttpResponse<String> detailRes = client.send(detailReq, HttpResponse.BodyHandlers.ofString());
                if (detailRes.statusCode() < 400) {
                    detailedOrders.put(new JSONObject(detailRes.body()));
                } else {
                    // fallback to original
                    detailedOrders.put(o);
                }
            }

            request.setAttribute("customer", customerObj);
            request.setAttribute("orders", detailedOrders);
            request.getRequestDispatcher("/orders_history.jsp").forward(request, response);

        } catch (InterruptedException e) {
            response.sendError(500, "Services unavailable.");
        }
    }
}
