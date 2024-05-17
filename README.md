# UData-test task

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/meg4ik/UData-test.git
    ```

2. Change directory to the project folder:

    ```bash
    cd UData-test
    ```

3. Create .env file based on .env_example in / directory

4. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

## Accessible urls
```sh
'all_products/'
''
'products/<str:product_uuid>/'
'products/<str:product_uuid>/<str:product_field>/'
```