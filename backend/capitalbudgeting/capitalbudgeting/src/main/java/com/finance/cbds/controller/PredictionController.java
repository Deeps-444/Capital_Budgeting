package com.finance.cbds.controller;

import java.util.Map;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.finance.cbds.service.MLServiceClient;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins =  "http://localhost:3000")
public class PredictionController {
	private final MLServiceClient mlServiceClient;
	
	public PredictionController(MLServiceClient mlServiceClient) {
		this.mlServiceClient = mlServiceClient;
	}
	
	@PostMapping("/evaluate")
	public Map<String, Object> evaluateProject(@RequestBody Map<String, Object> input) {
		return mlServiceClient.getPrediction(input);
	}
}
