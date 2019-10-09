#!/bin/bash
pip install pyyaml --target ./lambda
aws cloudformation package --template-file ./macro.yaml --s3-bucket geekoosh-macro --output-template-file ./macro-out.yaml
aws cloudformation deploy --template-file ./macro-out.yaml --stack-name macro-string-list-template --capabilities CAPABILITY_IAM