all: env test binary

clean:
	bin/clean.sh

env: clean
	bin/set_version.sh
	bin/env.sh

test:
	bin/test.sh

packages: binary
	bin/packages.sh

binary: env
	pyinstaller binary/binary.spec

.PHONY: binary
