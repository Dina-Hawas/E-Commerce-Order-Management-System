package controllers;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import org.json.JSONArray;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@WebServlet("/products")
public class InventoryServlet extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest req = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:5002/api/inventory/all"))
                .GET()
                .build();

        try {
            HttpResponse<String> res =
                    client.send(req, HttpResponse.BodyHandlers.ofString());

            JSONArray products = new JSONArray(res.body());
            request.setAttribute("products", products);
            request.getRequestDispatcher("/index.jsp").forward(request, response);

        } catch (Exception e) {
            response.sendError(500, "Inventory Service Error");
        }
    }
}
