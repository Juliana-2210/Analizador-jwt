"""
Configuración de conexión a MongoDB Atlas
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from datetime import datetime

load_dotenv()

# Obtener la URL de conexión de variables de entorno
MONGODB_URI = os.getenv("MONGODB_URI", "")

class MongoDBConnection:
    """Gestor de conexión a MongoDB Atlas"""
    
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self.connect()
    
    def connect(self):
        """Conectar a MongoDB Atlas"""
        try:
            if not MONGODB_URI:
                print("⚠️ MONGODB_URI no configurada. Modo offline.")
                self._client = None
                self._db = None
                return False
            
            self._client = MongoClient(
                MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
            )
            
            # Verificar conexión
            self._client.admin.command('ping')
            self._db = self._client['jwt_analyzer']
            
            print("✅ Conectado a MongoDB Atlas")
            return True
        except (ServerSelectionTimeoutError, ConnectionFailure) as e:
            print(f"❌ Error conectando a MongoDB: {e}")
            self._client = None
            self._db = None
            return False
    
    def is_connected(self):
        """Verificar si está conectado"""
        return self._client is not None and self._db is not None
    
    def get_db(self):
        """Obtener instancia de base de datos"""
        return self._db
    
    def close(self):
        """Cerrar conexión"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None


# Inicializar conexión global
mongo = MongoDBConnection()


class TokenRepository:
    """Repositorio para gestionar tokens en MongoDB"""
    
    COLLECTION_NAME = "tokens"
    
    @staticmethod
    def get_collection():
        """Obtener colección de tokens"""
        if not mongo.is_connected():
            return None
        db = mongo.get_db()
        collection = db[TokenRepository.COLLECTION_NAME]
        
        # Crear índice de creación (si no existe)
        collection.create_index("created_at")
        collection.create_index("type")
        
        return collection
    
    @staticmethod
    def save_token(token_data):
        """
        Guardar un token con su análisis
        
        token_data: {
            "token": str,
            "header": dict,
            "payload": dict,
            "signature": str,
            "type": str ("valid", "invalid", "expired", etc),
            "is_valid": bool,
            "signature_valid": bool,
            "analysis": dict,
            "secret": str (opcional),
            "algorithm": str,
            "notes": str (opcional)
        }
        """
        collection = TokenRepository.get_collection()
        if collection is None:
            return None
        
        token_data["created_at"] = datetime.utcnow()
        result = collection.insert_one(token_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_all_tokens(limit=50):
        """Obtener todos los tokens guardados"""
        collection = TokenRepository.get_collection()
        if collection is None:
            return []
        
        return list(collection.find().sort("created_at", -1).limit(limit))
    
    @staticmethod
    def get_token_by_id(token_id):
        """Obtener un token específico por ID"""
        from bson import ObjectId
        collection = TokenRepository.get_collection()
        if collection is None:
            return None
        
        try:
            return collection.find_one({"_id": ObjectId(token_id)})
        except:
            return None
    
    @staticmethod
    def get_token_by_token_string(token_string):
        """Obtener un token específico por su valor de token"""
        collection = TokenRepository.get_collection()
        if collection is None:
            return None
        
        try:
            return collection.find_one({"token": token_string})
        except:
            return None
    
    @staticmethod
    def get_tokens_by_type(token_type):
        """Obtener tokens por tipo (valid, invalid, expired, etc)"""
        collection = TokenRepository.get_collection()
        if collection is None:
            return []
        
        return list(collection.find({"type": token_type}).sort("created_at", -1))
    
    @staticmethod
    def delete_token(token_id):
        """Eliminar un token"""
        from bson import ObjectId
        collection = TokenRepository.get_collection()
        if collection is None:
            return False
        
        try:
            result = collection.delete_one({"_id": ObjectId(token_id)})
            return result.deleted_count > 0
        except:
            return False
    
    @staticmethod
    def count_tokens():
        """Contar tokens guardados"""
        collection = TokenRepository.get_collection()
        if collection is None:
            return 0
        return collection.count_documents({})
    
    @staticmethod
    def get_statistics():
        """Obtener estadísticas de tokens"""
        collection = TokenRepository.get_collection()
        if collection is None:
            return {}
        
        stats = {
            "total": collection.count_documents({}),
            "valid": collection.count_documents({"is_valid": True}),
            "invalid": collection.count_documents({"is_valid": False}),
            "expired": collection.count_documents({"type": "expired"}),
        }
        return stats


class CollectionRepository:
    """Repositorio para gestionar colecciones de tokens"""
    
    COLLECTION_NAME = "collections"
    
    @staticmethod
    def get_collection():
        """Obtener colección de colecciones"""
        if not mongo.is_connected():
            return None
        db = mongo.get_db()
        collection = db[CollectionRepository.COLLECTION_NAME]
        
        # Crear índice
        collection.create_index("created_at")
        collection.create_index("user_id")
        
        return collection
    
    @staticmethod
    def create_collection(name, description="", user_id="default"):
        """
        Crear una nueva colección de tokens
        
        Retorna el ID de la colección
        """
        collection = CollectionRepository.get_collection()
        if collection is None:
            return None
        
        data = {
            "name": name,
            "description": description,
            "user_id": user_id,
            "tokens": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = collection.insert_one(data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_all_collections(user_id="default"):
        """Obtener todas las colecciones del usuario"""
        collection = CollectionRepository.get_collection()
        if collection is None:
            return []
        
        return list(collection.find({"user_id": user_id}).sort("created_at", -1))
    
    @staticmethod
    def get_collection_by_id(collection_id):
        """Obtener una colección específica"""
        from bson import ObjectId
        collection = CollectionRepository.get_collection()
        if collection is None:
            return None
        
        try:
            return collection.find_one({"_id": ObjectId(collection_id)})
        except:
            return None
    
    @staticmethod
    def add_token_to_collection(collection_id, token_id):
        """Agregar un token a una colección"""
        from bson import ObjectId
        collection = CollectionRepository.get_collection()
        if collection is None:
            return False
        
        try:
            collection.update_one(
                {"_id": ObjectId(collection_id)},
                {
                    "$push": {"tokens": token_id},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            return True
        except:
            return False
    
    @staticmethod
    def remove_token_from_collection(collection_id, token_id):
        """Eliminar un token de una colección"""
        from bson import ObjectId
        collection = CollectionRepository.get_collection()
        if collection is None:
            return False
        
        try:
            collection.update_one(
                {"_id": ObjectId(collection_id)},
                {
                    "$pull": {"tokens": token_id},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            return True
        except:
            return False
    
    @staticmethod
    def delete_collection(collection_id):
        """Eliminar una colección"""
        from bson import ObjectId
        collection = CollectionRepository.get_collection()
        if collection is None:
            return False
        
        try:
            result = collection.delete_one({"_id": ObjectId(collection_id)})
            return result.deleted_count > 0
        except:
            return False

