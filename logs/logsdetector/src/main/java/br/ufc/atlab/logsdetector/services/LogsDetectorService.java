package br.ufc.atlab.logsdetector.services;

import java.time.Instant;
import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import tools.jackson.databind.ObjectMapper;

@Service
public class LogsDetectorService {

    private static final int REPETITION_THRESHOLD = 5;
    private static final int MAX_KBYTES_PER_SECOND = 1;

    private final ObjectMapper mapper = new ObjectMapper();

    public Map<String, Object> detect(List<Map<String, Object>> data) {

        // initialize flags
        for (Map<String, Object> item : data) {
            item.put("detected", false);
            item.put("reason", "");
        }

        detectVolumeSpikes(data);
        detectRepetitiveMessages(data);
        detectLevel(data);

        long detectedCount = data.stream()
                .filter(d -> Boolean.TRUE.equals(d.get("detected")))
                .count();

        Map<String, Object> response = new HashMap<>();
        response.put("analyzed", data.size());
        response.put("detected", detectedCount);
        response.put("data", data);

        return response;
    }

    /* -----------------------------------
       detect_volume_spikes
    ----------------------------------- */
    private void detectVolumeSpikes(List<Map<String, Object>> data) {
        Map<Instant, List<Map<String, Object>>> grouped = groupBySecond(data);

        grouped.forEach((second, logs) -> {
            try {
                byte[] jsonBytes = mapper.writeValueAsBytes(logs);
                double kbytes = jsonBytes.length / 1024.0;

                if (kbytes > MAX_KBYTES_PER_SECOND) {
                    for (Map<String, Object> log : logs) {
                        if (Boolean.FALSE.equals(log.get("detected"))) {
                            log.put("detected", true);
                            log.put("reason", "detect_volume_spikes");
                        }
                    }
                }
            } catch (Exception ignored) {
            }
        });
    }

    /* -----------------------------------
       detect_repetitive_messages
    ----------------------------------- */
    private void detectRepetitiveMessages(List<Map<String, Object>> data) {

        Map<String, Long> counter = data.stream()
                .map(log -> (String) log.get("message"))
                .collect(Collectors.groupingBy(m -> m, Collectors.counting()));

        Set<String> repetitive = counter.entrySet().stream()
                .filter(e -> e.getValue() >= REPETITION_THRESHOLD)
                .map(Map.Entry::getKey)
                .collect(Collectors.toSet());

        for (Map<String, Object> log : data) {
            if (repetitive.contains(log.get("message"))
                    && Boolean.FALSE.equals(log.get("detected"))) {
                log.put("detected", true);
                log.put("reason", "detect_repetitive_messages");
            }
        }
    }

    /* -----------------------------------
       detect_level
    ----------------------------------- */
    private void detectLevel(List<Map<String, Object>> data) {
        for (Map<String, Object> log : data) {
            String level = (String) log.get("level");
            if (("DEBUG".equals(level) || "TRACE".equals(level))
                    && Boolean.FALSE.equals(log.get("detected"))) {
                log.put("detected", true);
                log.put("reason", "detect_level");
            }
        }
    }

    /* -----------------------------------
       Utilities
    ----------------------------------- */
    private Map<Instant, List<Map<String, Object>>> groupBySecond(List<Map<String, Object>> logs) {

        Map<Instant, List<Map<String, Object>>> grouped = new HashMap<>();

        for (Map<String, Object> log : logs) {
            String ts = (String) log.get("timestamp");

            Instant instant = OffsetDateTime.parse(ts).withNano(0).toInstant();

            grouped.computeIfAbsent(instant, k -> new ArrayList<>()).add(log);
        }

        return grouped;
    }
}