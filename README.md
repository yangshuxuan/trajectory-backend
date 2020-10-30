# trajectory-backend

1. 这是轨迹处理的后端服务，充分利用了postgresql/postgis提供的支持，进行轨迹相关操作
2. 这个服务的轨迹是以Line表示，而不是通常的Point,这样有助于提高处理的性能
3. 该后端也使用了flask-sqlalchemy进行数据库相关操作，非常方便，由于该库的文档不够丰富，大量的操作都是摸索出来的，因此很有借鉴意义
4. [这是GIS处理需要使用的库](https://geoalchemy-2.readthedocs.io/en/latest/)

