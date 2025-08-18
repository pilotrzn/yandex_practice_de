export KUBECONFIG=/home/aavdonin/.kube/config
docker build . -t cr.yandex/crpkcnolbskcb64t810s/de-registry/stg_service:v2025-07-24-r1
docker push cr.yandex/crpkcnolbskcb64t810s/de-registry/stg_service:v2025-07-24-r1

helm upgrade --install --atomic stg-service app -n c04-avdonin-aleksej