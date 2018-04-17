Установка:

1. Установить docker
2. Установить libvirt
3. Спуллить daronar/base_phoronix
4. Скачать образ carrier.
5. Создать образ dockerinvm:
    5.1. Скачать docker.
    5.2. daronar/base_phoronix
    5.3. Настроить docker-tcp-socket (https://www.ivankrizsan.se/2016/05/18/enabling-docker-remote-api-on-ubuntu-16-04/)
6. Прописать пути к xml и qcow2 в SETTINGS.