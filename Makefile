.DEFAULT_GOAL := ci  # The default target if you just run "make"

venv-setup: # Setup Python venv
	rm -rf venv/
	python3 -m venv venv

install: # Install dependencies in Python venv
	. venv/bin/activate
	pip3 install --user -r requirements.txt

setup: venv-setup install

fmt:  # Format Python source
	yapf --in-place --parallel --recursive src

lint:  # Format, style, and type linting
	yapf --diff --parallel --recursive src
	bandit -r src
	pylint src
	mypy src --disallow-untyped-defs --ignore-missing-imports --warn-unused-ignores

test: # Run unit tests
	nose2 --with-coverage --coverage src --coverage-config setup.cfg

ci: fmt lint test

update-requirements:
	pip3 install -r requirements-top-level.txt --upgrade
	pip freeze -r requirements-top-level.txt > requirements.txt

sam-package:  # Build Dependencies (https://amzn.to/2MzGpXo), Generate CF, and upload package to S3
	sam build --manifest requirements-runtime.txt --use-container
	sam package \
		--template-file .aws-sam/build/template.yaml \
		--output-template-file template-out.yml \
		--s3-bucket $(bucket) \
		--s3-prefix remediations

sam-deploy-master: sam-package # Deploy CF stack
	sam deploy \
		--capabilities CAPABILITY_NAMED_IAM \
		--stack-name remediations \
		--s3-bucket $(bucket) \
		--s3-prefix remediations \
		--template-file template-out.yml

sam-deploy-satellite: sam-package # Deploy CF stack
	sam deploy \
		--capabilities CAPABILITY_NAMED_IAM \
		--stack-name remediations \
		--s3-bucket $(bucket) \
		--s3-prefix remediations \
		--template-file template-out.yml \
		--parameter-overrides IsMasterAccount='false' CreateSSMDocument='false' MasterAccountId=$(masterAccountId)

deploy-master: sam-package sam-deploy-master

deploy-satellite: sam-package sam-deploy-satellite

deploy-sar: # To associate an IAM role with the stack, add the param role="--role-arn <aws-role-arn>"
	aws cloudformation deploy --stack-name panther-aws-remediations --template-file template-sar.yml --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND --region $(region) $(role)
