package com.finance.cbds.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.finance.cbds.dto.ProjectInputDto;
import com.finance.cbds.entity.ProjectEvaluation;
import com.finance.cbds.service.PeService;

@RestController
@RequestMapping("/projects")
public class PeController {
	
	@Autowired
	private PeService service;
	
	@PostMapping
	public ProjectEvaluation createProject(@RequestBody ProjectInputDto input) {
		return service.saveProject(input);
	}
	
	@GetMapping
	public List<ProjectEvaluation> getAllProjects() {
		return service.getAllProjects();
	}

}
