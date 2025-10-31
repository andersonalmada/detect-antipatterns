from observa.framework.orchestrator import Orchestrator
from observa.sources.frutas_source import FrutasLocal
from observa.detectors.frutas_detector import FrutasExcessivas

orchestrator = Orchestrator()

source = FrutasLocal("FrutasLocal")
detector = FrutasExcessivas("FrutasExcessivas")

print(orchestrator.run(source=source, detector=detector))


