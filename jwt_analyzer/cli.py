# cli.py
import argparse
import json
from .parser import JWTParser, ParserError
from .semantic import validate_header, validate_payload, SemanticError
from .crypto_verify import verify_signature
from .base64url import b64url_encode, b64url_decode
from .encoder import encode_jwt

def cmd_decode(args):
    parser = JWTParser()
    try:
        parsed = parser.parse(args.token)
    except ParserError as e:
        print("Parse error:", e)
        return
    print("Header (decoded):")
    print(json.dumps(parsed["header"], indent=2))
    print("\nPayload (decoded):")
    print(json.dumps(parsed["payload"], indent=2))

def cmd_validate(args):
    parser = JWTParser()
    try:
        parsed = parser.parse(args.token)
    except Exception as e:
        print("Parse error:", e)
        return
    try:
        validate_header(parsed["header"])
        validate_payload(parsed["payload"], check_time=not args.skip_time)
    except SemanticError as e:
        print("Semantic validation error:", e)
        return
    # Verify signature if secret provided
    if args.secret is None:
        print("Semantic validation OK. No secret provided to verify signature.")
        return
    secret = args.secret.encode('utf-8')
    alg = parsed["header"].get("alg")
    ok = verify_signature(parsed["header_b64"], parsed["payload_b64"], parsed["signature"], secret, alg)
    print("Semantic validation OK.")
    print("Signature valid:" , ok)

def cmd_create(args):
    header = json.loads(args.header) if args.header else {"alg": args.alg, "typ": "JWT"}
    payload = json.loads(args.payload)
    secret = args.secret.encode('utf-8')
    token = encode_jwt(header, payload, secret)
    print(token)

def main():
    parser = argparse.ArgumentParser(prog="jwt_analyzer")
    sub = parser.add_subparsers(dest="cmd")
    d = sub.add_parser("decode")
    d.add_argument("token")
    v = sub.add_parser("validate")
    v.add_argument("token")
    v.add_argument("--secret", required=False)
    v.add_argument("--skip-time", action="store_true", help="Skip exp/iat time checks")
    c = sub.add_parser("create")
    c.add_argument("--payload", required=True, help='Payload JSON string')
    c.add_argument("--header", required=False, help='Header JSON string')
    c.add_argument("--alg", default="HS256")
    c.add_argument("--secret", required=True)
    args = parser.parse_args()
    if args.cmd == "decode":
        cmd_decode(args)
    elif args.cmd == "validate":
        cmd_validate(args)
    elif args.cmd == "create":
        cmd_create(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
