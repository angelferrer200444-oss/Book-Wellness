from models.Ob_Logros.logros1 import Logros1
from models.Ob_Logros.logros2 import Logros2
from models.Ob_Logros.logros3 import Logros3


class Logros:

    @staticmethod
    def obtener_logros(usuario_id):
        return {
            "logros1": Logros1.obtener_logros(usuario_id),
            "logros2": Logros2.obtener_logros(usuario_id),
            "logros3": Logros3.obtener_logros(usuario_id),
        }
