from sqlalchemy import func

class GeoUtils:
    @staticmethod
    def criar_ponto(latitude: float, longitude: float):
        return func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)

    @staticmethod
    def validar_coordenadas(latitude: float, longitude: float) -> bool:
        return -90 <= latitude <= 90 and -180 <= longitude <= 180
