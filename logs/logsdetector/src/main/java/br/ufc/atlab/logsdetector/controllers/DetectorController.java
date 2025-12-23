package br.ufc.atlab.logsdetector.controllers;

import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import br.ufc.atlab.logsdetector.services.LogsDetectorService;

@RestController
public class DetectorController {

    private final LogsDetectorService detectorService;

    public DetectorController(LogsDetectorService detectorService) {
        this.detectorService = detectorService;
    }

    @PostMapping("/detector")
    public Map<String, Object> detect(@RequestBody List<Map<String, Object>> inputData) {
        return detectorService.detect(inputData);
    }
}
