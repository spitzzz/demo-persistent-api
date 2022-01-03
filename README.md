# Demo Persistent API

The purpose of this repository is to provide basic demo code as a starting point for building a persistent API using Terraform. This repository makes use of open-source Terraform modules from the [Terraform Registry](https://registry.terraform.io/). Please note, this repository should only be used for example purposes, and all modules being referenced from the Terraform Registry should be fully vetted if you plan to re-purpose this code to your own use case.

## About the resources deployed

The included Terraform code will deploy 1 PUBLIC Amazon API Gateway (without any authorizer), 1 AWS Lambda Function (python based), 1 DynamoDB Table, and other supporting resources such as IAM roles, policies, etc.

## Requirements
- Terraform installed w/ versions >= `v1.0.10`
- Valid AWS Credentials configured locally for Terraform to utilize
- Python >= `3.10.1`

## How to Deploy

1. Clone down this repository
```
git clone git@github.com:spitzzz/demo-persistent-api.git
```

2. cd into the newly cloned repository directory
```
cd demo-persistent-api
```

3. Initialize Terraform
```
terraform init
```

4. Run a `terraform plan` and analyze the results are as you would expect.

5. Run a `terraform apply` - type `yes` if the results are as you would expect.

## How to Test the API

After a successful Terraform apply, you should receive the `api_invoke_url` as an output in the result.

1. Using the `api_invoke_url` open a tool such as [Postman](https://www.postman.com/) that you can use to build a request body.

Build a `POST` request with the `body` of the request following this format:
```
 {
     'id': string || number,
     'date': string,
     'type': string,
     'data': string
 }
```

Example Object:
```
 {
     'id': 1,
     'date': "2022-01-02T23:48:59+0000",
     'type': "info",
     'data': "test"
 }
 ```

 The current **example** lambda code also supports a list of objects like so:
 
```
[
    {
        'id': 1,
        'date': "2022-01-02T23:48:59+0000",
        'type': "info",
        'data': "test"
    },
    {
        'id': 2,
        'date': "2022-01-02T23:48:59+0000",
        'type': "error",
        'data': "uh oh"
    },
    {
        'id': 3,
        'date': "2022-01-02T23:48:59+0000",
        'type': "info",
        'data': "test2"
    }
]
 ```

 ## Cleanup

 Once you are finished testing the API, and want to destroy the resources, run the following commands/steps:

1. cd into repository you cloned the code
```
cd demo-persistent-api
```

2. Run Terraform Destroy
```
terraform destroy
```

 ## Contribute

 Please feel free to open a pull request for any improvements, suggestions, or bug fixes you might have.