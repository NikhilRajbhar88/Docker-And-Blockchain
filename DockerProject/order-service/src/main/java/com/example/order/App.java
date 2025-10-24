package com.example.order;

import org.springframework.boot.*;
import org.springframework.boot.autoconfigure.*;
import org.springframework.web.bind.annotation.*;

@SpringBootApplication
@RestController
public class App {

    @GetMapping("/order")
    public String getOrder() {
        return "Hello from Order Service - Host: " + System.getenv("HOSTNAME");
    }

    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }
}
