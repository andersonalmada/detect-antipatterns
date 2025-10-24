from observa.repositories import SourceRepository, DetectorRepository

# Registrar uma fonte
SourceRepository.add_source("alerts_source", {"alerts": [{"type": "CPU_HIGH"}]})

# Registrar um detector
DetectorRepository.add_detector("ExcessiveAlerts", class_path="observa.detectors.excessive_alerts.ExcessiveAlertsDetector")

# Listar tudo
print([s.name for s in SourceRepository.get_all()])
print([d.name for d in DetectorRepository.get_all()])
