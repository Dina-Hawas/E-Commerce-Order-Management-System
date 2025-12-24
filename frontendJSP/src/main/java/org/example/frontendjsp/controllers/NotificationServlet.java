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

@WebServlet("/sendNotification")
public class NotificationServlet extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String orderId = request.getParameter("order_id");
        int customerId = Integer.parseInt(request.getParameter("customer_id"));


        String jsonPayload = String.format(
                "{\"order_id\": \"%s\", \"customer_id\": %s}",
                orderId, customerId
        );

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest notifReq = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:5005/api/notifications/send"))
                .POST(HttpRequest.BodyPublishers.ofString(jsonPayload))
                .header("Content-Type", "application/json")
                .build();

        try {
            HttpResponse<String> notifRes =
                    client.send(notifReq, HttpResponse.BodyHandlers.ofString());

            System.out.println("Notification Response: " + notifRes.body());

            JSONObject json = new JSONObject(notifRes.body());

            request.setAttribute("status", json.getString("status"));
            request.setAttribute("message", json.getString("message"));

            request.getRequestDispatcher("/notification_result.jsp").forward(request, response);

        } catch (InterruptedException e) {
            e.printStackTrace();
            response.sendError(500, "Notification service unavailable.");
        }
    }
}
