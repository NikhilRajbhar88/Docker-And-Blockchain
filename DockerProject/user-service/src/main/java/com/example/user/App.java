package com.example.user;

import org.springframework.boot.*;
import org.springframework.boot.autoconfigure.*;
import org.springframework.web.bind.annotation.*;

@SpringBootApplication
@RestController
public class App {

    @GetMapping("/user")
    public String getUser() {
        return "Hello from User Service - Host: " + System.getenv("HOSTNAME");
    }

    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }
}
