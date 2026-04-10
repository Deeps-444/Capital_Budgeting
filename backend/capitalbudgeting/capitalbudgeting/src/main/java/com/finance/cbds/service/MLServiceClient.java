package com.finance.cbds.service;

import java.util.HashMap;
import java.util.Map;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.finance.cbds.dto.MLResponseDto;
import com.finance.cbds.dto.ProjectInputDto;

@Service
public class MLServiceClient {
	
	// to call python ml api
	private final RestTemplate restTemplate = new RestTemplate();
	
	public MLResponseDto getPrediction(ProjectInputDto input, double marketIndex, double riskIndex) {
		
		String url = "http://127.0.0.1:8000/predict";
		
		// making custom request
		Map<String, Object> request = new HashMap<>();

	    request.put("initialInvestment", input.getInitialInvestment());
	    request.put("revenueGrowthRate", input.getRevenueGrowthRate());
	    request.put("inflationRate", input.getInflationRate());
	    request.put("marketGrowthIndex", marketIndex);   
	    request.put("sectorRiskIndex", riskIndex);       
	    request.put("discountRate", input.getDiscountRate());
		
		//spring converts project input dto -> input to json 
        MLResponseDto response = restTemplate.postForObject(url, request, MLResponseDto.class);
        // exception for safety
        if (response == null) {
            throw new RuntimeException("ML Service returned null response");
        }
        
        //to confirm the mapping
        if (response.getMonteCarlo() != null) {
            System.out.println("Mean NPV: " + response.getMonteCarlo().getMeanNPV());
            System.out.println("Risk Probability: " + response.getMonteCarlo().getRiskProbability());
        }

        System.out.println("NPV: " + response.getNpv());
        System.out.println("IRR: " + response.getIrr());
        
        System.out.println(response);
        return response;
	}
}
