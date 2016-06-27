all: env test binary

clean:
	bin/clean.sh

env:
	bin/env.sh

test:
	bin/test.sh

packages:
	bin/packages.sh

binary:
	pyinstaller binary/binary.spec

.PHONY: binary
