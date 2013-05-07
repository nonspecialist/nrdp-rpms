# This option defines which mock configuration to use -- see /etc/mock for 
# the available configuration files for your system.
MOCK_CONFIG=epel-6-x86_64

SHELL=/bin/bash

SPEC=nrdp.spec
SOURCE=nrdp.zip
SRCDIR := $(shell /usr/bin/rpmbuild --eval '%{_sourcedir}' 2>/dev/null)
SRCS=$(SRCDIR)/$(SOURCE)
PATCHES=$(wildcard *.patch)
BASE=http://assets.nagios.com/downloads/nrdp
NAME=$(shell grep 'define name' $(SPEC) | awk '{ print $$3 }')
VERSION=$(shell grep 'define unmangled_version' $(SPEC) | awk '{ print $$3 }')
RELEASE=$(shell grep 'define release' $(SPEC) | awk '{ print $$3 }')
# only query mock if it's installed
MOCK_ROOT=$(shell type -p mock >/dev/null && /usr/bin/mock -r $(MOCK_CONFIG) --print-root-path)
MOCK_RESULT=$(shell /usr/bin/readlink -f $(MOCK_ROOT)/../result)

NVR=$(NAME)-$(VERSION)-$(RELEASE)
MOCK_SRPM=$(NVR).src.rpm

.DEFAULT: all

all: $(SRCS) srpm rpm

mock: $(SRCS) mock-rpm
	@echo "BUILD COMPLETE; RPMS are in $(MOCK_RESULT)"

$(SRCS):
	wget -O $(SRCDIR)/$(SOURCE) $(BASE)/$(SOURCE)
	cp $(PATCHES) $(SRCDIR)

srpm:
	rpmbuild -bs $(SPEC)

rpm:
	rpmbuild -bb $(SPEC)

mock-srpm:
	mock -r $(MOCK_CONFIG) --init
	mock -r $(MOCK_CONFIG) --buildsrpm --spec $(SPEC) --sources $(SRCDIR)

mock-rpm: mock-srpm
	cp $(MOCK_RESULT)/$(MOCK_SRPM) .
	mock -r $(MOCK_CONFIG) --rebuild $(MOCK_SRPM)

clean:
	rm -f $(SOURCE) $(SRCDIR)/$(SOURCE)
	for patch in $(PATCHES); do \
		rm -f $(SRCDIR)/$$patch; \
	done

mock-clean: clean
	mock -r $(MOCK_CONFIG) --clean
	rm -f $(MOCK_SRPM)
