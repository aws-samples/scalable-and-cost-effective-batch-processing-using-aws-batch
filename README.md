## Scalable and Cost-Effective Batch Processing with AWS Batch and Amazon FSx

This repository should be used when deploying the batch processing demonstration outlined in blog post: https://aws.amazon.com/blogs/hpc/ml-training-with-aws-batch-and-amazon-fsx/

## Getting started

Get started by running the following command from the repository base directory. This command should take approximately 20 minutes to complete.

```
$ aws cloudformation create-stack --stack-name aws-hpc-blog-batch-processing --template-body file://infra/template.yml --capabilities CAPABILITY_IAM
```

Next, retrieve the list of CloudFormation stack outputs for this stack. These values will be used in the proceeding steps, so keep them somewhere you can reference later.

```
$ aws cloudformation describe-stacks --stack-name aws-hpc-blog-batch-processing --query "Stacks[].Outputs[]" --output text
```

Next, create the input dataset to create copies of the test-data1.csv file. Refer to the CloudFormation stack outputs to find the value for <BucketName>.

```
$ BUCKET_NAME=<BucketName>
$ aws s3 cp model/test-data1.csv s3://${BUCKET_NAME}/input/
$ for a in {2..100}; do aws s3 cp s3://${BUCKET_NAME}/input/test-data1.csv s3://${BUCKET_NAME}/input/test-data${a}.csv; done
```

Next, create the Docker image and upload it to ECR where it will be accessible to our Compute Environment. Refer to the CloudFormation stack outputs to find the value for <RepositoryUri>.

```
$ REPOSITORY_URI=<RepositoryUri>
$ cd model  # enter the model directory for docker build
$ docker build -t $REPOSITORY_URI .
$ aws ecr get-login-password | docker login --username AWS --password-stdin $REPOSITORY_URI
$ docker push $REPOSITORY_URI
$ cd ..     # return to repository base directory
```

Run the following to submit the Job with two workers

```
$ aws batch submit-job --cli-input-json file://test-2-workers.json
```

Run the following to submit the Job with 10 workers

```
$ aws batch submit-job --cli-input-json file://test-10-workers.json
```

Now that our batch process has generated a set of predictions, we can copy them to S3 by executing an FSx for Lustre Data Repository export task. Run the following to initiate the task. Refer to the CloudFormation stack outputs to find the value for <FSxFileSystemId>.

```
$ FSX_FILESYSTEM_ID=<FSxFileSystemId>
$ aws fsx create-data-repository-task --type EXPORT_TO_REPOSITORY --file-system-id $FSX_FILESYSTEM_ID --report Enabled=false
```

## Project Structure


## Citation


## Useful links

## Others

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

