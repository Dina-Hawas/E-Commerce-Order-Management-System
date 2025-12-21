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

@WebServlet("/profile")
public class ProfileServlet extends HttpServlet {

    private static final String CUSTOMER_BASE = "http://localhost:5004";

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        // ✅ use customer_id consistently
        String customerId = request.getParameter("customer_id");

        // (optional) fallback to session if you ever store it
        if (customerId == null || customerId.isBlank()) {
            Object sessionId = request.getSession().getAttribute("customer_id");
            if (sessionId != null) customerId = sessionId.toString();
        }

        if (customerId == null || customerId.isBlank()) {
            response.sendError(400, "Missing customer_id. Use /profile?customer_id=1");
            return;
        }

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest req = HttpRequest.newBuilder()
                // ✅ correct URL
                .uri(URI.create(CUSTOMER_BASE + "/api/customers/" + customerId))
                .GET()
                .build();

        try {
            HttpResponse<String> res = client.send(req, HttpResponse.BodyHandlers.ofString());

            if (res.statusCode() >= 400) {
                response.sendError(res.statusCode(), "Customer service error: " + res.body());
                return;
            }

            JSONObject customerJson = new JSONObject(res.body());
            request.setAttribute("customer", customerJson);

            request.getRequestDispatcher("/profile.jsp").forward(request, response);

        } catch (InterruptedException e) {
            response.sendError(500, "Customer service unavailable.");
        }
    }
}
