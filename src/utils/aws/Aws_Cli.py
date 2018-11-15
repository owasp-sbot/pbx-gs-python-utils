import os
import boto3
import json
import shutil

class Aws_Cli:
    def __init__(self, **kwargs):
        self.aws_lambda = boto3.client('lambda', region_name = kwargs.get('region_name'))
        self.aws_s3     = boto3.client('s3'    , region_name = kwargs.get('region_name'))

    def lambda_create_function      (self, name, role, handler, s3_bucket, s3_key, memory = 512, timeout = 25 , runtime = 'python3.6'):
        if self.lambda_function_exists(name) is False:
            return self.aws_lambda.create_function(
                    FunctionName  = name             ,
                    Runtime       = runtime          ,
                    Role          = role             ,
                    Handler       = handler          ,
                    MemorySize    = memory           ,
                    Timeout       = timeout          ,
                    Code          = {
                                        "S3Bucket" : s3_bucket ,
                                        "S3Key"    : s3_key    })
        return None

        #

    def lambda_delete_function      (self, name                                                                 ):
        if self.lambda_function_exists(name):
            self.aws_lambda.delete_function( FunctionName = name)
        return self
        #

    def lambda_functions            (self                                                                       ):
        data = {}
        for function in self.aws_lambda.list_functions().get('Functions'):
            data[function['FunctionName']] = function
        return data

        #

    def lambda_function_exists      (self, name                                                                 ):
        try:
            self.aws_lambda.get_function(FunctionName=name)
            return True
        except Exception:
            return False

        #

    def lambda_function_info        (self, name                                                                 ):
        return self.aws_lambda.get_function(FunctionName = name)

    def lambda_invoke_function      (self, name, payload                                                        ):
        response      = self.aws_lambda.invoke(FunctionName=name, Payload = json.dumps(payload) )

        result_bytes  = response.get('Payload').read()
        result_string = result_bytes.decode('utf-8')
        result        = json.loads(result_string)
        return result, response

        #

    def lambda_invoke_function_async(self, name, payload                                                        ):
        return  self.aws_lambda.invoke(FunctionName=name, Payload = json.dumps(payload), InvocationType='Event')

    def lambda_update_function      (self, name, s3_bucket,s3_key                                               ):
        return self.aws_lambda.update_function_code(FunctionName = name,
                                                    S3Bucket     = s3_bucket ,
                                                    S3Key        = s3_key    )

        #

    def s3_buckets                  (self                                                                       ):
        data = {}
        for bucket in self.aws_s3.list_buckets().get('Buckets'):
            data[bucket['Name']] = bucket
        return data

        #

    #def s3_add_notification        (self, s)

    def s3_upload_folder            (self, folder, s3_bucket, s3_key                                            ):
        file = Aws_Utils().zip_folder(folder)
        self.aws_s3.upload_file(file, s3_bucket, s3_key)
        os.remove(file)
        return self

        #


class Aws_Utils:

    @staticmethod
    def run_code_in_lambda(code):
        file_Path = 'temp_code/code.py'
        temp_Dir  = 'temp_code'
        zip_file  = 'temp_code.zip'

        def create_temp_files():
            if not os.path.exists(temp_Dir):
                os.mkdir(temp_Dir)
            with open(file_Path, "w+") as f:
                f.write(code)

        def delete_temp_files():
            os.remove(file_Path)
            os.remove(zip_file)
            os.rmdir(temp_Dir)

        create_temp_files()

        name      = 'dynamic_code'
        role      = 'arn:aws:iam::244560807427:role/lambda_basic_execution'
        handler   = 'code.dynamic_method'
        s3_bucket = 'gs-lambda-tests'
        s3_key    = 'dinis/lambda-using-dynamic-code.zip'

        aws = Aws_Cli()
        aws.lambda_delete_function(name)
        aws.s3_upload_folder      (temp_Dir, s3_bucket, s3_key)
        aws.lambda_create_function(name, role, handler, s3_bucket, s3_key)

        (result, response) = aws.lambda_invoke_function(name, {})

        aws.lambda_delete_function(name)
        delete_temp_files()
        return result

    @staticmethod
    def zip_folder(root_dir):
        return shutil.make_archive(root_dir, "zip", root_dir)