from flask import Flask, render_template, request, jsonify
import json
import binascii
import time
from datetime import datetime, timedelta

from jwt_analyzer.lexer import LexerJWT, LexerError, Token
from jwt_analyzer.parser import JWTParser, ParserError
from jwt_analyzer.semantic import validate_header, validate_payload, SemanticError
from jwt_analyzer.crypto_verify import verify_signature, sign_hmac
from jwt_analyzer.encoder import encode_jwt
from jwt_analyzer.base64url import b64url_decode, b64url_encode
from jwt_analyzer.mongodb import TokenRepository, CollectionRepository, mongo

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ======================== CASOS DE PRUEBA ========================

TEST_CASES = {
    "válidos": [
        {
            "id": "valid_hs256",
            "nombre": "Token Válido HS256",
            "descripción": "Token válido firmado con HS256",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
            "secret": "your-256-bit-secret",
            "esperado": "✓ Token válido con firma correcta"
        },
        {
            "id": "valid_hs384",
            "nombre": "Token Válido HS384",
            "descripción": "Token válido firmado con HS384",
            "token": "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkphbmUiLCJpYXQiOjE1MTYyMzkwMjJ9.VFb0qJ1LRg_4ujIYvxWpmeVf3xo3d8E1hsHuJsstISc7WY1Z7g_cbW1tzjYj51B3",
            "secret": "your-384-bit-secret-longer-than-256",
            "esperado": "✓ Token válido HS384"
        }
    ],
    "expirados": [
        {
            "id": "expired_token",
            "nombre": "Token Expirado",
            "descripción": "Token cuya fecha de expiración ya pasó",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZXhwIjoxNTE2MjM5MDIyfQ.1oPvLPCCGb1jUX5f0n5VVAi_-qWkDhS2PuOv0EgVhWw",
            "secret": "secret",
            "esperado": "⏰ Token expirado (exp claim vencido)"
        }
    ],
    "malformados": [
        {
            "id": "missing_dots",
            "nombre": "Token sin Puntos",
            "descripción": "Token sin los separadores de puntos (sintaxis incorrecta)",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
            "secret": "",
            "esperado": "✗ Error sintáctico: falta estructura HEADER.PAYLOAD.SIGNATURE"
        },
        {
            "id": "too_many_parts",
            "nombre": "Demasiadas Partes",
            "descripción": "Token con más de 3 partes",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.FALSESIGNATURE.EXTRA",
            "secret": "",
            "esperado": "✗ Error sintáctico: se encontraron 4 partes en lugar de 3"
        },
        {
            "id": "invalid_base64",
            "nombre": "Base64 Inválido",
            "descripción": "Header con caracteres Base64URL inválidos",
            "token": "###INVALID###.eyJzdWIiOiIxMjM0NTY3ODkwIn0.FALSESIGNATURE",
            "secret": "",
            "esperado": "✗ Error léxico: caracteres Base64URL inválidos"
        }
    ],
    "firma_inválida": [
        {
            "id": "bad_signature",
            "nombre": "Firma Inválida",
            "descripción": "Token con firma modificada",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.FALSESIGNATURE123456789",
            "secret": "correct-secret",
            "esperado": "✗ Firma inválida: no coincide con la esperada"
        },
        {
            "id": "wrong_secret",
            "nombre": "Secreto Incorrecto",
            "descripción": "Token verificado con secreto incorrecto",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
            "secret": "wrong-secret-123",
            "esperado": "✗ Firma inválida: secreto no coincide"
        }
    ]
}

def lexical_analysis(jwt_str):
    lexer = LexerJWT()
    try:
        tokens = lexer.tokenize(jwt_str)
        toks = [{"type": t.type, "value": t.value} for t in tokens]
        return {"ok": True, "tokens": toks}
    except LexerError as e:
        return {"ok": False, "error": str(e)}

def syntactic_analysis(jwt_str):
    # Gramática simple: JWT -> HEADER . PAYLOAD . SIGNATURE
    parts = jwt_str.split('.')
    if len(parts) != 3:
        return {"ok": False, "error": f"Estructura inválida: se esperaban 3 partes, se encontraron {len(parts)}"}
    return {"ok": True, "structure": "JWT → HEADER . PAYLOAD . SIGNATURE", "parts_count": 3}

def decode_parts(header_b64, payload_b64, signature_b64):
    try:
        h_bytes = b64url_decode(header_b64)
        p_bytes = b64url_decode(payload_b64)
        s_bytes = b64url_decode(signature_b64)
    except Exception as e:
        raise ValueError(f"Error Base64URL: {e}")

    # intentar parsear JSON header/payload
    header = None
    payload = None
    header_err = None
    payload_err = None
    try:
        header = json.loads(h_bytes.decode("utf-8"))
    except Exception as e:
        header_err = str(e)
    try:
        payload = json.loads(p_bytes.decode("utf-8"))
    except Exception as e:
        payload_err = str(e)

    return {
        "header_bytes_hex": binascii.hexlify(h_bytes).decode(),
        "payload_bytes_hex": binascii.hexlify(p_bytes).decode(),
        "signature_bytes_hex": binascii.hexlify(s_bytes).decode(),
        "header": header,
        "payload": payload,
        "header_err": header_err,
        "payload_err": payload_err,
        "raw_header_bytes": h_bytes,
        "raw_payload_bytes": p_bytes,
        "raw_signature_bytes": s_bytes,
    }

def semantic_analysis(header_obj, payload_obj):
    messages = []
    try:
        validate_header(header_obj)
        messages.append("Header: campos obligatorios presentes y tipos válidos.")
    except SemanticError as e:
        messages.append(f"Header ERROR: {e}")
    try:
        validate_payload(payload_obj, check_time=False)  # no fallar por tiempo a menos que se solicite
        messages.append("Payload: validación de tipos OK (temporal check opcional).")
    except SemanticError as e:
        messages.append(f"Payload ERROR: {e}")
    # Validaciones temporales si existen:
    if isinstance(payload_obj, dict):
        now = int(time.time())
        if "exp" in payload_obj:
            try:
                exp_ok = int(payload_obj["exp"]) >= now
                messages.append(f"Claim exp: {payload_obj['exp']} (ahora: {now}) -> {'válida' if exp_ok else 'expirada'}")
            except Exception as e:
                messages.append(f"Claim exp ERROR: {e}")
        if "iat" in payload_obj:
            messages.append(f"Claim iat: {payload_obj['iat']}")
    return messages

@app.route("/", methods=["GET", "POST"])
def index():
    output = {}
    token = ""
    secret = ""
    new_token = ""
    db_status = "Conectado" if mongo.is_connected() else "Desconectado"
    
    if request.method == "POST":
        action = request.form.get("action")
        token = request.form.get("jwt", "").strip()
        secret_text = request.form.get("secret", "")
        secret = secret_text.encode("utf-8") if secret_text else b""

        # Crear token
        if action == "create":
            payload_new = request.form.get("payload_new", "")
            secret_new_text = request.form.get("secret_new", "")
            algorithm = request.form.get("algorithm", "HS256")  # HS256 o HS384
            expiration_time = request.form.get("expiration_time", "3600")  # segundos
            
            try:
                payload_obj = json.loads(payload_new)
                
                # Agregar timestamps al payload
                now = int(time.time())
                payload_obj["iat"] = now  # issued at
                exp_seconds = int(expiration_time)
                payload_obj["exp"] = now + exp_seconds  # expiration time
                
                # Crear header con el algoritmo seleccionado
                header = {"alg": algorithm, "typ": "JWT"}
                new_token = encode_jwt(header, payload_obj, secret_new_text.encode("utf-8"))
                
                # Guardar en MongoDB si está conectado
                if mongo.is_connected():
                    token_data = {
                        "token": new_token,
                        "header": header,
                        "payload": payload_obj,
                        "signature": "...",
                        "type": "created",
                        "is_valid": True,
                        "signature_valid": True,
                        "algorithm": algorithm,
                        "expiration_seconds": exp_seconds,
                        "created_at": now,
                        "expires_at": payload_obj["exp"],
                        "notes": f"Token creado con algoritmo {algorithm} y expiración en {exp_seconds}s"
                    }
                    token_id = TokenRepository.save_token(token_data)
                    output["create_result"] = {
                        "ok": True, 
                        "token": new_token,
                        "token_id": str(token_id) if token_id else None,
                        "algorithm": algorithm,
                        "expires_at": payload_obj["exp"],
                        "expiration_seconds": exp_seconds
                    }
                else:
                    output["create_result"] = {
                        "ok": True, 
                        "token": new_token,
                        "algorithm": algorithm,
                        "expires_at": payload_obj["exp"],
                        "expiration_seconds": exp_seconds
                    }
            except Exception as e:
                output["create_result"] = {"ok": False, "error": str(e)}
            return render_template("index_improved.html",
                                   output=output, token=token, secret=secret_text,
                                   new_token=new_token, db_status=db_status)

        # Análisis completo en paneles
        if action == "analyze":
            # LEXICAL
            lex = lexical_analysis(token)
            output["lexical"] = lex

            # SYNTACTIC
            syn = syntactic_analysis(token)
            output["syntactic"] = syn

            # If basic syntactic OK, attempt decode
            if syn.get("ok"):
                parts = token.split('.')
                try:
                    decoded = decode_parts(parts[0], parts[1], parts[2])
                    output["decoded"] = {
                        "ok": True,
                        "header": decoded["header"],
                        "payload": decoded["payload"],
                        "header_err": decoded["header_err"],
                        "payload_err": decoded["payload_err"],
                        "header_hex": decoded["header_bytes_hex"],
                        "payload_hex": decoded["payload_bytes_hex"],
                        "signature_hex": decoded["signature_bytes_hex"],
                    }
                except Exception as e:
                    output["decoded"] = {"ok": False, "error": str(e)}
            # SEMANTIC (only if header/payload decode OK)
            if output.get("decoded", {}).get("ok") and output["decoded"]["header"] and output["decoded"]["payload"]:
                sem_msgs = semantic_analysis(output["decoded"]["header"], output["decoded"]["payload"])
                output["semantic"] = {"ok": True, "messages": sem_msgs}
            else:
                output["semantic"] = {"ok": False, "messages": ["No se puede realizar análisis semántico: header/payload no decodificados correctamente."]}

            # SIGNATURE: verify if secret provided
            signature_valid = False
            if secret:
                try:
                    parts = token.split('.')
                    decoded_raw = decode_parts(parts[0], parts[1], parts[2])
                    header_obj = decoded_raw["header"]
                    if header_obj is None:
                        output["signature"] = {"ok": False, "error": "Header no decodificado; no se puede verificar firma."}
                    else:
                        alg = header_obj.get("alg")
                        ok_sig = verify_signature(parts[0], parts[1], decoded_raw["raw_signature_bytes"], secret, alg)
                        signature_valid = ok_sig
                        expected = None
                        try:
                            expected = sign_hmac(f"{parts[0]}.{parts[1]}".encode("utf-8"), secret, alg)
                            expected_hex = binascii.hexlify(expected).decode()
                        except Exception:
                            expected_hex = None
                        output["signature"] = {"ok": True, "valid": ok_sig, "expected_hex": expected_hex}
                except Exception as e:
                    output["signature"] = {"ok": False, "error": str(e)}
            else:
                output["signature"] = {"ok": False, "error": "No se proporcionó secret para verificación (opcional)."}
            
            # Guardar en MongoDB si está conectado
            if mongo.is_connected() and output.get("decoded", {}).get("ok"):
                try:
                    is_valid = (
                        output.get("lexical", {}).get("ok", False) and
                        output.get("syntactic", {}).get("ok", False) and
                        output.get("semantic", {}).get("ok", False) and
                        signature_valid
                    )
                    
                    token_data = {
                        "token": token,
                        "header": output["decoded"]["header"],
                        "payload": output["decoded"]["payload"],
                        "signature": output["decoded"]["signature_hex"][:20] + "...",
                        "type": "valid" if is_valid else "invalid",
                        "is_valid": is_valid,
                        "signature_valid": signature_valid,
                        "algorithm": output["decoded"]["header"].get("alg", "unknown"),
                        "analysis": {
                            "lexical": output.get("lexical", {}),
                            "syntactic": output.get("syntactic", {}),
                            "semantic": output.get("semantic", {}),
                        },
                        "notes": ""
                    }
                    # ✅ GUARDAR REALMENTE EN MONGODB
                    print(f"[DEBUG] Intentando guardar token: {token[:50]}...")
                    token_id = TokenRepository.save_token(token_data)
                    print(f"[DEBUG] Token guardado con ID: {token_id}")
                    output["mongodb_saved"] = True
                    output["saved_token_id"] = str(token_id) if token_id else None
                except Exception as e:
                    print(f"[ERROR] Error guardando token: {e}")
                    import traceback
                    traceback.print_exc()
                    output["mongodb_saved"] = False
                    output["mongodb_error"] = str(e)
            else:
                print(f"[DEBUG] No se guardará: mongo.is_connected()={mongo.is_connected()}, decoded.ok={output.get('decoded', {}).get('ok')}")

    return render_template("index_improved.html",
                           output=output, token=token, secret=secret.decode() if isinstance(secret, bytes) else secret,
                           new_token=new_token, db_status=db_status)

# ======================== API Routes para MongoDB ========================

@app.route("/api/tokens", methods=["GET"])
def api_get_tokens():
    """Obtener todos los tokens guardados"""
    if not mongo.is_connected():
        return jsonify({"error": "MongoDB no conectado"}), 503
    
    tokens = TokenRepository.get_all_tokens(limit=100)
    # Convertir ObjectId a string
    for token in tokens:
        token["_id"] = str(token["_id"])
    
    return jsonify(tokens)

@app.route("/api/tokens/<token_id>", methods=["GET"])
def api_get_token(token_id):
    """Obtener un token específico"""
    if not mongo.is_connected():
        return jsonify({"error": "MongoDB no conectado"}), 503
    
    token = TokenRepository.get_token_by_id(token_id)
    if not token:
        return jsonify({"error": "Token no encontrado"}), 404
    
    token["_id"] = str(token["_id"])
    return jsonify(token)

@app.route("/api/tokens", methods=["POST"])
def api_save_token():
    """Guardar un token con su análisis"""
    if not mongo.is_connected():
        return jsonify({"error": "MongoDB no conectado"}), 503
    
    data = request.get_json()
    token_id = TokenRepository.save_token(data)
    
    if token_id:
        return jsonify({"success": True, "token_id": token_id}), 201
    else:
        return jsonify({"error": "Error al guardar token"}), 500

@app.route("/api/tokens/<token_id>", methods=["DELETE"])
def api_delete_token(token_id):
    """Eliminar un token"""
    if not mongo.is_connected():
        return jsonify({"error": "MongoDB no conectado"}), 503
    
    if TokenRepository.delete_token(token_id):
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Error al eliminar token"}), 500

@app.route("/api/statistics", methods=["GET"])
def api_get_statistics():
    """Obtener estadísticas de tokens"""
    if not mongo.is_connected():
        return jsonify({"error": "MongoDB no conectado"}), 503
    
    stats = TokenRepository.get_statistics()
    return jsonify(stats)

# ======================== Colecciones ========================

@app.route("/api/collections", methods=["GET"])
def api_get_collections():
    """Obtener todas las colecciones"""
    if not mongo.is_connected():
        return jsonify({"error": "MongoDB no conectado"}), 503
    
    collections = CollectionRepository.get_all_collections()
    for coll in collections:
        coll["_id"] = str(coll["_id"])
    
    return jsonify(collections)

@app.route("/api/collections", methods=["POST"])
def api_create_collection():
    """Crear una nueva colección"""
    if not mongo.is_connected():
        return jsonify({"error": "MongoDB no conectado"}), 503
    
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")
    
    if not name:
        return jsonify({"error": "Nombre de colección requerido"}), 400
    
    collection_id = CollectionRepository.create_collection(name, description)
    
    if collection_id:
        return jsonify({"success": True, "collection_id": collection_id}), 201
    else:
        return jsonify({"error": "Error al crear colección"}), 500

@app.route("/api/collections/<collection_id>", methods=["GET"])
def api_get_collection(collection_id):
    """Obtener una colección específica"""
    if not mongo.is_connected():
        return jsonify({"error": "MongoDB no conectado"}), 503
    
    collection = CollectionRepository.get_collection_by_id(collection_id)
    if not collection:
        return jsonify({"error": "Colección no encontrada"}), 404
    
    collection["_id"] = str(collection["_id"])
    return jsonify(collection)

@app.route("/api/collections/<collection_id>/tokens/<token_id>", methods=["POST"])
def api_add_token_to_collection(collection_id, token_id):
    """Agregar un token a una colección"""
    if not mongo.is_connected():
        return jsonify({"error": "MongoDB no conectado"}), 503
    
    if CollectionRepository.add_token_to_collection(collection_id, token_id):
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Error al agregar token"}), 500

@app.route("/api/collections/<collection_id>/tokens/<token_id>", methods=["DELETE"])
def api_remove_token_from_collection(collection_id, token_id):
    """Eliminar un token de una colección"""
    if not mongo.is_connected():
        return jsonify({"error": "MongoDB no conectado"}), 503
    
    if CollectionRepository.remove_token_from_collection(collection_id, token_id):
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Error al eliminar token"}), 500

@app.route("/api/collections/<collection_id>", methods=["DELETE"])
def api_delete_collection(collection_id):
    """Eliminar una colección"""
    if not mongo.is_connected():
        return jsonify({"error": "MongoDB no conectado"}), 503
    
    if CollectionRepository.delete_collection(collection_id):
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Error al eliminar colección"}), 500

# ======================== CASOS DE PRUEBA ========================

@app.route("/api/test-cases", methods=["GET"])
def api_get_test_cases():
    """Obtener todos los casos de prueba"""
    return jsonify(TEST_CASES)

@app.route("/api/test-cases/<category>", methods=["GET"])
def api_get_test_case_category(category):
    """Obtener casos de prueba por categoría"""
    if category in TEST_CASES:
        return jsonify(TEST_CASES[category])
    else:
        return jsonify({"error": "Categoría no encontrada"}), 404

if __name__ == "__main__":
    app.run(debug=True)
