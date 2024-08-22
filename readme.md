
## Docker image build & run container  
```bash
  docker-compose build
  docker-compose up
``` 

## How to test the project?
```bash
curl --request POST \
  --url http://127.0.0.1:8000/faucet/fund/ \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/8.6.1' \
  --data '{
    "wallet_address": "0x5839F5d20b12081717d7b62B30263EB4FCf65089"
}'
```

```bash
curl --request GET \
  --url http://127.0.0.1:8000/faucet/stats/ \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/8.6.1'
```

![POST](https://github.com/azflin7/sepolia-faucet-api/assets/img/screenshot1.png)  

![GET](https://github.com/azflin7/sepolia-faucet-api/assets/img/screenshot2.png)  