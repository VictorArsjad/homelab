# Ngrok

## Installation

```
helm repo add ngrok https://charts.ngrok.com

export NGROK_AUTHTOKEN=
export NGROK_API_KEY=

helm install ngrok-operator ngrok/ngrok-operator \
  --namespace ngrok-operator \
  --create-namespace \
  --set credentials.apiKey=$NGROK_API_KEY \
  --set credentials.authtoken=$NGROK_AUTHTOKEN

kubectl apply -f ./ngrok/
```

## Reference

- https://dashboard.ngrok.com/get-started/setup/kubernetes