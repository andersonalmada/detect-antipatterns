from observa.framework.orchestrator import Orchestrator
from observa.sources.frutas_source import FrutasLocal
from observa.detectors.frutas_detector import FrutasExcessivas

orchestrator = Orchestrator()

source = FrutasLocal()
detector = FrutasExcessivas()

print(orchestrator.run(source=source, detector=detector))


