. venv/bin/activate
python -m jwt_analyzer.cli create --payload '{"sub":"demo","iat":$(date +%s),"exp":$(( $(date +%s) + 3600))}' --secret demo123
