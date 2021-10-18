setup:
	@./scripts/setup.sh

build:
	@./scripts/build.sh

install: build
	@./scripts/install.sh

upload: build
	@./scripts/upload.sh

upload-test: build
	@./scripts/upload-test.sh

lint:
	@./scripts/lint.sh

fix:
	@./scripts/fix.sh

unit-test:
	@./scripts/unit-test.sh

pip-update:
	@./scripts/pip-update.sh

test: unit-test lint

.PHONY: build
