package com.finance.cbds.service;

import java.util.Map;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class MLServiceClient {
	private final String ML_API_URL = "http://127.0.0.1:8000/predict";
	
	public Map<String, Object> getPrediction(Map<String, Object> inputData) {
		RestTemplate restTemplate = new RestTemplate();
		
		Map<String, Object> response = restTemplate.postForObject(ML_API_URL, inputData, Map.class);
		return response;
	}
}
