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
	
	public MLResponseDto getPrediction(ProjectInputDto input) {
		
		String url = "http://127.0.0.1:8000/predict";
		

//		Map<String, Object> request = new HashMap<>();

//		request.put("initialInvestment", input.getInitialInvestment());
//		request.put("revenueGrowthRate", input.getRevenueGrowthRate());
//		request.put("inflationRate", input.getInflationRate());
//		request.put("marketGrowthIndex", input.getMarketGrowthIndex());
//		request.put("sectorRiskIndex", input.getSectorRiskIndex());
//		request.put("discountRate", input.getDiscountRate());
		
		//spring converts project input dto -> inpuy to json 
        MLResponseDto response = restTemplate.postForObject(url, input, MLResponseDto.class);
        
        //to confirm the mapping
        System.out.println("Mean NPV: " + response.getMonteCarlo().getMeanNPV());
        System.out.println("Risk Probability: " + response.getMonteCarlo().getRiskProbability());

        return response;
	}
}
